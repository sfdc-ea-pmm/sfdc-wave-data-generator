import dateutil.parser
import definitions

from data_generator import DataGenerator


def run(batch_id, source_file_name, output_file_name):
    data_gen = DataGenerator()

    # load source file
    source_columns = [
        'External_Id__c',
        'AccountExternalId__c',
        'Owner.External_Id__c',
        'Name',
        'Amount',
        'StageName',
        'LeadSource',
        'Type',
        'ForecastCategoryName',
        'CloseDate',
        'CreatedDate__c',
        'RecordType.DeveloperName',
        'LastActivityDate__c',
        'Product2Name__c',
        'Product2Family__c',
        'Region__c',
        'TimeToClose__c',
        'SalesStageCount__c',
        'AccountAnnualRevenue__c',
        'AccountNumberOfEmployees__c',
        'AccountBookings__c',
        'Competitor__c',
        'DealSizeCategory__c',
        'Exec_Meeting__c',
        'Interactive_Demo__c'
    ]
    data_gen.load_source_file(source_file_name, source_columns)

    data_gen.rename_column('AccountExternalId__c', 'Account.External_Id__c')
    data_gen.rename_column('CreatedDate__c', 'DateTimeCreated__c')

    data_gen.add_formula_column('LastModifiedDate__c',
                                lambda cv: dateutil.parser.parse(cv['LastActivityDate__c']))

    # add a UUID for each row that is created in this batch
    data_gen.add_constant_column('analyticsdemo_batch_id__c', batch_id)

    data_gen.apply_transformations()

    data_gen.write(output_file_name)


if __name__ == "__main__":
    # execute only if running as a script
    run(definitions.oppty_shape, definitions.oppty)
