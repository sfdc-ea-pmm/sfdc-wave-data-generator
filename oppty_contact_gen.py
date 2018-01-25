import definitions

from data_generator import DataGenerator
from data_generator.formula import fake


def run(batch_id, source_file_name, output_file_name):
    data_gen = DataGenerator()

    # load source file
    account_columns = ['External_Id__c']
    data_gen.load_source_file(source_file_name, account_columns)

    data_gen.rename_column('External_Id__c', 'Account.External_Id__c')
    data_gen.add_formula_column('External_Id__c',
                                lambda cv: cv['Account.External_Id__c'].replace('W_Account', 'W_Contact'))

    data_gen.add_formula_column('FirstName', formula=fake.first_name)
    data_gen.add_formula_column('LastName', formula=fake.last_name)

    # add a UUID for each row that is created in this batch
    data_gen.add_constant_column('analyticsdemo_batch_id__c', batch_id)

    data_gen.apply_transformations()
    data_gen.write(output_file_name)


if __name__ == "__main__":
    # execute only if running as a script
    run(definitions.oppty_accounts, definitions.oppty_contacts)
