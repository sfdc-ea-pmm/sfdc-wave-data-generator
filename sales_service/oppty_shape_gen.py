import definitions
import dateutil.parser

from data_generator import DataGenerator
from data_generator.formula import fake
from datetime import date
from datetime import datetime
from datetime import timedelta
from math import floor, ceil
from numpy.random import choice

today = date.today()
today_datetime = datetime.combine(today, datetime.min.time())


def run(batch_id, source_file_name, output_file_name, reference_date=today_datetime, filter_function=None):

    def get_close_date(values):
        return dateutil.parser.parse(values['CloseDate'])

    def get_create_date(values):
        return dateutil.parser.parse(values['CreatedDate__c'])

    data_gen = DataGenerator()

    # load source file
    data_gen.load_source_file(source_file_name)

    # add a UUID for each row that is created in this batch
    data_gen.add_constant_column('analyticsdemo_batch_id__c', batch_id)

    # add an age column
    data_gen.add_copy_column('Age__c', 'TimeToClose__c')

    # generate a close date
    def close_date_formula(column_values):
        last_day = date(date.today().year, 12, 31)
        offset = column_values['close_date_offset__c']
        # last day of current year - offset
        close_date = last_day - timedelta(days=int(offset))
        return str(close_date)
    data_gen.add_formula_column('CloseDate', close_date_formula)


    # generate a create date
    def create_date_formula(column_values):
        close_date = dateutil.parser.parse(column_values['CloseDate'])
        offset = column_values['TimeToClose__c']
        create_date = close_date - timedelta(days=int(offset))
        return create_date.isoformat(sep=' ')
    data_gen.add_formula_column('CreatedDate__c', create_date_formula)

    # generate last activity date
    def last_activity_date_formula(column_values):
        create_date = get_create_date(column_values)
        close_date = get_close_date(column_values)
        if close_date > reference_date:
            close_date = reference_date
        if create_date > reference_date:
            create_date = reference_date
        return fake.date_time_between_dates(create_date, close_date).date()
    data_gen.add_formula_column('LastActivityDate__c', formula=last_activity_date_formula)

    data_gen.apply_transformations()

    if filter_function:
        data_gen.filter(filter_function)

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
            # set age
            age = (reference_date - create_day).days
            column_values['Age__c'] = age

            ttc = float(column_values['TimeToClose__c'])
            pct = age / ttc

            # set IsClosed to blank
            column_values['IsClosed'] = ''

            # set IsWon to blank
            column_values['IsWon'] = ''

            # set a stage name
            stage_name_index = int(floor(pct * 4) + choice([-1, 0, 1], p=[.2, .7, .1]))

            # adjust the stage name index
            if stage_name_index < 0:
                stage_name_index = 0
            if stage_name_index > 3:
                stage_name_index = 3

            column_values['StageName'] = definitions.stage_name[stage_name_index]

            column_values['Probability'] = definitions.probabilities[stage_name_index]

            column_values['ForecastCategory'] = definitions.forecast_category[choice([1, 2, 4], p=[.625, .25, .125])]

            column_values['ForecastCategoryName'] = definitions.forecast_category_name[column_values['ForecastCategory']]

            column_values['SalesStageCount__c'] = ceil(pct * float(column_values['SalesStageCount__c']))

            new_rows.append(data_gen.column_values_to_row(column_values))



    data_gen.rows = new_rows
    data_gen.reverse()

    data_gen.write(output_file_name)


if __name__ == "__main__":
    # execute only if running as a script
    run('1', 'data/input/OpportunityShape.csv', 'data/output/OpportunityShape.csv')
