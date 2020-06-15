import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import dateutil.parser

from data_generator import DataGenerator
from data_generator.formula import fake
from datetime import date
from datetime import datetime
from datetime import timedelta
from numpy.random import choice
from numpy.random import normal
from numpy.random import randint

today = date.today()
today_datetime = datetime.combine(today, datetime.min.time())

def run(batch_id, source_file_name, output_file_name, reference_date=today_datetime):
    data_gen = DataGenerator()

    # load source file
    data_gen.load_source_file(source_file_name, ['External_Id__c'])

    data_gen.rename_column('External_Id__c', 'User.External_Id__c')

    data_gen.add_copy_column('Owner.External_Id__c', 'User.External_Id__c')

    data_gen.duplicate_rows(duplication_factor=lambda: int(normal(60, 10)))

    data_gen.add_formula_column('External_Id__c', lambda: 'W_UserServicePresence.' + str(data_gen.current_row + 1))

    data_gen.add_formula_column('AtCapacityDuration__c', lambda: randint(30, 900))

    data_gen.add_formula_column('AverageCapacity__c', lambda: randint(30, 500))

    data_gen.add_formula_column('ConfiguredCapacity__c', lambda: randint(30, 600))

    start_date = reference_date - timedelta(days=365)
    end_date = reference_date

    data_gen.add_formula_column('CreatedDate__c',
                                lambda: fake.date_time_between_dates(start_date, end_date).isoformat(sep=' '))

    data_gen.add_formula_column('IdleDuration__c', lambda: randint(30, 600))

    data_gen.add_formula_column('IsCurrentState__c', lambda: choice(['true', 'false']))

    data_gen.add_formula_column('IsAway__c', lambda: choice(['true', 'false']))

    data_gen.add_formula_column('StatusDuration__c', lambda: randint(30, 900))

    data_gen.add_copy_column('StatusStartDate__c', 'CreatedDate__c')

    def status_end_date_formula(column_values):
        start_date = dateutil.parser.parse(column_values['StatusStartDate__c'])
        status_duration = int(column_values['StatusDuration__c'])
        return (start_date + timedelta(seconds=status_duration)).isoformat(sep=' ')
    data_gen.add_formula_column('StatusEndDate__c', formula=status_end_date_formula)


    data_gen.add_formula_column('ServicePresenceStatus.DeveloperName', [
        'Busy',
        'Online',
        'Available_Live_Agent',
        'Busy_Break',
        'Busy_Lunch',
        'Busy_Training',
        'Available_LiveMessage'
    ])

    # add a UUID for each row that is created in this batch
    data_gen.add_constant_column('analyticsdemo_batch_id__c', batch_id)

    data_gen.apply_transformations()

    output_columns = [
        'External_Id__c',
        'User.External_Id__c',
        'Owner.External_Id__c',
        'AtCapacityDuration__c',
        'AverageCapacity__c',
        'ConfiguredCapacity__c',
        'CreatedDate__c',
        'IdleDuration__c',
        'IsAway__c',
        'IsCurrentState__c',
        'StatusDuration__c',
        'StatusStartDate__c',
        'StatusEndDate__c',
        'ServicePresenceStatus.DeveloperName',
        'analyticsdemo_batch_id__c'
    ]
    data_gen.write(output_file_name, output_columns)


if __name__ == "__main__":
    # execute only if running as a script
    run('1', 'data/output/User.csv', 'data/output/UserServicePresence.csv')
