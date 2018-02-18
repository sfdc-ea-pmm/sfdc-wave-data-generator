import dateutil.parser
import definitions

from data_generator import DataGenerator
from data_generator.formula import account
from data_generator.formula import fake
from datetime import date
from datetime import datetime
from datetime import timedelta
from numpy.random import choice
from numpy.random import chisquare
from numpy.random import lognormal
from numpy.random import randint

today = date.today()
today_datetime = datetime.combine(today, datetime.min.time())


def run(source_file_name, output_file_name):
    data_gen = DataGenerator()


    # load source file
    data_gen.load_source_file(source_file_name)


    rename_map = {
        'Supplies Group': 'Product2Family__c',
        'Region': 'Region__c',
        'Route To Market': 'LeadSource',
        'Elapsed Days In Sales Stage': 'TimeToClose__c',
        'Sales Stage Change Count': 'SalesStageCount__c',
        'Opportunity Amount USD': 'Amount',
        'Deal Size Category': 'DealSizeCategory__c'
    }
    data_gen.rename_columns(rename_map)

    # multiple time to close by 2
    data_gen.add_formula_column('TimeToClose__c', lambda cv: int(cv['TimeToClose__c']) * 2)


    # map existing columns to new columns
    data_gen.add_map_column('Competitor__c', 'Competitor Type', definitions.competitor_type)
    data_gen.add_map_column('Product2Name__c', 'Supplies Subgroup', definitions.supplies_subgroup_map)
    data_gen.add_map_column('AccountAnnualRevenue__c', 'Client Size By Revenue', definitions.client_size_rev)
    data_gen.add_map_column('AccountNumberOfEmployees__c', 'Client Size By Employee Count',
                            definitions.client_size_employees)
    data_gen.add_map_column('AccountBookings__c', 'Revenue From Client Past Two Years', definitions.client_past_revenue)
    data_gen.add_map_column('IsWon', 'Opportunity Result', definitions.isWon)


    # generate external id
    data_gen.add_formula_column('External_Id__c', formula=lambda: 'W_Opportunity.' + str(data_gen.current_row + 1))


    data_gen.add_formula_column('Exec_Meeting__c', lambda: choice(['true', 'false'], p=[.35, .65]))

    data_gen.add_formula_column('Interactive_Demo__c', lambda: choice(['true', 'false'], p=[.30, .70]))

    def ttc_formula(column_values):
        ttc = int(column_values['TimeToClose__c'])
        exec_meeting = column_values['Exec_Meeting__c']
        competitor_type = column_values['Competitor Type']
        demo = column_values['Interactive_Demo__c']
        rev = column_values['AccountAnnualRevenue__c']

        if ttc == 0:
            return 0

        if exec_meeting == 'true':
            if competitor_type == 'None':
                ttc = ttc + 4
            else:
                ttc = ttc - 6
        if demo == 'true':
            if rev == 'T100':
                ttc = ttc + 6
            else:
                ttc = ttc - 5

        if ttc < 0:
            return 0

        return ttc
    data_gen.add_formula_column('TimeToClose__c', formula=ttc_formula)


    data_gen.add_constant_column('IsClosed', 'true')


    data_gen.add_formula_column('RecordType.DeveloperName', formula=lambda: choice(['SimpleOpportunity', 'ChannelPartner'], p=[1, 0]))


    # generate opportunity type
    types = ['Add-On Business', 'Existing Business', 'New Business', 'New Business / Add-on']
    data_gen.add_formula_column('Type', formula=lambda: choice(types, p=[0.1, 0.3, 0.5, 0.1]))


    # generate a close date year and quarter
    data_gen.add_formula_column('close_date_year', formula=lambda: choice(list(range(0, 30))))
    data_gen.add_formula_column('close_date_quarter', formula=lambda: choice([1, 2, 3, 4], p=[0.21, 0.24, 0.22, 0.33]))


    # generate a close date offset from the year and quarter
    def offset_formula(column_values):
        day = int(round(chisquare(9) * 5))
        offset = 365 * (column_values['close_date_year']) + 91 * (column_values['close_date_quarter'] - 1) + day
        return offset
    data_gen.add_formula_column('close_date_offset__c', offset_formula)


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
        create_date = dateutil.parser.parse(column_values['CreatedDate__c'])
        close_date = dateutil.parser.parse(column_values['CloseDate'])
        if close_date > today_datetime:
            close_date = today_datetime
        if create_date > today_datetime:
            create_date = today_datetime
        return fake.date_time_between_dates(create_date, close_date).date()
    data_gen.add_formula_column('LastActivityDate__c', formula=last_activity_date_formula)


    # generate StageName, ForecastCategory, and Probability
    data_gen.add_map_column('StageName', 'Opportunity Result', value_map={'Won': 'Closed Won', None: 'Closed Lost'})
    data_gen.add_map_column('ForecastCategory', 'Opportunity Result', value_map={'Won': 'Closed', None: 'Omitted'})
    data_gen.add_map_column('ForecastCategoryName', 'Opportunity Result', value_map={'Won': 'Closed', None: 'Omitted'})
    data_gen.add_map_column('Probability', 'Opportunity Result', value_map={'Won': '100', None: '0'})

    # randomly pick an owner from the same region
    region_territory_map = {
        'Pacific': lambda: 'W_Sales_User.' + str(choice([1, 2, 3, 4, 5, 6])),
        "Northwest": lambda: 'W_Sales_User.' + str(choice([1, 2, 3, 4, 5, 6])),
        "Midwest": lambda: 'W_Sales_User.' + str(choice([7, 8, 9, 10, 11])),
        "Southwest": lambda: 'W_Sales_User.' + str(choice([7, 8, 9, 10, 11])),
        "Mid-Atlantic": lambda: 'W_Sales_User.' + str(choice([7, 8, 9, 10, 11])),
        "Northeast": lambda: 'W_Sales_User.' + str(choice([12, 13, 14, 15, 16, 17])),
        "Southeast": lambda: 'W_Sales_User.' + str(choice([12, 13, 14, 15, 16, 17]))
    }
    data_gen.add_map_column('Owner.External_Id__c', 'Region__c', region_territory_map)


    # build out helper column for account selection
    def account_cat_formula(column_values):
        x1 = column_values['Client Size By Revenue']
        x2 = column_values['Client Size By Employee Count']
        x3 = column_values['Revenue From Client Past Two Years']
        return str(x1) + '.' + str(x2) + '.' + str(x3)
    data_gen.add_formula_column('account_cat', account_cat_formula)


    # apply pending transformations now so we can sort by account_cat
    data_gen.apply_transformations()


    data_gen.sort_by('account_cat')


    # helper dataset used for account selection
    data_gen.add_dataset('account_segment', {'account_id': 0, 'account_count': 0, 'current_account_cat': None})


    # generate a distribution of account ids
    def account_id_formula(column_values):
        account_segment = data_gen.datasets['account_segment']
        account_id = account_segment['account_id']
        account_count = account_segment['account_count']
        current_account_cat = account_segment['current_account_cat']

        if column_values['account_cat'] == current_account_cat and account_count > 0:
            # continue with the current account_id if there are still any to take
            # but first decrement account count
            account_count += -1
            account_segment['account_count'] = account_count

            return account_id
        else:
            # use new account id
            account_id += 1
            # generate a random number of opportunties to associate to an account
            account_count = int(round(lognormal(1))) + randint(1, 7)
            current_account_cat = column_values['account_cat']

            # update account segment dataset for next iteration
            account_count += -1
            account_segment['account_id'] = account_id
            account_segment['account_count'] = account_count
            account_segment['current_account_cat'] = current_account_cat

            return account_id
    data_gen.add_formula_column('AccountId__c', account_id_formula)


    # generate account id string
    data_gen.add_formula_column('AccountExternalId__c', formula=lambda cv: 'W_Account.' + str(cv['AccountId__c']))


    # generate account name string
    account_names = {}
    def account_name_formula(column_values):
        account_id = column_values['AccountId__c']
        if account_id in account_names:
            return account_names[account_id]
        else:
            account_name = account.account_name()
            account_names[account_id] = account_name
            return account_name
    data_gen.add_formula_column('AccountName__c', formula=account_name_formula)


    # generate name
    def name_formula(column_values):
        account_name = column_values['AccountName__c']
        amount = column_values['Amount']
        product_2_name = column_values['Product2Name__c']
        return account_name + ' ' + str(data_gen.current_row % 256)
    data_gen.add_formula_column('Name', name_formula)


    # apply remaining transformations
    data_gen.apply_transformations()


    # sort by account id
    data_gen.sort_by('AccountId__c')


    columns_to_write = [
        'External_Id__c',
        'Product2Name__c',
        'Product2Family__c',
        'Region__c',
        'LeadSource',
        'TimeToClose__c',
        'SalesStageCount__c',
        'Amount',
        'AccountAnnualRevenue__c',
        'AccountNumberOfEmployees__c',
        'AccountBookings__c',
        'Competitor__c',
        'DealSizeCategory__c',
        'AccountExternalId__c',
        'AccountName__c',
        'close_date_year',
        'close_date_quarter',
        'close_date_offset__c',
        'Exec_Meeting__c',
        'Interactive_Demo__c',
        'IsWon',
        'IsClosed',
        'Owner.External_Id__c',
        'Name',
        'Type',
        'StageName',
        'ForecastCategory',
        'ForecastCategoryName',
        'Probability',
        'RecordType.DeveloperName'
    ]


    data_gen.write(output_file_name, columns_to_write)


if __name__ == "__main__":
    # execute only if running as a script
    run(definitions.source_data, definitions.source_oppty_shape)
