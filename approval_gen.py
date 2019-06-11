import os
from datetime import date

from approval import approval_generator


def run():
    today = date.today()

    source_path = 'approval/data/input/'
    output_path = 'approval/data/output/latest/'
    archive_path = 'approval/data/output/archive/{}/'.format(today.isoformat())
    config_path = 'approval/config.json'

    if os.environ.get('WRITE_MODE') != 'S3' and not os.path.exists(output_path):
        os.makedirs(output_path)

    if os.environ.get('WRITE_MODE') != 'S3' and not os.path.exists(archive_path):
        os.makedirs(archive_path)

    approval_generator.run(source_path, output_path, config_path)

    approval_generator.run(source_path, archive_path, config_path)

if __name__ == "__main__":
    # execute only if running as a script
    run()