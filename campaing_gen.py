import os
from datetime import date

from campaign import campaign_generator


def run():
    today = date.today()
    source_path = 'campaign/data/input/'
    # output_path = 'b2b_commerce/output/archive/{}/'.format(today.isoformat())
    output_path = 'campaign/data/output/latest/'

    archive_path = 'campaign/data/output/archive/{}/'.format(today.isoformat())

    config_path = 'campaign/config.json'

    if os.environ.get('WRITE_MODE') != 'S3' and not os.path.exists(output_path):
        os.makedirs(output_path)

    if os.environ.get('WRITE_MODE') != 'S3' and not os.path.exists(archive_path):
        os.makedirs(archive_path)

    campaign_generator.run(source_path, output_path, config_path)

    campaign_generator.run(source_path, archive_path, config_path)

if __name__ == "__main__":
    # execute only if running as a script
    run()
