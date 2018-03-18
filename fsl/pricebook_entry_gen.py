import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from data_generator import DataGenerator
from datetime import datetime


def run(batch_id, source_file_name, output_file_name, source_products):
    data_gen = DataGenerator()

    # load source file
    data_gen.load_source_file(source_file_name)

    products = data_gen.load_dataset("Products", source_products, ['Id', 'External_Id__c']).dict('Id', 'External_Id__c')
    data_gen.add_map_column('Product2.External_Id__c', 'Product2Id', products)

    data_gen.add_constant_column('Pricebook2.Name', 'Standard Price Book')

    data_gen.apply_transformations()

    data_gen.write(output_file_name, columns=[
        'External_Id__c',
        'Product2.External_Id__c',
        'IsActive',
        'Pricebook2.Name',
        'UnitPrice'
    ])


if __name__ == "__main__":
    # execute only if running as a script
    run(datetime.now().strftime("%Y%m%d%-H%M%S%f"), 'data/output/PricebookEntry.csv', 'data/output/PricebookEntry.csv',
        'data/output/Product2.csv')
