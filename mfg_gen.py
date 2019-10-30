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

    
if __name__ == "__main__":
    # execute only if running as a script
    run()