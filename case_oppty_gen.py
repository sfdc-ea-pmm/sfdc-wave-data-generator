import dateutil.parser
import definitions

from data_generator import DataGenerator
from datetime import timedelta
from numpy.random import choice
from numpy.random import normal
from numpy.random import randint


def run(batch_id, source_file_name, output_file_name, shape_file_name):
    data_gen = DataGenerator()

    # load source file
    source_columns = ['External_Id__c', 'Owner.External_Id__c']
    data_gen.load_source_file(source_file_name, source_columns)

    data_gen.unique()

    # rename columns
    data_gen.rename_column('External_Id__c', 'Account.External_Id__c')

    data_gen.add_formula_column('External_Id__c', lambda: 'W_Services_Opportunity.' + str(data_gen.current_row + 1))

    stages = [
        'Qualification',
        'Needs Analysis',
        'Proposal/Quote',
        'Negotiation',
        'Closed Won',
        'Closed Lost'
    ]
    data_gen.add_formula_column('StageName', lambda: choice(stages, p=[.25, .20, .15, .10, .15, .15]))

    types = [
        'New Business',
        'Add-On Business',
        'Services',
        'Renewal'
    ]
    data_gen.add_formula_column('Type', lambda: choice(types, p=[.45, .27, .18, .10]))

    products = [
        "GC20002",
        "GC5000 series",
        "GC10001",
        "GC50000",
        "GC1000 series"
    ]
    data_gen.add_formula_column('Products__c', products)

    data_gen.add_formula_column('Amount', lambda: 1000 * int(normal(1400, 350)))

    data_gen.add_formula_column('Name', lambda cv: 'New Opportunity [' + str(data_gen.current_row + 1) + ']')


    # load shape data as dataset
    shape_columns = [
        'Account.External_Id__c',
        'CreatedDate__c',
        'LastActivityDate__c']
    shape_dataset = data_gen.load_dataset('shape', shape_file_name, shape_columns)

    # build map of account values
    shape_account_map = shape_dataset.group_by('Account.External_Id__c')

    # generate earliest created date
    def create_date_formula(column_values):
        accounts = shape_account_map.get(column_values['Account.External_Id__c'])
        create_dates = [dateutil.parser.parse(account['CreatedDate__c']) for account in accounts]
        create_dates.sort()
        return (create_dates[0] - timedelta(days=randint(1, 45))).isoformat(sep=' ')
    data_gen.add_formula_column('DateTimeCreated__c', create_date_formula)

    # generate last activity date
    def last_activity_date_formula(column_values):
        accounts = shape_account_map.get(column_values['Account.External_Id__c'])
        activity_dates = [dateutil.parser.parse(account['LastActivityDate__c']) for account in accounts]
        activity_dates.sort(reverse=True)
        return activity_dates[0].isoformat(sep=' ')
    data_gen.add_formula_column('LastActivityDate__c', last_activity_date_formula)

    data_gen.add_copy_column('CloseDate', 'DateTimeCreated__c')

    # add a UUID for each row that is created in this batch
    data_gen.add_constant_column('analyticsdemo_batch_id__c', batch_id)

    # apply transformations and write file
    data_gen.apply_transformations()

    output_columns = [
        'External_Id__c',
        'Owner.External_Id__c',
        'Account.External_Id__c',
        'DateTimeCreated__c',
        'CloseDate',
        'LastActivityDate__c',
        'Name',
        'Products__c',
        'StageName',
        'Amount',
        'Type',
        'analyticsdemo_batch_id__c'
    ]
    data_gen.write(output_file_name, output_columns)

if __name__ == "__main__":
    # execute only if running as a script
    run(definitions.case_accounts, definitions.case_oppty, definitions.case_shape)
