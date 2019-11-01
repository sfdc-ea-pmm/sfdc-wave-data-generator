import mfg_linker.definitions as definitions
import dateutil.parser
import copy

from data_generator import DataGenerator
from datetime import date
from datetime import datetime
from datetime import timedelta
from math import floor, ceil
from numpy.random import choice

today = date.today()
today_datetime = datetime.combine(today, datetime.min.time())

def dropId(input_file_with_id, output_file_without_id):
    """Drops Id columns from the file if any.

    Parameters
    ----------
    input_file_with_id : str
        The name of the file with Id column, including the path.        
    output_file_without_id : str
        The file name (including path) of the CSV file without Id column.

    Returns
    -------
    None
        Generates a new file without Id column in the indicated path.
    """
    print('Removing Id column from {}'.format(input_file_with_id))
    data_gen = DataGenerator()
    
    # load input file
    data_gen.load_source_file(input_file_with_id)

    # drop Id column
    if 'Id' in data_gen.column_names:
        final_cols = [cn for cn in data_gen.column_names if cn != 'Id']
        data_gen.write(output_file_without_id, columns=final_cols)
    else:
        print('No Id column found in {}'.format(input_file_with_id))


def generate_status_file(source_file, original_status_file, tmp_folder=today.isoformat(), file_name=''):
    """Takes a CSV file and generates another file containing mappings of External_Ids and intermediate and final statuses for the records.
    Some MFG objects require intermediate status.

    Parameters
    ----------
    source_file : str
        The name of the file (including the path) to be processed. File must have Id, External_Id__c and Status.
    original_status_file : str
        The file name (including path) of the CSV file containing the orginal Id and Status.
    tmp_folder : str
        Name of the folder for archive path. Default = today's date.
    file_name : str
        Name of Status file.

    Returns
    -------
    None
        Generates file(s) with corresponding statuses. Note that for SalesAgreements multiple files are generated and the name of these files will depend on the intermediate status name.
    """
    
    def get_original_final_status(status_by_id, record_id):
        return status_by_id[record_id][0].get('Status')

    data_gen = DataGenerator()
    data_gen.load_source_file(source_file, ['Id', 'External_Id__c', 'Status'])
    object_status = data_gen.load_dataset('object_status', original_status_file, ['Id','Status'])
    status_by_id = object_status.group_by('Id')

    
    ## Order and Contract records can go from DRAFT directly to their final status
    ## That is why only one file containing all final statuses is needed
    ## Note: For reference, an ALL status file, containing SAs and their final status, is created for SalesAgreements
    new_rows = []
    row_count = len(data_gen.rows)
    for r in range(row_count):
        row = data_gen.rows.pop()
        column_values = data_gen.row_to_column_values(row)
        column_values['Status'] = get_original_final_status(status_by_id, column_values['Id'])
        new_rows.append(data_gen.column_values_to_row(column_values))

    data_gen.rows = new_rows
    data_gen.reverse()

    # write file containing all statuses
    status_file = definitions.mfg_temporal_path.format(tmp_folder) + file_name
    data_gen.write(status_file, columns=['External_Id__c', 'Id', 'Status'])
    
    # clear objects
    new_rows.clear()
    status_by_id.clear()
    data_gen.remove_dataset('object_status')
    
    if file_name == 'SalesAgreement.status.ALL.csv':
        ## SalesAgreements require to be updated in steps up to their final status
        ## 1> Draft (already inserted)
        ## 2> Approved (all records but the ones with final_status=Draft must be updated to Approved)
        ## 3> Discarded (only records with final status as Discarded)
        ## 4> Cancelled (only records with final status as Cancelled)
        ## 5> Expired (only records with final status as Expired)
        ## Note: Some status like Activated are automatically handled in the Org once a record is Approved
        data_gen.load_source_file(status_file)
        data_gen.add_dataset('sa_all_status', copy.deepcopy(data_gen.rows))
        for status_name in ['Approved', 'Discarded', 'Cancelled', 'Expired']:
            status_file = definitions.mfg_temporal_path.format(tmp_folder) + 'SalesAgreement.status.' + status_name.upper() + '.csv'
            if status_name == 'Approved':
                data_gen.add_constant_column('Status', 'Approved')
                data_gen.apply_transformations()
            else:
                data_gen.rows = copy.deepcopy(data_gen.datasets['sa_all_status'])
                data_gen.filter(lambda cv: cv['Status']==status_name)
            
            if data_gen.row_count:
                data_gen.write(status_file, columns=['External_Id__c', 'Status'])
            else:
                print("No records for {}".format(status_file))


