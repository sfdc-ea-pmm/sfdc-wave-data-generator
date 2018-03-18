import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from data_generator import DataGenerator
from datetime import datetime


def run(batch_id, source_file_name, output_file_name, source_accounts):
    data_gen = DataGenerator()

    # load source file
    data_gen.load_source_file(source_file_name)

    accounts = data_gen.load_dataset("Accounts", source_accounts, ['Id', 'External_Id__c']).dict('Id', 'External_Id__c')

    data_gen.add_map_column('Account.External_Id__c', 'AccountId', accounts)

    data_gen.apply_transformations()

    data_gen.write(output_file_name, columns=[
        'External_Id__c',
        'Account.External_Id__c',
        'Subject'
    ])


if __name__ == "__main__":
    # execute only if running as a script
    run(datetime.now().strftime("%Y%m%d%-H%M%S%f"), 'data/output/Case.csv', 'data/output/Case.csv',
        'data/output/Account.csv')
