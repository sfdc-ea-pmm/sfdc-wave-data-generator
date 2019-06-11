import os
from datetime import date

from lead_trending import lead_trending_generator


def run():
    today = date.today()

    if os.environ.get('WRITE_MODE') != 'S3':
        source_path = 'lead_trending/data/input/'
        output_path = 'lead_trending/data/output/latest/'
        archive_path = 'lead_trending/data/output/archive/{}/'.format(today.isoformat())
        config_path = 'lead_trending/config.json'
    else:
        source_path = 'lead-trending/data/input/'
        output_path = 'lead-trending/data/output/latest/'
        archive_path = 'lead-trending/data/output/archive/{}/'.format(today.isoformat())
        config_path = 'lead_trending/config.json'

    if os.environ.get('WRITE_MODE') != 'S3' and not os.path.exists(output_path):
        os.makedirs(output_path)

    if os.environ.get('WRITE_MODE') != 'S3' and not os.path.exists(archive_path):
        os.makedirs(archive_path)

    lead_trending_generator.run(source_path, output_path, config_path)

    lead_trending_generator.run(source_path, archive_path, config_path)

if __name__ == "__main__":
    # execute only if running as a script
    run()