def run(batch_id, source_file_name, output_file_name, config, reference_date=today_datetime, filter_function=None):

    data_gen = DataGenerator()

    # load source file
    data_gen.load_source_file(source_file_name)

    # generate external id
    col_name = config['externalIdColumnName']
    data_gen.add_formula_column(col_name, formula=lambda: config['externalIdFormat'] + str(data_gen.current_row + 1))

    # iterate through the columns to be mapped
    #  load current foreign file
    #  if replaceSourceColumn is true, replace the 'sourceColumn' by 'replacementColumnName'
    #  retrieve 'foreignRetrieveColumn' where 'foreignMappingColumn' == 'sourceColumn'
    for mapCol in config['mappings']:
        if '.source.' in mapCol['foreignFile']:
            foreign_file = definitions.mfg_source_path + mapCol['foreignFile']
        else:
            foreign_file = definitions.mfg_temporal_path.format(today.isoformat()) + mapCol['foreignFile']
        
        foreignRetrieveColumn = mapCol['foreignRetrieveColumn']
        sourceColumn = mapCol['sourceColumn']

        aux_dataset = data_gen.load_dataset('aux', foreign_file)
        aux_by_id = aux_dataset.group_by('Id')

        def get_aux_data(column_values):
            if column_values[sourceColumn] == '':
                aux_data = ''
            else:
                aux_data = aux_by_id.get(column_values[sourceColumn])[0].get(foreignRetrieveColumn)
            return aux_data
        data_gen.add_formula_column(sourceColumn, formula=get_aux_data)

        data_gen.apply_transformations()

        if mapCol['replaceSourceColumn']:
            data_gen.rename_column(sourceColumn, mapCol['replacementColumnName'])
    
    # always empty the auxiliary lists
    aux_dataset = []
    aux_by_id = []

    # remove auxiliary dataset to free up memory
    if 'aux' in data_gen.datasets:
        data_gen.remove_dataset('aux')

    if 'Status' in data_gen.column_names:
        data_gen.add_constant_column('Status', 'Draft')

    # generate LastProcessedDate
    data_gen.add_constant_column('LastProcessedDate', today.isoformat())

    # add a UUID for each row that is created in this batch
    data_gen.add_constant_column('analyticsdemo_batch_id__c', batch_id)

    data_gen.apply_transformations()

    if filter_function:
        data_gen.filter(filter_function)

    data_gen.write(output_file_name)


    # Now the creation of the status file begins
    tmp_folder = reference_date.strftime("%Y-%m-%d")
    if 'Contract.csv' in output_file_name:
        generate_status_file(source_file=output_file_name, original_status_file=definitions.source_contract, tmp_folder=tmp_folder, file_name='Contract.status.ALL.csv')
    elif 'Order.csv' in output_file_name:
        generate_status_file(source_file=output_file_name, original_status_file=definitions.source_order, tmp_folder=tmp_folder, file_name='Order.status.ALL.csv')
    elif 'SalesAgreement.csv' in output_file_name:
        generate_status_file(source_file=output_file_name, original_status_file=definitions.source_sales_agreement, tmp_folder=tmp_folder, file_name='SalesAgreement.status.ALL.csv')


if __name__ == "__main__":
    # execute only if running as a script
    run('1', 'data/input/Contract.source.csv', 'data/output/Contract.csv')
    dropId('data/output/Contract.csv', 'data/output/Contract.csv')
