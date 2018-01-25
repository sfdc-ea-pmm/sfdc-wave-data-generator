import dateutil.parser
import definitions

from data_generator import DataGenerator
from datetime import date
from datetime import datetime
from datetime import timedelta
from random import randint

today = date.today()
today_datetime = datetime.combine(today, datetime.min.time())

def run(batch_id, source_file_name, output_file_name, reference_datetime=today_datetime):
    case_status = ['Escalated', 'Waiting on Customer', 'On Hold', 'Working']

    data_gen = DataGenerator()

    # load source file
    source_columns = [
        'External_Id__c',
        'Owner.External_Id__c',
        'CreatedDate__c',
        'ClosedDate__c',
        'First_Contact_Close__c',
        'Status'
    ]
    data_gen.load_source_file(source_file_name, source_columns)

    data_gen.rename_column('External_Id__c', 'Case.External_Id__c')
    data_gen.rename_column('Owner.External_Id__c', 'CreatedById__c')

    data_gen.add_formula_column('External_Id__c', '')

    data_gen.add_constant_column('Field__c', 'created')
    data_gen.add_constant_column('OldValue__c', '')
    data_gen.add_constant_column('NewValue__c', '')

    # add a UUID for each row that is created in this batch
    data_gen.add_constant_column('analyticsdemo_batch_id__c', batch_id)

    data_gen.apply_transformations()

    current_count = 1
    new_rows = []
    row_count = len(data_gen.rows)
    for i in range(row_count):
        row = data_gen.rows.pop()
        column_values = data_gen.row_to_column_values(row)

        column_values['External_Id__c'] = 'W_CaseHistory.' + str(current_count)
        current_count += 1
        case_id = column_values['Case.External_Id__c']
        created_by = column_values['CreatedById__c']
        created_date = dateutil.parser.parse(column_values['CreatedDate__c'])
        closed_date = dateutil.parser.parse(column_values['ClosedDate__c'])
        if closed_date > reference_datetime:
            closed_date = reference_datetime

        first_contact_close = column_values['First_Contact_Close__c']
        status = column_values['Status']

        # include initial created row
        new_rows.append(data_gen.column_values_to_row(column_values))

        # include new status
        new_column_values = {
            'External_Id__c': 'W_CaseHistory.' + str(current_count),
            'Case.External_Id__c': case_id,
            'CreatedById__c': created_by,
            'CreatedDate__c': created_date,
            'Field__c': 'Status',
            'OldValue__c': '',
            'NewValue__c': 'New',
            'ClosedDate__c': '',
            'First_Contact_Close__c': ''
        }
        new_rows.append(data_gen.column_values_to_row(new_column_values))
        current_count += 1

        old_value = 'New'
        next_event_date = created_date

        while next_event_date <= closed_date:
            next_event_date = next_event_date + timedelta(days=randint(0, 30))

            if first_contact_close == 'true' and status == 'Closed':
                next_event_date = closed_date
                new_column_values = {
                    'External_Id__c': 'W_CaseHistory.' + str(current_count),
                    'Case.External_Id__c': case_id,
                    'CreatedById__c': created_by,
                    'CreatedDate__c': next_event_date,
                    'Field__c': 'Status',
                    'OldValue__c': old_value,
                    'NewValue__c': 'Closed',
                    'ClosedDate__c': '',
                    'First_Contact_Close__c': ''
                }
                new_rows.append(data_gen.column_values_to_row(new_column_values))
                current_count += 1
                break
            elif next_event_date >= closed_date:
                next_event_date = closed_date
                new_column_values = {
                    'External_Id__c': 'W_CaseHistory.' + str(current_count),
                    'Case.External_Id__c': case_id,
                    'CreatedById__c': created_by,
                    'CreatedDate__c': next_event_date,
                    'Field__c': 'Status',
                    'OldValue__c': old_value,
                    'NewValue__c': status,
                    'ClosedDate__c': '',
                    'First_Contact_Close__c': ''
                }
                new_rows.append(data_gen.column_values_to_row(new_column_values))
                current_count += 1
                break
            else:
                new_value = case_status[randint(0, len(case_status) - 1)]

                while old_value == new_value:
                    new_value = case_status[randint(0, len(case_status) - 1)]

                new_column_values = {
                    'External_Id__c': 'W_CaseHistory.' + str(current_count),
                    'Case.External_Id__c': case_id,
                    'CreatedById__c': created_by,
                    'CreatedDate__c': next_event_date,
                    'Field__c': 'Status',
                    'OldValue__c': old_value,
                    'NewValue__c': new_value,
                    'ClosedDate__c': '',
                    'First_Contact_Close__c': '',
                    'analyticsdemo_batch_id__c': batch_id
                }
                new_rows.append(data_gen.column_values_to_row(new_column_values))
                old_value = new_value
                current_count += 1

    data_gen.rows = new_rows
    data_gen.reverse()

    output_columns = [
        'External_Id__c',
        'Case.External_Id__c',
        'CreatedById__c',
        'CreatedDate__c',
        'Field__c',
        'OldValue__c',
        'NewValue__c',
        'analyticsdemo_batch_id__c'
    ]
    data_gen.write(output_file_name, output_columns)


if __name__ == "__main__":
    # execute only if running as a script
    run(definitions.case_data, definitions.case_history)
