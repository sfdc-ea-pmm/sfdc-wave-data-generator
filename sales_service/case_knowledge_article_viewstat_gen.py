import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


from data_generator import DataGenerator
from random import uniform
from random import randint


def run(batch_id, source_file_name, output_file_name):
    data_gen = DataGenerator()

    # load source file
    source_columns = [
        'KnowledgeArticle.External_Id__c',
        'User.External_Id__c',
        'CreatedDate__c'
    ]
    data_gen.load_source_file(source_file_name, source_columns)

    data_gen.rename_column('KnowledgeArticle.External_Id__c', 'Parent.External_Id__c')
    data_gen.rename_column('User.External_Id__c', 'Owner.External_Id__c')

    data_gen.add_formula_column('External_Id__c', formula=lambda: 'W_KCSArticle_ViewStat.' + str(data_gen.current_row + 1))

    channels = [
        'App',
        'Desktop Site',
        'Mobile Site'
    ]
    data_gen.add_formula_column('Channel__c', channels)

    data_gen.add_formula_column('ViewCount__c', formula=lambda: randint(1, 100))

    data_gen.add_formula_column('NormalizedScore__c', formula=lambda: round(uniform(1, 10), 3))
    # add a UUID for each row that is created in this batch
    data_gen.add_constant_column('analyticsdemo_batch_id__c', batch_id)
    # apply transformations and write file
    data_gen.apply_transformations()

    output_columns = [
        'External_Id__c',
        'Channel__c',
        'Parent.External_Id__c',
        'ViewCount__c',
        'NormalizedScore__c',
        'analyticsdemo_batch_id__c'
    ]
    data_gen.write(output_file_name, output_columns)


if __name__ == "__main__":
    # execute only if running as a script
    run('1', 'data/output/CaseArticle.csv', 'data/output/KCSArticle_ViewStat.csv')
