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


    # generate a random number of events per opportunity
    data_gen.duplicate_rows(duplication_factor=lambda: randint(1, 3))


    data_gen.add_formula_column('External_Id__c', formula=lambda: 'W_Sales_Event.' + str(data_gen.current_row + 1))


    data_gen.add_formula_column('Subject', formula=event.event_subject)
    data_gen.add_formula_column('EventSubtype', formula=event.event_subtype)
    data_gen.add_formula_column('DurationInMinutes', formula=event.event_call_duration)

    is_first = True
    def create_date_formula(column_values):
        oppty_create_date = dateutil.parser.parse(column_values['CreatedDate__c'])
        oppty_last_activity_date = dateutil.parser.parse(column_values['ActivityDate'])
        nonlocal is_first
        if is_first:
            create_date = oppty_last_activity_date
        else:
            create_date = fake.date_time_between_dates(oppty_create_date, oppty_last_activity_date)
        is_first = False
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
    data_gen.write(output_file_name)


if __name__ == "__main__":
    # execute only if running as a script
    run('1', 'data/output/OpportunityShape.csv', 'data/output/Event.csv')
