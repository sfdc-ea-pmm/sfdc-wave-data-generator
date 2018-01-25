import copy_data_file
import dateutil.parser
import definitions
import oppty_account_cleanup
import oppty_account_gen
import oppty_case_gen
import oppty_contact_gen
import oppty_event_gen
import oppty_history_gen
import oppty_gen
import oppty_lead_gen
import oppty_line_item_gen
import oppty_product_gen
import oppty_forecasting_quota_gen
import oppty_forecasting_user_gen
import oppty_quota_gen
import oppty_shape_gen
import oppty_task_gen
import oppty_user_gen
import os

from datetime import date
from datetime import datetime
from datetime import timedelta


def run():
    today = date.today()
    today_datetime = datetime.combine(today, datetime.min.time())
    output_path = definitions.oppty_temporal_path.format(today.isoformat())

    batch_id = datetime.now().strftime("%Y%m%d%-H%M%S%f")

    # make output directory if it doesn't exist
    if os.environ.get('WRITE_MODE') != 'S3' and not os.path.exists(output_path):
        os.makedirs(output_path)

    # generate opportunity shape
    oppty_shape_file = output_path + 'OpportunityShape.csv'
    oppty_shape_gen.run(batch_id, definitions.source_oppty_shape, oppty_shape_file, today_datetime)

    # generate temporal opportunity shape
    oppty_file = output_path + 'Opportunity.csv'
    cutoff_date = today_datetime - timedelta(days=365 * 2)
    oppty_shape_gen.run(batch_id, oppty_shape_file, oppty_file, today_datetime,
                        lambda cv: dateutil.parser.parse(cv['CreatedDate__c']) >= cutoff_date)

    # generate accounts
    account_file = output_path + 'Account.csv'
    oppty_account_gen.run(batch_id, oppty_file, account_file)

    # generate contacts
    contact_file = output_path + 'Contact.csv'
    oppty_contact_gen.run(batch_id, account_file, contact_file)

    # generate users
    user_file = output_path + 'User.csv'
    manager_file = output_path + 'Manager.csv'
    oppty_user_gen.run(batch_id, oppty_file, user_file, manager_file)

    # generate forecasting quota
    forecasting_quota_file = output_path + 'ForecastingQuota.csv'
    oppty_forecasting_quota_gen.run(batch_id, user_file, forecasting_quota_file)

    # generate forecasting quota
    forecasting_user_file = output_path + 'ForecastingUser.csv'
    oppty_forecasting_user_gen.run(batch_id, user_file, forecasting_user_file)

    # generate quota
    quota_file = output_path + 'Quota.csv'
    oppty_quota_gen.run(batch_id, user_file, quota_file)

    # generate cases
    case_file = output_path + 'Case.csv'
    oppty_case_gen.run(batch_id, account_file, case_file)

    # generate products and pricebook entries
    product_file = output_path + 'Product2.csv'
    pricebook_file = output_path + 'PricebookEntry.csv'
    oppty_product_gen.run(batch_id, oppty_file, product_file, pricebook_file)

    # generate opportunity line items
    line_item_file = output_path + 'OpportunityLineItem.csv'
    oppty_line_item_gen.run(batch_id, oppty_file, line_item_file, product_file, pricebook_file)

    # generate opportunity history
    history_file = output_path + 'OpportunityHistory.csv'
    oppty_history_gen.run(batch_id, oppty_file, history_file, today_datetime)

    # generate events
    event_file = output_path + 'Event.csv'
    oppty_event_gen.run(batch_id, oppty_file, event_file, today_datetime)

    # generate tasks
    task_file = output_path + 'Task.csv'
    oppty_task_gen.run(batch_id, oppty_file, task_file, today_datetime)

    # generate leads
    lead_file = output_path + 'Lead.csv'
    oppty_lead_gen.run(batch_id, oppty_file, lead_file, account_file, contact_file)

    # generate opportunities
    oppty_file = output_path + 'Opportunity.csv'
    oppty_gen.run(batch_id, oppty_file, oppty_file)

    # clean up accounts
    oppty_account_cleanup.run(account_file, account_file)

    # copy all files to the latest folder
    latest_output_path = definitions.oppty_latest_path

    if os.environ.get('WRITE_MODE') != 'S3' and not os.path.exists(latest_output_path):
        os.makedirs(latest_output_path)

    latest_oppty_shape_file = latest_output_path + 'OpportunityShape.csv'
    copy_data_file.run(oppty_shape_file, latest_oppty_shape_file)

    latest_oppty_file = latest_output_path + 'Opportunity.csv'
    copy_data_file.run(oppty_file, latest_oppty_file)

    latest_account_file = latest_output_path + 'Account.csv'
    copy_data_file.run(account_file, latest_account_file)

    latest_contact_file = latest_output_path + 'Contact.csv'
    copy_data_file.run(contact_file, latest_contact_file)

    latest_user_file = latest_output_path + 'User.csv'
    copy_data_file.run(user_file, latest_user_file)

    latest_manager_file = latest_output_path + 'Manager.csv'
    copy_data_file.run(manager_file, latest_manager_file)

    latest_forecasting_quota_file = latest_output_path + 'ForecastingQuota.csv'
    copy_data_file.run(forecasting_quota_file, latest_forecasting_quota_file)

    latest_forecasting_user_file = latest_output_path + 'ForecastingUser.csv'
    copy_data_file.run(forecasting_user_file, latest_forecasting_user_file)

    latest_quota_file = latest_output_path + 'Quota.csv'
    copy_data_file.run(quota_file, latest_quota_file)

    latest_case_file = latest_output_path + 'Case.csv'
    copy_data_file.run(case_file, latest_case_file)

    latest_product_file = latest_output_path + 'Product2.csv'
    copy_data_file.run(product_file, latest_product_file)

    latest_pricebook_file = latest_output_path + 'PricebookEntry.csv'
    copy_data_file.run(pricebook_file, latest_pricebook_file)

    latest_line_item_file = latest_output_path + 'OpportunityLineItem.csv'
    copy_data_file.run(line_item_file, latest_line_item_file)

    latest_history_file = latest_output_path + 'OpportunityHistory.csv'
    copy_data_file.run(history_file, latest_history_file)

    latest_event_file = latest_output_path + 'Event.csv'
    copy_data_file.run(event_file, latest_event_file)

    latest_task_file = latest_output_path + 'Task.csv'
    copy_data_file.run(task_file, latest_task_file)

    latest_lead_file = latest_output_path + 'Lead.csv'
    copy_data_file.run(lead_file, latest_lead_file)

if __name__ == "__main__":
    # execute only if running as a script
    run()
