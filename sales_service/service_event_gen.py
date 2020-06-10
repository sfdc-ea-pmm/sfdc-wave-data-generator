import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import dateutil.parser

from data_generator import DataGenerator
from data_generator.formula import event
from data_generator.formula import fake
from datetime import date
from datetime import datetime
from datetime import timedelta
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
        'LastActivityDate__c'
    ]

    data_gen.load_source_file(source_file_name, source_columns)

    data_gen.rename_column('External_Id__c', 'Case.External_Id__c')

    data_gen.duplicate_rows(duplication_factor=lambda: randint(0, 3))

    data_gen.add_formula_column('External_Id__c', formula=lambda: 'W_Event.' + str(id_offset + data_gen.current_row + 1))

    data_gen.add_formula_column('Subject', formula=event.event_subject)
    data_gen.add_formula_column('EventSubtype', formula=event.event_subtype)
    data_gen.add_formula_column('DurationInMinutes', formula=event.event_call_duration)

    def create_date_formula(column_values):
        case_create_date = dateutil.parser.parse(column_values['CreatedDate__c'])
        case_close_date = datetime.combine(dateutil.parser.parse(column_values['LastActivityDate__c']), case_create_date.time())
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

    def activity_datetime_formula(column_values):
        return dateutil.parser.parse(column_values['ActivityDate'])
    
    data_gen.add_formula_column('ActivityDateTime', activity_datetime_formula)

    data_gen.add_constant_column('ShowAs', 'Busy')

    # add a UUID for each row that is created in this batch
    data_gen.add_constant_column('analyticsdemo_batch_id__c', batch_id)

    # apply transformations and write
    data_gen.apply_transformations()

    output_columns = [
        'External_Id__c',
        'Owner.External_Id__c',
        'Case.External_Id__c',
        'Subject',
        'EventSubtype',
        'DurationInMinutes',
        'ShowAs',
        'CreatedDate__c',
        'LastModifiedDate__c',
        'ActivityDate',
        'ActivityDateTime',
        'analyticsdemo_batch_id__c'
    ]

    data_gen.write(output_file_name, output_columns)

if __name__ == "__main__":
    # execute only if running as a script
    run('1', 'data/output/CaseShape.csv', 'data/output/ServiceEvent.csv')
