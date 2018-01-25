import dateutil.parser
import definitions

from data_generator import DataGenerator
from datetime import timedelta
from numpy.random import randint


def run(batch_id, source_file_name, output_file_name):
    data_gen = DataGenerator()

    # load source file
    source_columns = [
        'KnowledgeArticle.External_Id__c',
        'CreatedDate__c'
    ]
    data_gen.load_source_file(source_file_name, source_columns)

    data_gen.rename_column('KnowledgeArticle.External_Id__c', 'External_Id__c')

    data_gen.add_formula_column('ArticleNumber__c', lambda: data_gen.current_row + 1)

    data_gen.add_formula_column('CaseAssociationCount__c', lambda: randint(1, 6))

    def first_published_date_formula(column_values):
        create_date = dateutil.parser.parse(column_values['CreatedDate__c'])
        return (create_date + timedelta(days=randint(1, 10))).isoformat(sep=' ')
    data_gen.add_formula_column('FirstPublishedDate__c', formula=first_published_date_formula)

    def last_published_date_formula(column_values):
        first_publised_date = dateutil.parser.parse(column_values['FirstPublishedDate__c'])
        return (first_publised_date + timedelta(days=randint(1, 10))).isoformat(sep=' ')
    data_gen.add_formula_column('LastPublishedDate__c', formula=last_published_date_formula)

    # add a UUID for each row that is created in this batch
    data_gen.add_constant_column('analyticsdemo_batch_id__c', batch_id)

    # apply transformations and write file
    data_gen.apply_transformations()

    output_columns = [
        'ArticleNumber__c',
        'External_Id__c',
        'CaseAssociationCount__c',
        'CreatedDate__c',
        'FirstPublishedDate__c',
        'LastPublishedDate__c',
        'analyticsdemo_batch_id__c'
    ]
    data_gen.write(output_file_name, output_columns)


if __name__ == "__main__":
    # execute only if running as a script
    run(definitions.case_articles, definitions.case_knowledge_articles)
