import definitions

from data_generator import DataGenerator
from numpy.random import choice
from numpy.random import lognormal
from numpy.random import randint
from numpy import mean
from numpy import std


def run(source_file_name, output_file_name):
    data_gen = DataGenerator()

    # load source file
    data_gen.load_source_file(source_file_name)

    # find mean and std of profit
    profits = []
    for row in data_gen.rows:
        column_values = data_gen.row_to_column_values(row)
        profits.append(float(column_values['Profit']))


    profit_mean = mean(profits)
    profit_std = std(profits)

    # filter out profits more than 2 std out.
    def filter_func(column_values):
        profit = float(column_values['Profit'])
        z_score = abs((profit - profit_mean) / profit_std)
        return z_score <= 2
    data_gen.filter(filter_function=filter_func)


    store_tier_map = {
        'New York 4': "Tier 1",
        'New York 3': "Tier 1",
        'New York 2': "Tier 1",
        'New York 1': "Tier 1",
        'Chicago 3': "Tier 1",
        'Chicago 2': "Tier 2",
        'Chicago 1': "Tier 2",
        'Boston 2': "Tier 2",
        'Boston 1': "Tier 3"
    }
    data_gen.add_map_column('Tier', 'Store', store_tier_map)


    month_channel_map = {
        'January': 'Chat',
        'February': 'Chat',
        'March': 'Chat',
        'April': 'Chat',
        'May': 'Chat',
        'June': 'Email',
        'July': 'Email',
        'August': 'Facebook',
        'September': 'Phone',
        'October': 'Phone',
        'November': 'Website',
        'December': 'Website'
    }
    data_gen.add_map_column('Origin', 'Month', month_channel_map)


    discount_support_map = {
        '0': 'Free',
        '0.05': 'Free',
        '0.15': 'Basic',
        '0.1': 'Silver',
        '0.2': 'Platinum'
    }
    data_gen.add_map_column('Type_of_Support__c', 'Discount', discount_support_map)


    camp_reason_map = {
        "Bundled": "Documentation",
        "Buy More & Save": "Unknown Failure",
        "Competitor Focus": "Feature Question",
        "Door Buster": "Hardware Question",
        "Friends & Family": "Late Delivery",
        "Local": "Software Question",
        "Paper Circular": "General Question",
        "Regional": "Item Damaged",
        "Social": "Item Damaged"
    }
    data_gen.add_map_column('Reason', 'Marketing Campaign', camp_reason_map)


    city_priority_map = {
        "Boston": "Low",
        "Chicago": "Medium",
        "New York": "High"
    }
    data_gen.add_map_column('Priority', 'City', city_priority_map)


    comp_sla_map = {
        "High": "Violation",
        "Normal": "Compliant",
        "Low": "Compliant"
    }
    data_gen.add_map_column('SLA', 'Competition', comp_sla_map)


    data_gen.add_constant_column('Status', 'Closed')


    sla_first_contact_close_map = {
        'Compliant': lambda: choice(['true', 'false'], p=[.9, .1]),
        'Violation': lambda: choice(['true', 'false'], p=[.7, .3])
    }
    data_gen.add_map_column('First_Contact_Close__c', 'SLA', sla_first_contact_close_map)


    sla_time_open_map = {
        'Compliant': lambda: choice([12, 24, 36, 48], p=[.50, .20, .20, .10]),
        'Violation': lambda: choice([60, 72, 84, 96, 108, 120], p=[.60, .20, .10, .05, .03, .02])
    }
    data_gen.add_map_column('Time_Open__c', 'SLA', sla_time_open_map)


    def region_formula(column_values):
        average_age = float(column_values['Average Age'])
        if average_age < 40:
            return 'West CSR'
        elif average_age >= 40.0 and average_age < 50:
            return 'Central CSR'
        else:
            return 'East CSR'
    data_gen.add_formula_column('Team__c', region_formula)


    def user_formula(column_values):
        average_age = float(column_values['Average Age'])
        if average_age < 40:
            return 'W_Services_User.' + str(choice([1, 2, 3, 4, 5]))
        elif average_age >= 40.0 and average_age < 50:
            return 'W_Services_User.' + str(choice([6, 7, 8, 9, 10, 11]))
        else:
            return 'W_Services_User.' + str(choice([12, 13, 14, 15, 16, 17]))
    data_gen.add_formula_column('Owner.External_Id__c', user_formula)


    # generate offer voucher - give vouchers to customers that were unhappy with Video Games or Cables to boost CSAT
    def offer_voucher_formula(column_values):
        csat = float(column_values['Profit Linear'])
        item = column_values['Item']

        if item in ['Video Games', 'Cables']:
            return choice(['true', 'false'], p=[csat/100, (100 - csat) / 100])
        else:
            return 'false'
    data_gen.add_formula_column('Offer_Voucher__c', offer_voucher_formula)


    def send_field_service_formula(column_values):
        csat = float(column_values['Profit Linear'])
        item = column_values['Item']

        if csat >= 80.0 and item == 'Tablet':
            return 'true'
        else:
            return choice(['true', 'false'], p=[.25, .75])
    data_gen.add_formula_column('Send_FieldService__c', send_field_service_formula)

    data_gen.add_map_column('IsEscalated', 'Tier', {'Tier 1': 'true', None: 'false'})

    # generate close date offset
    # random offset covering the last 14 months
    data_gen.add_formula_column('close_date_offset', lambda: randint(1, 30 * 14))


    # generate account id - generate a long tail distribution - cubic function +- randint
    # helper dataset used for account selection
    data_gen.add_dataset('current_account', {'account_id': 0, 'account_count': 0})


    # generate a distribution of account ids
    def account_id_formula(column_values):
        current_account = data_gen.datasets['current_account']
        account_id = current_account['account_id']
        account_count = current_account['account_count']

        if account_count > 0:
            # continue with the current account_id if there are still any to take
            # but first decrement account count
            account_count += -1
            current_account['account_count'] = account_count
        else:
            # use new account id
            account_id += 1
            account_count = int(round(lognormal(1))) + randint(1, 7)

            # update account dataset for next iteration
            account_count += -1
            current_account['account_count'] = account_count
            current_account['account_id'] = account_id
        return 'W_Services_Account.' + str(account_id)
    data_gen.add_formula_column('Account.External_Id__c', account_id_formula)

    def csat_formula(column_values):
        # first normalize csat between 30-90
        csat = float(column_values['Profit Linear'])
        new_delta = 70
        csat = (new_delta * csat / 100) + 30
        channel = column_values['Origin']
        is_escalated = column_values['IsEscalated']
        send_field_service = column_values['Send_FieldService__c']
        offer_voucher = column_values['Offer_Voucher__c']

        if is_escalated == 'true':
            if channel == 'Phone':
                csat = csat - 2
            else:
                csat = csat + 2

        if send_field_service == 'true':
            if channel == 'Phone':
                csat = csat - 2
            else:
                csat = csat + 4

        if offer_voucher == 'true':
            if channel == 'Phone':
                csat = csat - 2
            else:
                csat = csat + 4

        return csat
    data_gen.add_formula_column('CSAT__c', formula=csat_formula)

    data_gen.add_map_column('Outlier', 'Outlier', value_map={
        'TRUE': 'true',
        None: 'false'
    })

    data_gen.apply_transformations()


    data_gen.add_map_column('Time_Open__c', 'First_Contact_Close__c', value_map={
        'true': 0,
        None: lambda cv: cv['Time_Open__c']
    })

    data_gen.apply_transformations()

    rename_map = {
        'Item': 'Product_Family_KB__c'
    }
    data_gen.rename_columns(rename_map)

    output_columns = [
        'Origin',
        'Store',
        'Tier',
        'Product_Family_KB__c',
        'Priority',
        'Average Age',
        'Percent Male',
        'SLA',
        'Daily Revenue',
        'Reason',
        'Reg Price',
        'Type_of_Support__c',
        'Price',
        'Quantity',
        'Cost',
        'Profit',
        'CSAT__c',
        'Profit Log',
        'Outlier',
        'Status',
        'First_Contact_Close__c',
        'Time_Open__c',
        'Team__c',
        'Owner.External_Id__c',
        'close_date_offset',
        'Account.External_Id__c',
        'Offer_Voucher__c',
        'Send_FieldService__c',
        'IsEscalated'
    ]
    data_gen.write(output_file_name, output_columns)


if __name__ == "__main__":
    # execute only if running as a script
    run(definitions.source_case_data, definitions.source_case_shape)