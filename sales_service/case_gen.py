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


def run(batch_id, source_file_name, output_file_name, filter_function=None):
    data_gen = DataGenerator()

    # load source file
    data_gen.load_source_file(source_file_name)

    data_gen.add_formula_column('Contact.External_Id__c',
                                lambda cv: cv['Account.External_Id__c'].replace('W_Services_Account', 'W_Services_Contact'))

    # add a UUID for each row that is created in this batch
    data_gen.add_constant_column('analyticsdemo_batch_id__c', batch_id)


    data_gen.apply_transformations()

    if filter_function:
        data_gen.filter(filter_function)

    output_columns = [
        'External_Id__c',
        'Owner.External_Id__c',
        'Account.External_Id__c',
        'Contact.External_Id__c',
        'CreatedDate__c',
        'ClosedDate__c',
        'LastActivityDate__c',
        'Origin',
        'Tier',
        'Product_Family_KB__c',
        'Priority',
        'SLA',
        'Reason',
        'Type_of_Support__c',
        'CSAT__c',
        'Status',
        'First_Contact_Close__c',
        'Time_Open__c',
        'Team__c',
        'close_date_offset',
        'Offer_Voucher__c',
        'Send_FieldService__c',
        'IsEscalated',
        'MilestoneStatus__c',
        'analyticsdemo_batch_id__c'
    ]
    data_gen.write(output_file_name, output_columns)


if __name__ == "__main__":
    # execute only if running as a script
    cutoff_date = today_datetime - timedelta(days=365 * 2)
    run('1', 'data/output/CaseShape.csv', 'data/output/Case.csv',
        filter_function=lambda cv: dateutil.parser.parse(cv['CreatedDate__c']) >= cutoff_date)
