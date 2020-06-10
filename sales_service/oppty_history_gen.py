import dateutil.parser

from data_generator import DataGenerator
from data_generator.formula import fake
from datetime import date
from datetime import datetime
from datetime import timedelta
from numpy.random import choice
from random import randint
from random import uniform

today = date.today()
today_datetime = datetime.combine(today, datetime.min.time())


def run(batch_id, source_file_name, output_file_name, reference_date=today_datetime):
    data_gen = DataGenerator()

    # load source file
    source_columns = [
        'External_Id__c',
        'StageName',
        'Amount',
        'ForecastCategory',
        'CloseDate',
        'CreatedDate__c',
        'SalesStageCount__c'
    ]
    data_gen.load_source_file(source_file_name, source_columns)

    data_gen.rename_columns({
        'StageName': 'StageName__c',
        'Amount': 'Amount__c',
        'ForecastCategory': 'ForecastCategory__c',
        'CloseDate': 'CloseDate__c'
    })

    data_gen.add_copy_column('Opportunity.External_Id__c', 'External_Id__c')

    # add a UUID for each row that is created in this batch
    data_gen.add_constant_column('analyticsdemo_batch_id__c', batch_id)

    data_gen.apply_transformations()

    stages = ['Qualification', 'Discovery', 'Proposal/Quote', 'Negotiation']
    forecast_categories = ['BestCase', 'Pipeline', 'Commit']

    pipe_bucket = ['No Change', 'Reopen', 'Expand', 'Reduce', 'Moved Out', 'Moved In', 'Stage Change']
    pipe_bucket_ratio = [0.10, 0.05, 0.15, 0.15, 0.30, 0.10, 0.15]
    qualification_pipe_bucket = ['No Change', 'Reopen', 'Expand', 'Reduce', 'Moved Out', 'Moved In']
    qualification_pipe_bucket_ratio = [0.20, 0.05, 0.20, 0.10, 0.35, 0.10]
    zero_amount_pipe_bucket = ['No Change', 'Reopen', 'Moved Out', 'Moved In', 'Stage Change']
    zero_amount_pipe_bucket_ratio = [0.20, 0.05, 0.35, 0.10, 0.30]

    current_count = 1
    new_rows = []
    row_count = len(data_gen.rows)
    for i in range(row_count):
        row = data_gen.rows.pop()
        column_values = data_gen.row_to_column_values(row)

        opportunity_id = column_values['Opportunity.External_Id__c']
        close_date = dateutil.parser.parse(column_values['CloseDate__c'])
        create_date = dateutil.parser.parse(column_values['CreatedDate__c'])
        final_amount = int(column_values['Amount__c'])
        final_forecast_category = column_values['ForecastCategory__c']
        final_stage_name = column_values['StageName__c']
        stage_count = int(column_values['SalesStageCount__c'])

        # initialize most recent event date to reference_date or earlier
        event_date_range_start = create_date + (close_date - create_date) / 2
        event_date_range_end = close_date

        if close_date > reference_date:
            event_date_range_end = reference_date
            event_date_range_start = create_date + (reference_date - create_date) / 2

        # ensure event happens on or after opportunity create_date
        event_date = fake.date_time_between_dates(event_date_range_start, event_date_range_end)

        # create final state
        column_values['CreatedDate__c'] = event_date
        column_values['External_Id__c'] = 'W_OpportunityHistory.' + str(current_count)
        current_count += 1
        new_rows.append(data_gen.column_values_to_row(column_values))

        next_create_date = event_date
        next_stage_name = final_stage_name
        next_forecast_category = final_forecast_category
        next_close_date = close_date
        next_amount = final_amount

        movedOut = False
        movedIn = False
        expand = False
        reduce = False
        reopen = False
        initialized = False

        # generate events in reverse order until create_date
        for current_stage_count in range(stage_count):
            # choose the proper bucket depending on the scenario
            bucket = pipe_bucket
            ratio = pipe_bucket_ratio
            if next_amount <= 0:
                bucket = zero_amount_pipe_bucket
                ratio = zero_amount_pipe_bucket_ratio
            elif next_stage_name == 'Qualification':
                bucket = qualification_pipe_bucket
                ratio = qualification_pipe_bucket_ratio

            event = choice(bucket, p=ratio)

            event_date_range_end = event_date
            event_date_range_start = create_date + (event_date - create_date) / 2
            event_date = fake.date_time_between_dates(event_date_range_start, event_date_range_end)

            # if next stage is closed, make the previous event a stage change
            if 'Closed' in next_stage_name:
                event = 'Stage Change'

            # if the event date is the create date, create the initial state
            if current_stage_count == stage_count - 1:
                event_date = create_date
                event = 'Initial State'

            if event != 'No Change':
                curr_close_date = next_close_date
                curr_amount = next_amount
                curr_stage_name = next_stage_name
                curr_forecast_category = next_forecast_category

                if event == 'Reopen' and not reopen:
                    curr_stage_name = 'Closed Lost'
                    curr_forecast_category = 'Omitted'
                    reopen = True
                elif event == 'Initial State':
                    curr_stage_name = 'Qualification'
                    curr_forecast_category = 'Pipeline'
                    initialized = True
                elif event == 'Expand' and not expand:
                    curr_amount = next_amount - int(uniform(.15, .45) * final_amount)
                    if curr_amount <= 0:
                        # reduce instead
                        curr_amount = next_amount + int(uniform(.15, .45) * final_amount)
                    expand = True
                elif event == 'Reduce' and not reduce:
                    curr_amount = next_amount + int(uniform(.15, .45) * final_amount)
                    reduce = True
                elif event == 'Moved In' and not movedIn:
                    curr_close_date = curr_close_date + timedelta(days=randint(0, 30))
                    movedIn = True
                elif event == 'Moved Out' and not movedOut:
                    curr_close_date = curr_close_date - timedelta(days=randint(30, 90))
                    movedOut = True
                elif event == 'Stage Change':
                    # if next stage is not closed, use previous stage
                    if 'Closed' not in next_stage_name and stages.index(next_stage_name) - 1 > 0:
                        curr_stage_name = stages[stages.index(next_stage_name) - 1]
                    # if next stage is closed, use any stage
                    elif 'Closed' in next_stage_name:
                        curr_stage_name = stages[randint(1, len(stages) - 1)]
                    else:
                        curr_stage_name = stages[0]
                    curr_forecast_category = forecast_categories[randint(0, len(forecast_categories) - 1)]

                new_column_values = {
                    'External_Id__c': 'W_OpportunityHistory.' + str(current_count),
                    'Opportunity.External_Id__c': opportunity_id,
                    'StageName__c': curr_stage_name,
                    'Amount__c': curr_amount,
                    'ForecastCategory__c': curr_forecast_category,
                    'CreatedDate__c': event_date.isoformat(sep=' '),
                    'CloseDate__c': curr_close_date.date().isoformat(),
                    'analyticsdemo_batch_id__c': batch_id
                }
                current_count += 1
                new_rows.append(data_gen.column_values_to_row(new_column_values))

                next_stage_name = curr_stage_name
                next_forecast_category = curr_forecast_category
                next_close_date = curr_close_date
                next_amount = curr_amount

    data_gen.rows = new_rows
    data_gen.reverse()

    data_gen.write(output_file_name, [
        'External_Id__c',
        'Amount__c',
        'StageName__c',
        'ForecastCategory__c',
        'CloseDate__c',
        'CreatedDate__c',
        'Opportunity.External_Id__c',
        'analyticsdemo_batch_id__c'])


if __name__ == "__main__":
    # execute only if running as a script
    run('1', 'data/output/OpportunityShape.csv', 'data/output/OpportunityHistory.csv')
