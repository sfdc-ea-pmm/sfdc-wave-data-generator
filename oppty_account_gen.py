import dateutil.parser
import definitions
import uuid

from data_generator import DataGenerator
from data_generator.formula import account
from data_generator.formula import fake
from numpy.random import choice
from numpy.random import randint


def run(batch_id, source_file_name, output_file_name):
    data_gen = DataGenerator()


    # load source file
    source_columns = ['AccountExternalId__c', 'AccountName__c']
    data_gen.load_source_file(source_file_name, source_columns)


    # rename columns
    data_gen.rename_column('AccountExternalId__c', 'External_Id__c')
    data_gen.rename_column('AccountName__c', 'Name')


    # filter out duplicate data
    data_gen.unique()


    # load shape data as dataset
    shape_columns = [
        'AccountExternalId__c',
        'AccountAnnualRevenue__c',
        'AccountNumberOfEmployees__c',
        'AccountBookings__c',
        'Region__c',
        'Owner.External_Id__c',
        'CloseDate',
        'CreatedDate__c']
    shape_dataset = data_gen.load_dataset('shape', source_file_name, shape_columns)


    # build map of account values
    shape_account_map = shape_dataset.group_by('AccountExternalId__c')


    # helper method to get shape data related to an account
    def get_shape_data(column_values, shape_column_name):
        return shape_account_map.get(column_values['External_Id__c'])[0].get(shape_column_name)


    # generate owner
    def owner_formula(column_values):
        return get_shape_data(column_values, 'Owner.External_Id__c')
    data_gen.add_formula_column('Owner.External_Id__c', owner_formula)


    # update number employees based on shape data
    def employees_formula(column_values):
        employees = get_shape_data(column_values, 'AccountNumberOfEmployees__c')
        return randint(*account.client_size_employees_bands[employees])
    data_gen.add_formula_column('NumberOfEmployees', employees_formula)


    # update annual revenue based on shape data
    def revenue_formula(column_values):
        revenue = get_shape_data(column_values, 'AccountAnnualRevenue__c')
        return 1000 * randint(*account.client_size_rev_bands[revenue])
    data_gen.add_formula_column('AnnualRevenue', revenue_formula)


    # generate account source
    data_gen.add_formula_column('AccountSource', formula=account.account_source)


    # update type based on shape data
    def type_formula(column_values):
        return get_shape_data(column_values, 'AccountAnnualRevenue__c')
    data_gen.add_formula_column('Type', type_formula)


    # generate industry
    data_gen.add_formula_column('Industry', formula=account.account_industry)


    # generate billing street
    data_gen.add_formula_column('BillingStreet', formula=lambda: fake.building_number() + ' ' + fake.street_name())


    # generate billing city
    data_gen.add_formula_column('BillingCity', formula=fake.city)


    # update billing state based on shape data
    def state_formula(column_values):
        region = get_shape_data(column_values, 'Region__c')
        return choice(account.region_state_map[region])
    data_gen.add_formula_column('BillingState', state_formula)


    # generate billing country
    data_gen.add_constant_column('BillingCountry', 'USA')


    # generate year started
    data_gen.add_formula_column('YearStarted', formula=account.account_year_started)


    # generate ownership
    data_gen.add_formula_column('Ownership', formula=account.account_ownership)


    # generate rating
    data_gen.add_formula_column('Rating', formula=account.account_rating)


    # generate earliest created date
    def create_date_formula(column_values):
        opptys = shape_account_map.get(column_values['External_Id__c'])
        create_dates = [dateutil.parser.parse(oppty['CreatedDate__c']) for oppty in opptys]
        create_dates.sort()
        return create_dates[0]
    data_gen.add_formula_column('CreatedDate__c', create_date_formula)


    # generate earliest close date
    def close_date_formula(column_values):
        opptys = shape_account_map.get(column_values['External_Id__c'])
        close_dates = [dateutil.parser.parse(oppty['CloseDate']).date() for oppty in opptys]
        close_dates.sort()
        return close_dates[0]
    data_gen.add_formula_column('OpportunityCloseDate__c', close_date_formula)

    # add a UUID for each row that is created in this batch
    data_gen.add_constant_column('analyticsdemo_batch_id__c', batch_id)

    # apply transformations and write file
    data_gen.apply_transformations()
    data_gen.write(output_file_name)


if __name__ == "__main__":
    # execute only if running as a script
    run(definitions.oppty_shape, definitions.oppty_accounts)
