import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from data_generator import DataGenerator
from datetime import datetime


def run(batch_id, source_file_name, output_file_name, source_operating_hours):
    data_gen = DataGenerator()

    # load source file
    data_gen.load_source_file(source_file_name)

    operating_hours = data_gen.load_dataset("OperatingHours", source_operating_hours, ['Id', 'External_Id__c']).dict('Id', 'External_Id__c')

    data_gen.add_map_column('OperatingHours.External_Id__c', 'OperatingHoursId', operating_hours)

    data_gen.apply_transformations()

    data_gen.write(output_file_name, columns=[
        'External_Id__c',
        'Name',
        'OperatingHours.External_Id__c',
        'State',
        'IsActive',
        'Country',
        'City'
    ])


if __name__ == "__main__":
    # execute only if running as a script
    run(datetime.now().strftime("%Y%m%d%-H%M%S%f"), 'data/output/ServiceTerritory.csv', 'data/output/ServiceTerritory.csv',
        'data/output/OperatingHours.csv')
