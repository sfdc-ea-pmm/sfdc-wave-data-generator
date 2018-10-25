import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from data_generator import DataGenerator
from datetime import datetime


def run(batch_id, source_file_name, output_file_name, source_pricebook, source_work_orders):
    data_gen = DataGenerator()

    # load source file
    data_gen.load_source_file(source_file_name)

    pricebook = data_gen.load_dataset("Pricebook", source_pricebook, ['Id', 'External_Id__c']).dict('Id', 'External_Id__c')
    data_gen.add_map_column('PricebookEntry.External_Id__c', 'PricebookEntryId', pricebook)

    work_orders = data_gen.load_dataset("WorkOrders", source_work_orders, ['Id', 'External_ID__c']).dict('Id', 'External_ID__c')
    data_gen.add_map_column('WorkOrder.External_Id__c', 'WorkOrderId', work_orders)

    data_gen.apply_transformations()

    data_gen.write(output_file_name, columns=[
        'External_ID__c',
        'PricebookEntry.External_Id__c',
        'WorkOrder.External_Id__c',
        'QuantityConsumed'
    ])

def update(source_file_name, output_file_name, source_work_orders):
    data_gen = DataGenerator()

    # load source file
    data_gen.load_source_file(source_file_name)

    service_appointments = data_gen.load_dataset("WorkOrders", source_work_orders, ['External_ID__c']).dict('External_ID__c', 'External_ID__c')
    service_appointments[None] = 'None'

    data_gen.add_map_column('WorkOrder.External_Id__c', 'WorkOrder.External_Id__c', service_appointments)

    data_gen.apply_transformations()

    data_gen.filter(lambda cv: cv['WorkOrder.External_Id__c'].startswith('WO.'))

    data_gen.apply_transformations()

    data_gen.write(output_file_name, columns=[
        'External_ID__c',
        'PricebookEntry.External_Id__c',
        'WorkOrder.External_Id__c',
        'QuantityConsumed'
    ])


if __name__ == "__main__":
    # execute only if running as a script
    run(datetime.now().strftime("%Y%m%d%-H%M%S%f"), 'data/output/ProductConsumed.csv', 'data/output/ProductConsumed.csv',
        'data/output/PricebookEntry.csv', 'data/output/WorkOrder.csv')