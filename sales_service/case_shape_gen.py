import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import dateutil.parser

from data_generator import DataGenerator
from datetime import date
from datetime import datetime
from datetime import timedelta
from data_generator.formula import fake
from numpy.random import choice
from numpy.random import randint

today = date.today()
today_datetime = datetime.combine(today, datetime.min.time())


def run(batch_id, source_file_name, output_file_name, reference_date=today_datetime):
    
    def get_close_date(values):
        return dateutil.parser.parse(values['ClosedDate__c'])

    def get_create_date(values):
        return dateutil.parser.parse(values['CreatedDate__c'])

    data_gen = DataGenerator()

    # load source file
    data_gen.load_source_file(source_file_name)

    # calculate dates
    def close_date_formula(column_values):
        last_day = date(date.today().year, 12, 31)
        last_day = datetime.combine(last_day, datetime.min.time())
        offset = column_values['close_date_offset']
        # last day of current year - offset
        close_date = last_day - timedelta(days=int(offset))
        close_date = close_date + timedelta(hours=int(choice([9, 10, 11, 12, 13, 14, 15, 16, 17],
                                                         p=[.12, .13, .13, .07, .09, .13, .13, .11, .09])),
                                            minutes=randint(0, 60),
                                            seconds=randint(0, 60))
        
        return close_date.isoformat(sep=' ')
    
    data_gen.add_formula_column('ClosedDate__c', close_date_formula)


    def created_date_formula(column_values):
        time_open = int(column_values['Time_Open__c'])
        date_closed = dateutil.parser.parse(column_values['ClosedDate__c'])
        return (date_closed - timedelta(days=time_open)).isoformat(sep=' ')
    
    data_gen.add_formula_column('CreatedDate__c', created_date_formula)

    # generate last activity date
    def last_activity_date_formula(column_values):
        create_date = dateutil.parser.parse(column_values['CreatedDate__c'])
        close_date = dateutil.parser.parse(column_values['ClosedDate__c'])
        if close_date > today_datetime:
            close_date = today_datetime
        if create_date > today_datetime:
            create_date = today_datetime
        return fake.date_time_between_dates(create_date, close_date).date()
    data_gen.add_formula_column('LastActivityDate__c', formula=last_activity_date_formula)

    data_gen.apply_transformations()

    new_rows = []
    row_count = len(data_gen.rows)
    for i in range(row_count):
        row = data_gen.rows.pop()
        column_values = data_gen.row_to_column_values(row)

        close_day = get_close_date(column_values)
        create_day = get_create_date(column_values)

        # if close date is before reference date keep it exactly as is
        if close_day <= reference_date:
            new_rows.append(row)

        # if create date is before reference date, but the close date is after reference date
        elif (create_day <= reference_date) and (close_day > reference_date):

            column_values['Status'] = choice([
                'New',
                'Working',
                'Waiting on Customer',
                'Response Received',
                'Escalated',
                'Warning',
                'Attention',
                'On Hold',
                'Closed in Community'], p=[
                0.20,
                0.30,
                0.10,
                0.05,
                0.10,
                0.05,
                0.05,
                0.10,
                0.05
            ])

            new_rows.append(data_gen.column_values_to_row(column_values))

    data_gen.rows = new_rows
    data_gen.reverse()

    def milestone_status_formula(column_values):
        status = column_values['Status']
        if status != 'Closed':
            status = 'Open'
        sla = column_values['SLA']
        return status + ' - ' + sla
    data_gen.add_formula_column('MilestoneStatus__c', formula=milestone_status_formula)

    data_gen.add_formula_column('External_Id__c', formula=lambda: 'W_Case.' + str(data_gen.current_row + 1))

    # add a UUID for each row that is created in this batch
    data_gen.add_constant_column('analyticsdemo_batch_id__c', batch_id)

    data_gen.apply_transformations()

    data_gen.write(output_file_name)

if __name__ == "__main__":
    # execute only if running as a script
    run('1', 'data/input/CaseShape.csv', 'data/output/CaseShape.csv')
