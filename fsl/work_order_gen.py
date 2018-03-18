import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from data_generator import DataGenerator
from datetime import date
from datetime import datetime

today = date.today()
today_datetime = datetime.combine(today, datetime.min.time())


def run(batch_id, source_file_name, output_file_name, source_cases, source_accounts, source_work_types, reference_datetime=today_datetime):
    data_gen = DataGenerator()

    # load source file
    data_gen.load_source_file(source_file_name)

    data_gen.add_constant_column('CreatedDate__c', reference_datetime.isoformat(sep=' '))

    cases = data_gen.load_dataset("Cases", source_cases, ['Id', 'External_Id__c']).dict('Id', 'External_Id__c')
    data_gen.add_map_column('Case.External_Id__c', 'CaseId', cases)

    accounts = data_gen.load_dataset("Accounts", source_accounts, ['Id', 'External_Id__c']).dict('Id', 'External_Id__c')
    data_gen.add_map_column('Account.External_Id__c', 'AccountId', accounts)

    work_types = data_gen.load_dataset("WorkTypes", source_work_types, ['Id', 'External_Id__c']).dict('Id', 'External_Id__c')
    data_gen.add_map_column('WorkType.External_Id__c', 'WorkTypeId', work_types)

    data_gen.add_constant_column('Pricebook2.Name', 'Standard Price Book')

    data_gen.apply_transformations()

    data_gen.write(output_file_name, columns=[
        'External_Id__c',
        'CreatedDate__c',
        'Status',
        'Pricebook2.Name',
        'Priority',
        'Case.External_Id__c',
        'Account.External_Id__c',
        'WorkType.External_Id__c'
    ])


if __name__ == "__main__":
    # execute only if running as a script
    run(datetime.now().strftime("%Y%m%d%-H%M%S%f"), 'data/output/WorkOrder.csv', 'data/output/WorkOrder.csv',
        'data/output/Case.csv', 'data/output/Account.csv', 'data/output/WorkType.csv')
