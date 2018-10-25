import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import dateutil.parser

from data_generator import DataGenerator
from datetime import date
from datetime import datetime
from datetime import timedelta

today = date.today()
today_datetime = datetime.combine(today, datetime.min.time())


def run(batch_id, source_file_name, output_file_name, source_service_resources, delta=timedelta(days=14)):
    data_gen = DataGenerator()

    # load source file
    data_gen.load_source_file(source_file_name)


    data_gen.add_formula_column('Start',
                                lambda cv: "" if cv['Start'] == "" else (dateutil.parser.parse(cv['Start']) + timedelta(days=delta.days - 1)).replace(tzinfo=None))

    data_gen.add_formula_column('End',
                                lambda cv: "" if cv['End'] == "" else (dateutil.parser.parse(cv['End']) + timedelta(days=delta.days - 1)).replace(tzinfo=None))


    service_resources = data_gen.load_dataset("ServiceResources", source_service_resources, ['Id', 'External_ID__c']).dict('Id', 'External_ID__c')

    data_gen.add_map_column('Resource.External_Id__c', 'ResourceId', service_resources)

    data_gen.apply_transformations()

    data_gen.add_copy_column('CreatedDate__c', 'Start')

    data_gen.apply_transformations()

    data_gen.write(output_file_name, columns=[
        'External_ID__c',
        'Resource.External_Id__c',
        'CreatedDate__c',
        'Start',
        'End',
        'Type',
        #'State',
        #'Country',
        #'City'
    ])


if __name__ == "__main__":
    # execute only if running as a script
    run(datetime.now().strftime("%Y%m%d%-H%M%S%f"), 'data/output/ResourceAbsence.csv', 'data/output/ResourceAbsence.csv',
        'data/output/ServiceResource.csv')
