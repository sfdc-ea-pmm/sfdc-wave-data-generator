import definitions

from data_generator import DataGenerator
from numpy.random import choice


def run(batch_id, source_file_name, output_file_name):
    data_gen = DataGenerator()

    # load source file
    source_columns = [
        'External_Id__c',
        'Owner.External_Id__c',
        'CreatedDate__c'
    ]
    data_gen.load_source_file(source_file_name, source_columns)

    data_gen.rename_column('External_Id__c', 'Case.External_Id__c')
    data_gen.rename_column('Owner.External_Id__c', 'User.External_Id__c')

    # todo one case article per case? at most 1? distribution?
    data_gen.duplicate_rows(duplication_factor=lambda: choice([0, 1], p=[.75, .25]))

    data_gen.add_formula_column('External_Id__c', formula=lambda: 'W_CaseArticle.' + str(data_gen.current_row + 1))
    data_gen.add_formula_column('KnowledgeArticle.External_Id__c',
                                formula=lambda: 'W_KCSArticle.' + str(data_gen.current_row + 1))

    data_gen.add_constant_column('ArticleVersionNumber__c', 1)

    data_gen.add_constant_column('IsSharedByEmail__c', ['true', 'false'])

    # add a UUID for each row that is created in this batch
    data_gen.add_constant_column('analyticsdemo_batch_id__c', batch_id)

    # apply transformations and write file
    data_gen.apply_transformations()

    output_columns = [
        'External_Id__c',
        'User.External_Id__c',
        'ArticleVersionNumber__c',
        'CreatedDate__c',
        'KnowledgeArticle.External_Id__c',
        'IsSharedByEmail__c',
        'Case.External_Id__c',
        'analyticsdemo_batch_id__c'
    ]
    data_gen.write(output_file_name, output_columns)


if __name__ == "__main__":
    # execute only if running as a script
    run(definitions.case_data, definitions.case_articles)
