import definitions

from data_generator import DataGenerator
from random import randint


def run(batch_id, source_file_name, product_output_file_name, pricebook_output_file_name):
    data_gen = DataGenerator()

    # load source file
    source_columns = ['Product2Name__c', 'Product2Family__c']
    data_gen.load_source_file(source_file_name, source_columns)

    # rename columns
    data_gen.rename_column('Product2Name__c', 'Name')
    data_gen.rename_column('Product2Family__c', 'Family')

    # filter out duplicate data
    data_gen.unique()

    # generate product code
    data_gen.add_formula_column('External_Id__c', formula=lambda: 'W_Product.' + str(data_gen.current_row + 1))

    data_gen.add_copy_column('ProductCode', 'External_Id__c')

    # apply transformations and write Product2 file
    data_gen.apply_transformations()
    data_gen.write(product_output_file_name)

    # generate pricebook entry code
    data_gen.add_formula_column('External_Id__c', formula=lambda: 'W_PricebookEntry.' + str(data_gen.current_row + 1))

    # generate product id reference
    data_gen.add_copy_column('Product2.External_Id__c', 'ProductCode')

    # get map of product names to opportunity amounts
    shape_dataset = data_gen.load_dataset('shape', source_file_name, ['Product2Name__c', 'Amount'])
    amounts_by_product_name = shape_dataset.group_by('Product2Name__c')

    # generate unit price
    def unit_price_formula(column_values):
        # find average opportunity amount for product
        product_name = column_values['Name']
        amounts = amounts_by_product_name[product_name]
        avg_amount = 0
        count = 0
        for amount in amounts:
            amount = int(amount['Amount'])
            if amount > 0:
                count += 1
                avg_amount += amount
        avg_amount = avg_amount / count
        random_quantity = randint(1, 100)
        return int(avg_amount / random_quantity)
    data_gen.add_formula_column('UnitPrice', formula=unit_price_formula)

    data_gen.add_constant_column('IsActive', 'true')
    data_gen.add_constant_column('Pricebook2.Name', 'Standard Price Book')

    # add a UUID for each row that is created in this batch
    data_gen.add_constant_column('analyticsdemo_batch_id__c', batch_id)

    # apply transformations and write PricebookEntry file
    data_gen.apply_transformations()

    data_gen.write(pricebook_output_file_name,
                   ['External_Id__c', 'Product2.External_Id__c', 'IsActive', 'Pricebook2.Name', 'UnitPrice', 'analyticsdemo_batch_id__c'])

if __name__ == "__main__":
    # execute only if running as a script
    run(definitions.oppty_shape, definitions.oppty_products, definitions.oppty_pricebook)
