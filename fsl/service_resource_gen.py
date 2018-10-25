import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from data_generator import DataGenerator
from datetime import datetime


def run(batch_id, source_file_name, output_file_name, source_users):
    data_gen = DataGenerator()

    # load source file
    data_gen.load_source_file(source_file_name)

    users = data_gen.load_dataset("Users", source_users, ['Id', 'External_ID__c']).dict('Id', 'External_ID__c')

    data_gen.add_map_column('RelatedRecord.External_Id__c', 'RelatedRecordId', users)

    data_gen.apply_transformations()

    data_gen.write(output_file_name, columns=[
        'External_ID__c',
        'Name',
        'IsActive',
        'RelatedRecord.External_Id__c'
    ])


if __name__ == "__main__":
    # execute only if running as a script
    run(datetime.now().strftime("%Y%m%d%-H%M%S%f"), 'data/output/ServiceResource.csv', 'data/output/ServiceResource.csv',
        'data/output/User.csv')