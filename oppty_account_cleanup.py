import definitions

from data_generator import DataGenerator


def run(source_file_name, output_file_name):
    data_gen = DataGenerator()

    # load source file
    source_columns = [
        'External_Id__c',
        'Name',
        'Owner.External_Id__c',
        'NumberOfEmployees',
        'AnnualRevenue',
        'AccountSource',
        'Type',
        'Industry',
        'BillingStreet',
        'BillingCity',
        'BillingState',
        'BillingCountry',
        'YearStarted',
        'Ownership',
        'Rating',
        'CreatedDate__c',
        'analyticsdemo_batch_id__c'
    ]
    data_gen.load_source_file(source_file_name, source_columns)

    data_gen.write(output_file_name)


if __name__ == "__main__":
    # execute only if running as a script
    run(definitions.oppty_accounts, definitions.oppty_accounts)
