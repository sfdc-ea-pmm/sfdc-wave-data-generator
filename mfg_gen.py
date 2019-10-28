import os
import boto3
import split_data_file

from datetime import date
from mfg import mfg_generator


def run():
    today = date.today()
    config_path = 'mfg/config.json'

    if os.environ.get('WRITE_MODE') != 'S3':
        source_path = 'mfg/data/input/'
        output_path = 'mfg/data/output/latest/'
        archive_path = 'mfg/data/output/archive/{}/'.format(today.isoformat())
    else:
        source_path = 'mfg/data/input/'
        output_path = 'mfg/data/output/latest/'
        archive_path = 'mfg/data/output/archive/{}/'.format(today.isoformat())

    if os.environ.get('WRITE_MODE') != 'S3' and not os.path.exists(output_path):
        os.makedirs(output_path)

    if os.environ.get('WRITE_MODE') != 'S3' and not os.path.exists(archive_path):
        os.makedirs(archive_path)

    mfg_generator.run(source_path, output_path, config_path)

    
    if False: # no splitting for now oz.
        suffix = '-dataPart-'
        if os.environ.get('WRITE_MODE') != 'S3':
            for f in os.listdir(output_path):
                if suffix not in f:
                    r = split_data_file.split_if_needed(output_path, f, output_path, suffix, deleteSource=True)
                    print(r)
        else:
            client = boto3.client('s3')
            paginator = client.get_paginator('list_objects_v2')
            result = paginator.paginate(Bucket=os.environ.get('S3_BUCKET_NAME'),StartAfter=output_path)
            for page in result:
                if "Contents" in page:
                    for key in page["Contents"]:
                        path_and_file = key["Key"].rsplit('/', 1)
                        f = path_and_file[-1] # get just the name of the file
                        if path_and_file[0] not in output_path:
                            break
                        if suffix not in f:
                            r = split_data_file.split_if_needed(output_path, f, output_path, suffix, deleteSource=True)
                    break # no need to look further down in the directory structure

if __name__ == "__main__":
    # execute only if running as a script
    run()