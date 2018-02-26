import dateutil.parser
import definitions

from data_generator import DataGenerator
from data_generator.formula import fake
from data_generator.formula import task
from datetime import date
from datetime import datetime
from datetime import timedelta
from numpy.random import randint


today = date.today()
today = datetime.combine(today, datetime.min.time())


def run(batch_id, source_file_name, output_file_name, reference_datetime=today):
    data_gen = DataGenerator()


    # load source file
    source_columns = [
        'External_Id__c',
        'Owner.External_Id__c',
        'CreatedDate__c',
        'LastActivityDate__c'
    ]
    data_gen.load_source_file(source_file_name, source_columns)

    data_gen.rename_column('External_Id__c', 'What.External_Id__c')
    data_gen.rename_column('LastActivityDate__c', 'ActivityDate')


    # generate a random number of tasks per opportunity
    data_gen.duplicate_rows(duplication_factor=lambda: randint(1, 3))


    data_gen.add_formula_column('External_Id__c', formula=lambda: 'W_Sales_Task.' + str(data_gen.current_row + 1))


    data_gen.add_formula_column('TaskSubtype', formula=task.oppty_task_subtype)
    data_gen.add_formula_column('CallDurationInSeconds', formula=task.task_call_duration)
    data_gen.add_formula_column('CallDisposition', formula=task.task_call_disposition)
    data_gen.add_formula_column('CallType', formula=task.task_call_type)


    data_gen.add_formula_column('Status', formula=task.task_status)

    data_gen.add_formula_column('Priority', formula=task.task_priority)

    def create_date_formula(column_values):
        oppty_create_date = dateutil.parser.parse(column_values['CreatedDate__c'])
        oppty_last_activity_date = dateutil.parser.parse(column_values['ActivityDate'])
        create_date = fake.date_time_between_dates(oppty_create_date, oppty_last_activity_date)
        if create_date > reference_datetime:
            create_date = reference_datetime
        return create_date.isoformat(sep=' ')
    data_gen.add_formula_column('CreatedDate__c', create_date_formula)


    def activity_date_formula(column_values):
        create_date = dateutil.parser.parse(column_values['CreatedDate__c']).date()
        return (create_date + timedelta(days=randint(0, 14))).isoformat()
    data_gen.add_formula_column('ActivityDate', activity_date_formula)


    data_gen.add_formula_column('Subject', formula=task.task_subject)

    # add a UUID for each row that is created in this batch
    data_gen.add_constant_column('analyticsdemo_batch_id__c', batch_id)

    # apply transformations and write
    data_gen.apply_transformations()
    data_gen.write(output_file_name)

if __name__ == "__main__":
    # execute only if running as a script
    run('1', definitions.oppty_shape, definitions.oppty_tasks)
