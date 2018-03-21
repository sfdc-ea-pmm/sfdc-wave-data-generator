import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from data_generator import DataGenerator


def run(batch_id, source_file_name, output_file_name):
    data_gen = DataGenerator()

    # load source file
    source_columns = [
        'KnowledgeArticle.External_Id__c'
    ]
    data_gen.load_source_file(source_file_name, source_columns)

    data_gen.rename_column('KnowledgeArticle.External_Id__c', 'Parent.External_Id__c')

    data_gen.add_formula_column('External_Id__c', formula=lambda: 'W_KCSArticle_DCS.' + str(data_gen.current_row + 1))

    data_gen.add_constant_column('DataCategoryGroupName__c', 'All')

    data_gen.add_constant_column('DataCategoryName__c', 'All')

    # add a UUID for each row that is created in this batch
    data_gen.add_constant_column('analyticsdemo_batch_id__c', batch_id)

    # apply transformations and write file
    data_gen.apply_transformations()

    output_columns = [
        'External_Id__c',
        'Parent.External_Id__c',
        'DataCategoryGroupName__c',
        'DataCategoryName__c',
        'analyticsdemo_batch_id__c'
    ]
    data_gen.write(output_file_name, output_columns)


if __name__ == "__main__":
    # execute only if running as a script
    run('1', 'data/output/CaseArticle.csv', 'data/output/KCSArticle_DataCategorySelection.csv')
