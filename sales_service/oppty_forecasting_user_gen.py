from data_generator import DataGenerator

def run(batch_id, source_file_name, output_file_name):
    data_gen = DataGenerator()

    # load source file
    source_columns = ['External_Id__c','UserRole.Name']
    data_gen.load_source_file(source_file_name, source_columns)

    # data_gen.filter(lambda cv: 'RVP' in cv['UserRole.Name']) # commented out because using shape file from service with no RVP value in UserRole.Name
    data_gen.filter(lambda cv: 'CSM' in cv['UserRole.Name']) # comes from Service

    data_gen.rename_column('External_Id__c', 'ForecastUser.External_Id__c')

    data_gen.rename_column('UserRole.Name', 'Name')

    # add a UUID for each row that is created in this batch
    data_gen.add_constant_column('analyticsdemo_batch_id__c', batch_id)

    # apply transformations and write file
    data_gen.apply_transformations()
    data_gen.write(output_file_name, ['Name','ForecastUser.External_Id__c','analyticsdemo_batch_id__c'])