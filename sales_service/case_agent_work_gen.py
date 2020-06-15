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
from numpy.random import randint

today = date.today()
today = datetime.combine(today, datetime.min.time())

def run(batch_id, source_file_name, output_file_name, reference_datetime=today):
    data_gen = DataGenerator()

    # load source file
    data_gen.load_source_file(source_file_name)

    data_gen.rename_column('External_Id__c', 'Case.External_Id__c')
    data_gen.rename_column('Owner.External_Id__c', 'User.External_Id__c')

    data_gen.duplicate_rows(duplication_factor=lambda: choice([1, 2, 3, 4, 5], p=[.65, .15, .10, .05, .05]))

    data_gen.add_formula_column('External_Id__c', formula=lambda: 'W_AgentWork.' + str(data_gen.current_row + 1))

    data_gen.add_copy_column('RequestDateTime__c', 'CreatedDate__c')

    def created_date_formula(column_values):
        created_date = dateutil.parser.parse(column_values['CreatedDate__c'])
        closed_date = dateutil.parser.parse(column_values['ClosedDate__c'])
        if closed_date > reference_datetime:
            closed_date = reference_datetime
        mid_date = created_date + (closed_date - created_date)/2
        return fake.date_time_between_dates(created_date, mid_date).isoformat(sep=' ')
    data_gen.add_formula_column('CreatedDate__c', created_date_formula)

    def assigned_date_formula(column_values):
        created_date = dateutil.parser.parse(column_values['CreatedDate__c'])
        return (created_date + timedelta(seconds=randint(0, 120))).isoformat(sep=' ')
    data_gen.add_formula_column('AssignedDateTime__c', assigned_date_formula)

    def accept_date_formula(column_values):
        assigned_date = dateutil.parser.parse(column_values['AssignedDateTime__c'])
        return (assigned_date + timedelta(seconds=randint(30, 600))).isoformat(sep=' ')
    data_gen.add_formula_column('AcceptDateTime__c', accept_date_formula)

    def close_date_formula(column_values):
        accept_date = dateutil.parser.parse(column_values['AcceptDateTime__c'])
        return (accept_date + timedelta(seconds=randint(30, 1800))).isoformat(sep=' ')
    data_gen.add_formula_column('CloseDateTime__c', close_date_formula)

    def active_time_formula(column_values):
        accept_date = dateutil.parser.parse(column_values['AcceptDateTime__c'])
        close_date = dateutil.parser.parse(column_values['CloseDateTime__c'])
        return int((close_date - accept_date).total_seconds())
    data_gen.add_formula_column('ActiveTime__c', active_time_formula)

    data_gen.add_formula_column('AgentCapacityWhenDeclined__c', lambda: randint(30, 1800))

    def cancel_date_formula(column_values):
        assigned_date = dateutil.parser.parse(column_values['AssignedDateTime__c'])
        return (assigned_date + timedelta(seconds=randint(30, 600))).isoformat(sep=' ')
    data_gen.add_formula_column('CancelDateTime__c', cancel_date_formula)

    data_gen.add_formula_column('CapacityPercentage__c', lambda: randint(1, 101))

    data_gen.add_formula_column('CapacityWeight__c', lambda: randint(1, 7))

    def decline_date_formula(column_values):
        assigned_date = dateutil.parser.parse(column_values['AssignedDateTime__c'])
        return (assigned_date + timedelta(seconds=randint(30, 600))).isoformat(sep=' ')
    data_gen.add_formula_column('DeclineDateTime__c', decline_date_formula)

    data_gen.add_formula_column('DeclineReason__c', formula=fake.sentence)

    data_gen.add_copy_column('HandleTime__c', 'ActiveTime__c')

    data_gen.add_formula_column('OriginalQueue.DeveloperName', [
        'GeneralQueue',
        'InternationalQueue',
        'Knowledge_Translations',
        'Social_Queue',
        'TargetCampaign',
        'Tier1Queue',
        'Tier2Queue',
        'Tier3Queue'
    ])

    data_gen.add_formula_column('PushTimeout__c', lambda: randint(0, 100))


    def push_timeout_date_formula(column_values):
        create_date = dateutil.parser.parse(column_values['CreatedDate__c'])
        return create_date + timedelta(seconds=column_values['PushTimeout__c'])
    data_gen.add_formula_column('PushTimeoutDateTime__c', push_timeout_date_formula)

    data_gen.add_formula_column('ServiceChannel.DeveloperName', [
        'Cases',
        'LiveMessage',
        'sfdc_liveagent',
        'Leads'
    ])

    def speed_to_answer_formula(column_values):
        request_date = dateutil.parser.parse(column_values['RequestDateTime__c'])
        accept_date = dateutil.parser.parse(column_values['AcceptDateTime__c'])
        return int((accept_date - request_date).total_seconds())
    data_gen.add_formula_column('SpeedToAnswer__c', speed_to_answer_formula)


    data_gen.add_formula_column('Status__c', [
        'Assigned',
        'Unavailable',
        'Declined',
        'Opened',
        'Closed',
        'DeclinedOnPushTimeout',
        'Canceled'
    ])

    # add a UUID for each row that is created in this batch
    data_gen.add_constant_column('analyticsdemo_batch_id__c', batch_id)

    def filter_func(column_values):
        created_date = dateutil.parser.parse(column_values['CreatedDate__c'])
        cutoff_date = reference_datetime - timedelta(days=60)
        return column_values['Origin'] == 'Chat' and created_date >= cutoff_date
    data_gen.filter(filter_function=filter_func)

    data_gen.apply_transformations()

    data_gen.sort_by('RequestDateTime__c')

    output_columns = [
        'External_Id__c',
        'RequestDateTime__c',
        'CreatedDate__c',
        'AssignedDateTime__c',
        'AcceptDateTime__c',
        'CloseDateTime__c',
        'ActiveTime__c',
        'AgentCapacityWhenDeclined__c',
        'CancelDateTime__c',
        'CapacityPercentage__c',
        'CapacityWeight__c',
        'DeclineDateTime__c',
        'DeclineReason__c',
        'HandleTime__c',
        'OriginalQueue.DeveloperName',
        'PushTimeout__c',
        'PushTimeoutDateTime__c',
        'ServiceChannel.DeveloperName',
        'SpeedToAnswer__c',
        'Status__c',
        'User.External_Id__c',
        'Case.External_Id__c',
        'analyticsdemo_batch_id__c'
    ]
    return data_gen.write(output_file_name, output_columns, 6000)


if __name__ == "__main__":
    # execute only if running as a script
    run('1', 'data/output/Case.csv', 'data/output/AgentWork.csv')
