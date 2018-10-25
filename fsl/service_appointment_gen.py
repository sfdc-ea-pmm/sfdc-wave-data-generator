import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import dateutil.parser

from data_generator import DataGenerator
from datetime import date
from datetime import datetime
from datetime import timedelta

today = date.today()
today = datetime.combine(today, datetime.min.time())


def run(batch_id, source_file_name, output_file_name, source_accounts, source_service_resources,
        source_service_territories, source_work_orders, reference_datetime=today):
    data_gen = DataGenerator()

    # load source file
    data_gen.load_source_file(source_file_name)

    data_gen.add_formula_column('EarliestStartTime', lambda cv: dateutil.parser.parse(cv['EarliestStartTime']))

    data_gen.apply_transformations()

    data_gen.sort_by('EarliestStartTime', reverse=True)

    # shift dates to be 2 weeks prior to the reference date
    delta = reference_datetime.date() - data_gen.row_to_column_values(data_gen.rows[0])['EarliestStartTime'].date()
    data_gen.add_formula_column('EarliestStartTime',
                                lambda cv: (cv['EarliestStartTime'] + timedelta(days=delta.days - 1)).replace(tzinfo=None))

    data_gen.add_formula_column('ActualStartTime',
                                lambda cv: "" if cv['ActualStartTime'] == "" else (dateutil.parser.parse(cv['ActualStartTime']) + timedelta(days=delta.days - 1)).replace(tzinfo=None))

    data_gen.add_formula_column('ActualEndTime',
                                lambda cv: "" if cv['ActualEndTime'] == "" else (dateutil.parser.parse(cv['ActualEndTime']) + timedelta(days=delta.days - 1)).replace(tzinfo=None))

    data_gen.add_formula_column('ArrivalWindowStartTime',
                                lambda cv: "" if cv['ArrivalWindowStartTime'] == "" else (dateutil.parser.parse(cv['ArrivalWindowStartTime']) + timedelta(days=delta.days - 1)).replace(tzinfo=None))

    data_gen.add_formula_column('ArrivalWindowEndTime',
                                lambda cv: "" if cv['ArrivalWindowEndTime'] == "" else (dateutil.parser.parse(cv['ArrivalWindowEndTime']) + timedelta(days=delta.days - 1)).replace(tzinfo=None))

    data_gen.add_formula_column('DueDate',
                                lambda cv: "" if cv['DueDate'] == "" else (dateutil.parser.parse(cv['DueDate']) + timedelta(days=delta.days - 1)).replace(tzinfo=None))

    data_gen.apply_transformations()

    data_gen.add_copy_column('CreatedDate__c', 'EarliestStartTime')

    accounts = data_gen.load_dataset("Accounts", source_accounts, ['Id', 'External_ID__c']).dict('Id', 'External_ID__c')

    data_gen.add_map_column('Account.External_Id__c', 'AccountId', accounts)

    service_resources = data_gen.load_dataset("ServiceResources", source_service_resources, ['Id', 'External_ID__c']).dict('Id', 'External_ID__c')

    data_gen.add_map_column('ServiceResource.External_Id__c', 'FSLDemoTools_Service_Resource__c', service_resources)

    service_territories = data_gen.load_dataset("ServiceTerritories", source_service_territories, ['Id', 'External_ID__c']).dict('Id', 'External_ID__c')

    data_gen.add_map_column('ServiceTerritory.External_Id__c', 'ServiceTerritoryId', service_territories)

    work_orders = data_gen.load_dataset("WorkOrders", source_work_orders, ['Id', 'External_ID__c']).dict('Id', 'External_ID__c')

    data_gen.add_map_column('WorkOrder.External_Id__c', 'ParentRecordId', work_orders)

    data_gen.apply_transformations()

    data_gen.filter(lambda cv: cv['WorkOrder.External_Id__c'].startswith('WO.'))

    data_gen.apply_transformations()

    data_gen.write(output_file_name, columns=[
        'External_ID__c',
        'CreatedDate__c',
        'ServiceResource.External_Id__c',
        'ServiceTerritory.External_Id__c',
        'WorkOrder.External_Id__c',
        'ActualStartTime',
        'ArrivalWindowStartTime',
        'ActualDuration',
        'EarliestStartTime',
        'Duration',
        'DurationType',
        'Status',
        'DueDate',
        'ActualEndTime',
        'ArrivalWindowEndTime'
    ])
    return delta


if __name__ == "__main__":
    # execute only if running as a script
    run(datetime.now().strftime("%Y%m%d%-H%M%S%f"), 'data/output/ServiceAppointment.csv', 'data/output/ServiceAppointment.csv',
        'data/output/Account.csv', 'data/output/ServiceResource.csv', 'data/output/ServiceTerritory.csv',
        'data/output/WorkOrder.csv')