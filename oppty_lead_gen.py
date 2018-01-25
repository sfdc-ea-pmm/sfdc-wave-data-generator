import dateutil.parser
import definitions

from data_generator import DataGenerator
from data_generator.formula import fake
from data_generator.formula import lead
from datetime import timedelta
from numpy.random import choice
from numpy.random import randint


def run(batch_id, source_file_name, output_file_name, accounts_file_name, contacts_file_name):
    data_gen = DataGenerator()


    # load source file
    source_columns = [
        'External_Id__c',
        'AccountExternalId__c',
        'Owner.External_Id__c',
        'LeadSource',
        'CloseDate',
        'CreatedDate__c'
    ]
    data_gen.load_source_file(source_file_name, source_columns)

    # load accounts as dataset
    account_columns = [
        'External_Id__c',
        'Name',
        'BillingState',
        'Industry'
    ]
    account_dataset = data_gen.load_dataset('accounts', accounts_file_name, account_columns)
    accounts_by_id = account_dataset.group_by('External_Id__c')


    # load contacts as dataset
    contact_columns = [
        'External_Id__c',
        'FirstName',
        'LastName'
    ]
    contact_dataset = data_gen.load_dataset('contacts', contacts_file_name, contact_columns)
    contacts_by_id = contact_dataset.group_by('External_Id__c')


    # helper method to get account data
    def get_account_data(column_values, account_column_name):
        return accounts_by_id.get(column_values['ConvertedAccount.External_Id__c'])[0].get(account_column_name)


    # helper method to get contact data
    def get_contact_data(column_values, contact_column_name):
        return contacts_by_id.get(column_values['ConvertedContact.External_Id__c'])[0].get(contact_column_name)


    # rename columns
    data_gen.rename_column('External_Id__c', 'ConvertedOpportunity.External_Id__c')
    data_gen.rename_column('AccountExternalId__c', 'ConvertedAccount.External_Id__c')
    data_gen.rename_column('CloseDate', 'ConvertedDate__c')


    # generate converted lead at a random ratio
    data_gen.duplicate_rows(duplication_factor=lambda: choice([0, 1], p=[.75, .25]))


    # generate id
    data_gen.add_formula_column('External_Id__c', formula=lambda: 'W_Lead.' + str(data_gen.current_row + 1))


    # generate create date
    def create_date_formula(column_values):
        oppty_create_date = dateutil.parser.parse(column_values['CreatedDate__c'])
        return oppty_create_date - timedelta(days=randint(0, 45))
    data_gen.add_formula_column('CreatedDate__c', create_date_formula)


    # generate status
    data_gen.add_formula_column('Status', formula=lead.lead_status)


    # generate status
    data_gen.add_map_column('IsConverted', 'Status', {
        'Qualified - Convert': 'true',
        None: 'false'
    })


    # generate opportunity
    data_gen.add_map_column('ConvertedOpportunity.External_Id__c', 'Status', {
        'Qualified - Convert': lambda cv: cv['ConvertedOpportunity.External_Id__c'],
        None: ''
    })


    # generate account
    data_gen.add_map_column('ConvertedAccount.External_Id__c', 'Status', {
        'Qualified - Convert': lambda cv: cv['ConvertedAccount.External_Id__c'],
        None: ''
    })


    # generate contact
    data_gen.add_map_column('ConvertedContact.External_Id__c', 'Status', {
        'Qualified - Convert': lambda cv: cv['ConvertedAccount.External_Id__c'].replace('W_Account', 'W_Contact'),
        None: ''
    })


    # generate converted date
    data_gen.add_map_column('ConvertedDate__c', 'Status', {
        'Qualified - Convert': lambda cv: cv['ConvertedDate__c'],
        None: ''
    })


    # generate name
    data_gen.add_map_column('FirstName', 'Status', {
        'Qualified - Convert': lambda cv: get_contact_data(cv, 'FirstName'),
        None: lambda: fake.first_name()
    })


    data_gen.add_map_column('LastName', 'Status', {
        'Qualified - Convert': lambda cv: get_contact_data(cv, 'LastName'),
        None: lambda: fake.last_name()
    })


    # generate company
    data_gen.add_map_column('Company', 'Status', {
        'Qualified - Convert': lambda cv: get_account_data(cv, 'Name'),
        None: 'Not Applicable'
    })


    # generate industry
    data_gen.add_map_column('Industry', 'Status', {
        'Qualified - Convert': lambda cv: get_account_data(cv, 'Industry'),
        None: ''
    })


    # generate state
    data_gen.add_map_column('State', 'Status', {
        'Qualified - Convert': lambda cv: get_account_data(cv, 'BillingState'),
        None: ''
    })


    # generate is unread by owner
    data_gen.add_map_column('IsUnreadByOwner', 'Status', {
        'Qualified - Convert': 'false',
        None: lead.lead_is_unread_by_owner
    })

    # generate rating
    data_gen.add_formula_column('Rating', formula=lead.lead_rating)

    # add a UUID for each row that is created in this batch
    data_gen.add_constant_column('analyticsdemo_batch_id__c', batch_id)

    # apply transformations and write file
    data_gen.apply_transformations()
    data_gen.write(output_file_name)


if __name__ == "__main__":
    # execute only if running as a script
    run(definitions.oppty_shape, definitions.oppty_leads, definitions.oppty_accounts, definitions.oppty_contacts)
