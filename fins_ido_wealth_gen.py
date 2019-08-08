import os
from datetime import date

from fins_ido_wealth import fins_ido_wealth_generator


def run():
    today = date.today()

    if os.environ.get('WRITE_MODE') != 'S3':
        source_path = 'fins_ido_wealth/data/input/'
        output_path = 'fins_ido_wealth/data/output/latest/'
        archive_path = 'fins_ido_wealth/data/output/archive/{}/'.format(today.isoformat())
        config_path = 'fins_ido_wealth/config.json'
    else:
        source_path = 'fins-ido-wealth/data/input/'
        output_path = 'fins-ido-wealth/data/output/latest/'
        archive_path = 'fins-ido-wealth/data/output/archive/{}/'.format(today.isoformat())
        config_path = 'fins-ido-wealth/config.json'

    if os.environ.get('WRITE_MODE') != 'S3' and not os.path.exists(output_path):
        os.makedirs(output_path)

    if os.environ.get('WRITE_MODE') != 'S3' and not os.path.exists(archive_path):
        os.makedirs(archive_path)

    fins_ido_wealth_generator.run(source_path, output_path, config_path)

    fins_ido_wealth_generator.run(source_path, archive_path, config_path)

if __name__ == "__main__":
    # execute only if running as a script
    run()