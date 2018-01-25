import dateutil.parser
import definitions

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
    source_columns = [
        'External_Id__c',
        'Owner.External_Id__c',
        'CreatedDate__c',
        'ClosedDate__c',
        'Origin'
    ]
    data_gen.load_source_file(source_file_name, source_columns)

    data_gen.rename_column('External_Id__c', 'Case.External_Id__c')
    data_gen.rename_column('ClosedDate__c', 'EndTime__c')

    data_gen.duplicate_rows(duplication_factor=lambda: choice([1, 2, 3, 4, 5], p=[.65, .15, .10, .05, .05]))

    data_gen.add_formula_column('External_Id__c', lambda: 'W_LiveChatTranscript.' + str(data_gen.current_row + 1))

    data_gen.add_formula_column('Abandoned__c', lambda: randint(1, 300))

    data_gen.add_formula_column('AverageResponseTimeOperator__c', lambda: randint(1, 180))

    data_gen.add_formula_column('AverageResponseTimeVisitor__c', lambda: randint(1, 180))

    data_gen.add_formula_column('Body__c', formula=fake.body)

    data_gen.add_formula_column('Browser__c', formula=fake.browser)

    data_gen.add_constant_column('BrowserLanguage__c', 'en_US')

    data_gen.add_formula_column('ChatDuration__c', lambda: randint(1, 600))

    data_gen.add_formula_column('ChatKey__c', formula=fake.md5)

    data_gen.add_formula_column('IpAddress__c', formula=fake.ipv4)

    data_gen.add_formula_column('LiveChatButton.DeveloperName',
                                ['Public_Website_Chat_Button'])

    data_gen.add_formula_column('Location__c', formula=fake.city)


    data_gen.add_formula_column('MaxResponseTimeOperator__c', lambda: randint(1, 120))

    data_gen.add_formula_column('MaxResponseTimeVisitor__c', lambda: randint(1, 240))

    data_gen.add_formula_column('Name__c', lambda: str(data_gen.current_row + 1).zfill(8))

    data_gen.add_formula_column('OperatorMessageCount__c', lambda: randint(1, 100))

    data_gen.add_formula_column('Platform__c', ['MacOSX', 'iOS', 'Android', 'Windows', 'Unix'])

    referrer = [
        "https://na17.salesforce.com/setup/forcecomHomepage.apexp?setupid=ForceCom&retURL=%2Fui%2Fsupport%2Fservicedesk%2FServiceDeskPage",
        "https://na13.salesforce.com/home/home.jsp",
        "https://sdodemo-main.force.com/partners/servlet/servlet.Integration?lid=01ra0000001VlbA&ic=1",
        "https://sitestudio.na17.force.com/?exitURL=%2F_ui%2Fnetworks%2Fsetup%2FSetupNetworksPage%2Fd",
        "https://mail.google.com/mail/u/0/",
        "https://sdodemo-main.force.com/customers/servlet/servlet.Integration?lid=01ra0000001VlbP&ic=1",
        "https://sdodemo-main.force.com/consumers/servlet/servlet.Integration?lid=01ro0000000EN78&ic=1",
        "https://na17.salesforce.com/servlet/servlet.su?oid=00D300000007EfQ&retURL=%2F0033000000PuxU2&sunetworkuserid=005a000000AuCha&sunetworkid=0DBo0000000Gn4h",
        "https://sdodemo-main.force.com/customers/servlet/servlet.Integration?ic=1&lid=01ra0000001VlbP"
    ]
    data_gen.add_formula_column('ReferrerUri__c', referrer)

    def create_date_formula(column_values):
        case_create_date = dateutil.parser.parse(column_values['CreatedDate__c'])
        case_close_date = dateutil.parser.parse(column_values['EndTime__c'])
        create_date = fake.date_time_between_dates(case_create_date, case_close_date)
        if create_date > reference_datetime:
            create_date = reference_datetime
        return create_date.isoformat(sep=' ')
    data_gen.add_formula_column('CreatedDate__c', create_date_formula)


    def start_time_formula(column_values):
        create_date = dateutil.parser.parse(column_values['CreatedDate__c'])
        start_time = create_date + timedelta(seconds=randint(1, 300))
        return start_time.isoformat(sep=' ')
    data_gen.add_formula_column('StartTime__c', start_time_formula)


    def end_time_formula(column_values):
        create_date = dateutil.parser.parse(column_values['StartTime__c'])
        end_time = create_date + timedelta(seconds=randint(1, 600))
        return end_time.isoformat(sep=' ')
    data_gen.add_formula_column('EndTime__c', end_time_formula)

    data_gen.add_copy_column('RequestTime__c', 'CreatedDate__c')

    data_gen.add_formula_column('Status__c', lambda: choice(['Missed', 'Completed'], p=[.20, .80]))

    data_gen.add_map_column('EndedBy__c', 'Status__c', {
        'Completed': ['Visitor', 'Agent'],
        None: 'Visitor'
    })

    data_gen.add_constant_column('SupervisorTranscriptBody__c', '')

    data_gen.add_constant_column('ScreenResolution__c', '')

    data_gen.add_formula_column('UserAgent__c', formula=fake.user_agent)

    data_gen.add_formula_column('VisitorMessageCount__c', lambda: randint(1, 50))

    data_gen.add_formula_column('WaitTime__c', lambda: randint(1, 120))

    def last_referenced_date_formula(column_values):
        create_date = dateutil.parser.parse(column_values['CreatedDate__c'])
        last_referenced_date = create_date + timedelta(seconds=randint(1, 300))
        return last_referenced_date.isoformat(sep=' ')
    data_gen.add_formula_column('LastReferencedDate__c', last_referenced_date_formula)


    data_gen.add_copy_column('LastViewedDate__c', 'LastReferencedDate__c')

    # add a UUID for each row that is created in this batch
    data_gen.add_constant_column('analyticsdemo_batch_id__c', batch_id)

    def filter_func(column_values):
        return column_values['Origin'] == 'Chat'
    data_gen.filter(filter_function=filter_func)

    # apply transformations and write file
    data_gen.apply_transformations()

    data_gen.sort_by('StartTime__c')

    output_columns = [
        'External_Id__c',
        'Abandoned__c',
        'AverageResponseTimeOperator__c',
        'MaxResponseTimeOperator__c',
        'OperatorMessageCount__c',
        'Body__c',
        'Browser__c',
        'BrowserLanguage__c',
        'Case.External_Id__c',
        'ChatDuration__c',
        'ChatKey__c',
        'CreatedDate__c',
        'StartTime__c',
        'EndTime__c',
        'EndedBy__c',
        'LastReferencedDate__c',
        'LastViewedDate__c',
        'LiveChatButton.DeveloperName',
        'Location__c',
        'Owner.External_Id__c',
        'Platform__c',
        'ReferrerUri__c',
        'ScreenResolution__c',
        'RequestTime__c',
        'Status__c',
        'SupervisorTranscriptBody__c',
        'UserAgent__c',
        'AverageResponseTimeVisitor__c',
        'IpAddress__c',
        'MaxResponseTimeVisitor__c',
        'VisitorMessageCount__c',
        'WaitTime__c',
        'analyticsdemo_batch_id__c'
    ]
    data_gen.write(output_file_name, output_columns)


if __name__ == "__main__":
    # execute only if running as a script
    run('1', definitions.case_data, definitions.case_livechat_transcripts)


