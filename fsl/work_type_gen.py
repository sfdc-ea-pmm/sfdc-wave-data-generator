import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from data_generator import DataGenerator
from datetime import datetime


def run(batch_id, source_file_name, output_file_name):
    data_gen = DataGenerator()

    # load source file
    data_gen.load_source_file(source_file_name)

    data_gen.write(output_file_name, columns=[
        'External_ID__c',
        'Name',
        'DurationType',
        'EstimatedDuration'
        #'Burden_Cost__c',
        #'Revenue__c'
    ])


if __name__ == "__main__":
    # execute only if running as a script
    run(datetime.now().strftime("%Y%m%d%-H%M%S%f"), 'data/output/WorkType.csv', 'data/output/WorkType.csv')