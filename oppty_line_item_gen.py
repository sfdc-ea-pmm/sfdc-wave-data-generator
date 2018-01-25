import definitions

from data_generator import DataGenerator
from math import ceil


def run(batch_id, source_file_name, output_file_name, products_file_name, pricebook_file_name):
    data_gen = DataGenerator()

    # load source file
    source_columns = ['External_Id__c', 'Product2Name__c', 'Amount']
    data_gen.load_source_file(source_file_name, source_columns)

    # load datasets
    products = data_gen.load_dataset('products', products_file_name)
    products_by_name = products.group_by('Name')

    pricebook = data_gen.load_dataset('pricebook', pricebook_file_name)
    pricebook_by_product = pricebook.group_by('Product2.External_Id__c')

    # rename columns
    data_gen.rename_column('External_Id__c', 'Opportunity.External_Id__c')
    data_gen.rename_column('Amount', 'TotalPrice')

    data_gen.add_formula_column('External_Id__c', formula=lambda: 'W_OpportunityLineItem.' + str(data_gen.current_row + 1))

    # transform product name to code
    data_gen.add_formula_column('ProductCode', lambda cv: products_by_name[cv['Product2Name__c']][0]['ProductCode'])

    # generate product reference id
    data_gen.add_formula_column('Product2.External_Id__c',
                                lambda cv: products_by_name[cv['Product2Name__c']][0]['External_Id__c'])

    # generate list price
    data_gen.add_formula_column('ListPrice', lambda cv: pricebook_by_product[cv['ProductCode']][0]['UnitPrice'])

    # generate pricebook reference id
    data_gen.add_formula_column('PricebookEntry.External_Id__c',
                                lambda cv: pricebook_by_product[cv['ProductCode']][0]['External_Id__c'])

    # generate quantity
    def quanity_formula(column_values):
        total_price = int(column_values['TotalPrice'])
        list_price = int(column_values['ListPrice'])
        quantity = total_price / list_price
        if quantity <= 0:
            quantity = 1
        return ceil(quantity)
    data_gen.add_formula_column('Quantity', quanity_formula)

    # add a UUID for each row that is created in this batch
    data_gen.add_constant_column('analyticsdemo_batch_id__c', batch_id)

    # apply transformations and write file
    data_gen.apply_transformations()

    output_columns = [
        'External_Id__c',
        'Opportunity.External_Id__c',
        'TotalPrice',
        'PricebookEntry.External_Id__c',
        'Quantity',
        'analyticsdemo_batch_id__c'
    ]
    data_gen.write(output_file_name, output_columns)

if __name__ == "__main__":
    # execute only if running as a script
    run(definitions.oppty_shape, definitions.oppty_line_item, definitions.oppty_products,
        definitions.oppty_pricebook)
