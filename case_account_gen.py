import definitions

from data_generator import DataGenerator
from data_generator.formula import account
from data_generator.formula import fake
from numpy.random import normal


def run(batch_id, source_file_name, output_file_name):
    data_gen = DataGenerator()


    # load source file
    source_columns = ['Account.External_Id__c']
    data_gen.load_source_file(source_file_name, source_columns)


    # rename columns
    data_gen.rename_column('Account.External_Id__c', 'External_Id__c')

    # filter out duplicate data
    data_gen.unique()

    # load shape data as dataset
    shape_columns = [
        'Account.External_Id__c',
        'Owner.External_Id__c'
    ]
    shape_dataset = data_gen.load_dataset('shape', source_file_name, shape_columns)


    # build map of account values
    shape_account_map = shape_dataset.group_by('Account.External_Id__c')


    # helper method to get shape data related to an account
    def get_shape_data(column_values, shape_column_name):
        return shape_account_map.get(column_values['External_Id__c'])[0].get(shape_column_name)

    # generate name
    data_gen.add_formula_column('Name', formula=account.account_name)

    # generate owner
    def owner_formula(column_values):
        return get_shape_data(column_values, 'Owner.External_Id__c')
    data_gen.add_formula_column('Owner.External_Id__c', owner_formula)


    # generate account source
    data_gen.add_formula_column('AccountSource', formula=account.account_source)


    # generate annual revenue
    data_gen.add_formula_column('AnnualRevenue', lambda: 1000 * int(normal(2800, 600)))


    # generate billing street
    data_gen.add_formula_column('BillingStreet', formula=lambda: fake.building_number() + ' ' + fake.street_name())


    # generate billing city
    data_gen.add_formula_column('BillingCity', formula=fake.city)


    # generate billing state
    data_gen.add_formula_column('BillingState', formula=fake.state_abbr)


    # generate billing postal code
    data_gen.add_formula_column('BillingPostalCode', formula=fake.zipcode)


    # generate billing country
    data_gen.add_constant_column('BillingCountry', 'USA')


    # generate industry
    data_gen.add_formula_column('Industry', formula=account.account_industry)


    # generate number employees
    data_gen.add_formula_column('NumberOfEmployees', lambda: int(normal(150, 35)))


    # generate ownership
    data_gen.add_formula_column('Ownership', formula=account.account_ownership)


    # generate phone
    data_gen.add_formula_column('Phone', formula=fake.phone_number)


    # generate rating
    data_gen.add_formula_column('Rating', formula=account.account_rating)


    # generate type
    data_gen.add_formula_column('Type', formula=account.account_type)


    # generate year started
    data_gen.add_formula_column('YearStarted', formula=account.account_year_started)

    # add a UUID for each row that is created in this batch
    data_gen.add_constant_column('analyticsdemo_batch_id__c', batch_id)

    # apply transformations and write file
    data_gen.apply_transformations()
    data_gen.write(output_file_name)


if __name__ == "__main__":
    # execute only if running as a script
    run(definitions.case_data, definitions.case_accounts)
