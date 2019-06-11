import os
from datetime import date

from social import social_generator


def run():
    today = date.today()

    source_path = 'social/data/input/'
    output_path = 'social/data/output/latest/'
    archive_path = 'social/data/output/archive/{}/'.format(today.isoformat())
    config_path = 'social/config.json'

    if os.environ.get('WRITE_MODE') != 'S3' and not os.path.exists(output_path):
        os.makedirs(output_path)

    if os.environ.get('WRITE_MODE') != 'S3' and not os.path.exists(archive_path):
        os.makedirs(archive_path)

    social_generator.run(source_path, output_path, config_path)

    social_generator.run(source_path, archive_path, config_path)

if __name__ == "__main__":
    # execute only if running as a script
    run()