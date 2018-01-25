import definitions

from data_generator import DataGenerator


def run(batch_id, source_file_name, output_file_name):
    data_gen = DataGenerator()

    # load source file
    source_columns = [
        'KnowledgeArticle.External_Id__c',
        'User.External_Id__c',
        'CreatedDate__c'
    ]
    data_gen.load_source_file(source_file_name, source_columns)

    data_gen.rename_column('KnowledgeArticle.External_Id__c', 'KCSArticle__ka.External_Id__c')
    data_gen.rename_column('User.External_Id__c', 'Owner.External_Id__c')

    data_gen.add_formula_column('External_Id__c', formula=lambda: 'W_KCSArticleVersion.' + str(data_gen.current_row + 1))

    data_gen.add_formula_column('ArticleNumber__c', lambda: data_gen.current_row + 1)

    data_gen.add_formula_column('PublishStatus__c', ['Archived', 'Online'])

    data_gen.add_constant_column('IsLatestVersion__c', 'true')
    data_gen.add_constant_column('IsVisibleInApp__c', 'true')
    data_gen.add_constant_column('IsVisibleInCsp__c', 'true')
    data_gen.add_constant_column('IsVisibleInPkb__c', 'true')
    data_gen.add_constant_column('IsVisibleInPrm__c', 'true')

    data_gen.add_constant_column('VersionNumber__c', '1')
    data_gen.add_constant_column('Language__c', 'en_US')

    titles = [
        "Health",
        "Computers",
        "Music",
        "Tools",
        "Home",
        "Outdoors",
        "Jewelery",
        "Toys",
        "Grocery",
        "Clothing",
        "Games",
        "Automotive",
        "Beauty",
        "Garden",
        "Books",
        "Industrial",
        "Baby",
        "Kids",
        "Movies",
        "Sports",
        "Shoes",
        "Electronics"
    ]
    data_gen.add_formula_column('Title__c', titles)

    # add a UUID for each row that is created in this batch
    data_gen.add_constant_column('analyticsdemo_batch_id__c', batch_id)

    # apply transformations and write file
    data_gen.apply_transformations()

    output_columns = [
        'External_Id__c',
        'ArticleNumber__c',
        'CreatedDate__c',
        'Owner.External_Id__c',
        'PublishStatus__c',
        'IsLatestVersion__c',
        'IsVisibleInApp__c',
        'IsVisibleInCsp__c',
        'IsVisibleInPkb__c',
        'IsVisibleInPrm__c',
        'KCSArticle__ka.External_Id__c',
        'Title__c',
        'VersionNumber__c',
        'Language__c',
        'analyticsdemo_batch_id__c'
    ]
    data_gen.write(output_file_name, output_columns)


if __name__ == "__main__":
    # execute only if running as a script
    run(definitions.case_articles, definitions.case_knowledge_article_versions)
