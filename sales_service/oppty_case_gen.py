import dateutil.parser

from data_generator import DataGenerator
from data_generator.formula import case
from datetime import date
from datetime import datetime
from datetime import timedelta
from numpy.random import lognormal
from numpy.random import randint

today = date.today()
today = datetime.combine(today, datetime.min.time())


def run(batch_id, source_file_name, output_file_name, reference_datetime=today):
    data_gen = DataGenerator()


    # load source file
    account_columns = [
        'External_Id__c',
        'Owner.External_Id__c',
        'OpportunityCloseDate__c'
    ]
    data_gen.load_source_file(source_file_name, account_columns)

    data_gen.rename_column('External_Id__c', 'Account.External_Id__c')
    data_gen.rename_column('OpportunityCloseDate__c', 'CreatedDate__c')

    # generate a random number of cases per account
    data_gen.duplicate_rows(duplication_factor=lambda: int(lognormal(0) + randint(0, 2)))

    data_gen.add_formula_column('External_Id__c', formula=lambda: 'W_Sales_Case.' + str(data_gen.current_row + 1))

    # generate contact
    def contact_formula(column_values):
        return column_values['Account.External_Id__c'].replace('W_Account', 'W_Contact')
    data_gen.add_formula_column('Contact.External_Id__c', contact_formula)


    data_gen.add_formula_column('IsEscalated', case.case_is_escalated)
    data_gen.add_formula_column('CSAT__c', case.case_csat)

    data_gen.add_formula_column('Origin', formula=case.case_origin)
    data_gen.add_formula_column('Type', formula=case.case_type)
    data_gen.add_formula_column('Subject', formula=case.case_subject)
    data_gen.add_formula_column('Priority', formula=case.case_priority)

    data_gen.add_formula_column('Status', formula=case.case_status)


    def create_date_formula(column_values):
        oppty_close_date = dateutil.parser.parse(column_values['CreatedDate__c'])
        create_date = oppty_close_date + timedelta(days=randint(0, 90))
        if create_date > reference_datetime:
            create_date = reference_datetime
        return create_date.isoformat(sep=' ')
    data_gen.add_formula_column('CreatedDate__c', create_date_formula)


    def close_date_formula(column_values):
        create_date = dateutil.parser.parse(column_values['CreatedDate__c'])
        if column_values['Status'] == 'Closed':
            close_date = create_date + timedelta(days=randint(0, 10))
            if close_date > reference_datetime:
                close_date = reference_datetime
            return close_date.isoformat(sep=' ')
        else:
            return ''
    data_gen.add_formula_column('ClosedDate__c', close_date_formula)

    # add a UUID for each row that is created in this batch
    data_gen.add_constant_column('analyticsdemo_batch_id__c', batch_id)

    data_gen.apply_transformations()
    data_gen.write(output_file_name)


if __name__ == "__main__":
    # execute only if running as a script
    run('1', 'data/output/Account.csv', 'data/output/Case.csv')
