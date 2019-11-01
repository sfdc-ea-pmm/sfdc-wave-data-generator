## this program creates external ids and links records across multiple data files

import copy_data_file
import dateutil.parser
import os
import json

from mfg_linker import mfg_file_gen
from mfg_linker import definitions

from datetime import date
from datetime import datetime
from datetime import timedelta

def file_to_string(relative_path):
    str_file = open(relative_path, 'r').read()
    return str_file

def run():
    """Loads input CSV files for MFG and creates External Ids for all records. Then maps all rows in the files using this newly generated External Ids.

    This data will be loaded either from local disk or S3 depending on the READ_MODE
    environment variable. If READ_MODE=S3, it will load the dataset file using the
    load_dataset_from_s3 function, otherwise it will read from local disk using
    the load_dataset_from_s3 function.

    Parameters
    ----------
    No parameters needed. Everything is specified in mfg_linker.definitions file.

    Returns
    -------
    None
        Generates files in output folders.
    """

    today = date.today()
    today_datetime = datetime.combine(today, datetime.min.time())
    output_path = definitions.mfg_temporal_path.format(today.isoformat())
    
    configs = json.loads(file_to_string(definitions.config_file))
    files_list = configs.get('configs')

    batch_id = datetime.now().strftime("%Y%m%d%-H%M%S%f")

    # make output directory if it doesn't exist
    if os.environ.get('WRITE_MODE') != 'S3' and not os.path.exists(output_path):
        os.makedirs(output_path)

    out_files_list = []
    for f in files_list:
        # generate file
        source_file = definitions.mfg_source_path + f['mainInputFile']
        output_file = output_path + f['outputFile']
        mfg_file_gen.run(batch_id, source_file, output_file, f, today_datetime)
        out_files_list.append( {'filePath': output_file, 'fileName': f['outputFile']} )

    # add status files
    out_files_list.append({'filePath': output_path + 'Contract.status.ALL.csv', 'fileName': 'Contract.status.ALL.csv'})
    out_files_list.append({'filePath': output_path + 'Order.status.ALL.csv', 'fileName': 'Order.status.ALL.csv'})
    out_files_list.append({'filePath': output_path + 'SalesAgreement.status.ALL.csv', 'fileName': 'SalesAgreement.status.ALL.csv'})
    out_files_list.append({'filePath': output_path + 'SalesAgreement.status.APPROVED.csv', 'fileName': 'SalesAgreement.status.APPROVED.csv'})
    out_files_list.append({'filePath': output_path + 'SalesAgreement.status.DISCARDED.csv', 'fileName': 'SalesAgreement.status.DISCARDED.csv'})
    out_files_list.append({'filePath': output_path + 'SalesAgreement.status.CANCELLED.csv', 'fileName': 'SalesAgreement.status.CANCELLED.csv'})
    out_files_list.append({'filePath': output_path + 'SalesAgreement.status.EXPIRED.csv', 'fileName': 'SalesAgreement.status.EXPIRED.csv'})

    # copy all files to the latest folder
    latest_output_path = definitions.mfg_latest_path

    if os.environ.get('WRITE_MODE') != 'S3' and not os.path.exists(latest_output_path):
        os.makedirs(latest_output_path)

    for f in out_files_list:
        # first remove all Id columns
        mfg_file_gen.dropId(f['filePath'], f['filePath'])

        # then copy to 'latest'
        latest_data_file = latest_output_path + f['fileName']
        copy_data_file.run(f['filePath'], latest_data_file)


if __name__ == "__main__":
    # execute only if running as a script
    run()
