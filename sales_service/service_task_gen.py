import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import dateutil.parser

from data_generator import DataGenerator
from data_generator.formula import fake
from data_generator.formula import task
from datetime import date
from datetime import datetime
from datetime import timedelta
from numpy.random import choice
from numpy.random import randint


today = date.today()
today = datetime.combine(today, datetime.min.time())


def run(batch_id, source_file_name, output_file_name, reference_datetime=today, id_offset=0):
    
    data_gen = DataGenerator()

    # load source file
    source_columns = [
        'External_Id__c',
        'Owner.External_Id__c',
        'CreatedDate__c',
        'LastActivityDate__c',
        'Team__c'
    ]

    data_gen.load_source_file(source_file_name, source_columns)

    data_gen.rename_column('External_Id__c', 'Case.External_Id__c')
    data_gen.rename_column('LastActivityDate__c', 'ActivityDate')
    data_gen.rename_column('Team__c', 'CallObject')

    # generate a random number of tasks per case
    data_gen.duplicate_rows(duplication_factor=lambda: randint(0, 3))

    data_gen.add_formula_column('External_Id__c', formula=lambda: 'W_Task.' + str(id_offset + data_gen.current_row + 1))

    data_gen.add_formula_column('TaskSubtype', formula=task.task_subtype)
    data_gen.add_formula_column('CallDurationInSeconds', formula=task.task_call_duration)
    data_gen.add_formula_column('CallDisposition', formula=task.task_call_disposition)
    data_gen.add_formula_column('CallType', formula=task.task_call_type)
    data_gen.add_formula_column('Status', formula=task.task_status)
    data_gen.add_formula_column('Priority', formula=task.task_priority)

    def create_date_formula(column_values):
        case_create_date = dateutil.parser.parse(column_values['CreatedDate__c'])
        case_close_date = datetime.combine(dateutil.parser.parse(column_values['ActivityDate']), case_create_date.time())
        if case_close_date > reference_datetime:
            case_close_date = reference_datetime
        create_date = fake.date_time_between_dates(case_create_date, case_close_date)
        if create_date > reference_datetime:
            create_date = reference_datetime
        return create_date.isoformat(sep=' ')

    data_gen.add_formula_column('CreatedDate__c', create_date_formula)

    data_gen.add_copy_column('LastModifiedDate__c', 'CreatedDate__c')

    def activity_date_formula(column_values):
        create_date = dateutil.parser.parse(column_values['CreatedDate__c']).date()
        return (create_date + timedelta(days=randint(0, 14))).isoformat()
    
    data_gen.add_formula_column('ActivityDate', activity_date_formula)

    data_gen.add_formula_column('Subject', formula=task.task_subject_simple)

    data_gen.add_map_column('Type', 'Subject', value_map={
        'Call': lambda: choice(['Call', 'Meeting'], p=[.70, .30]),
        'Send Letter': 'Email',
        'Send Quote': 'Email',
        None: lambda: choice(['Meeting', 'Prep', 'Other'], p=[.50, .25, .25])
    })

    # add a UUID for each row that is created in this batch
    data_gen.add_constant_column('analyticsdemo_batch_id__c', batch_id)

    # apply transformations and write
    data_gen.apply_transformations()

    output_columns = [
        'External_Id__c',
        'Owner.External_Id__c',
        'Case.External_Id__c',
        'CreatedDate__c',
        'LastModifiedDate__c',
        'ActivityDate',
        'Subject',
        'Type',
        'TaskSubtype',
        'CallDurationInSeconds',
        'CallDisposition',
        'CallType',
        'CallObject',
        'Status',
        'Priority',
        'analyticsdemo_batch_id__c'
    ]
    data_gen.write(output_file_name, output_columns)

if __name__ == "__main__":
    # execute only if running as a script
    run('1', 'data/output/CaseShape.csv', 'data/output/ServiceTask.csv')
