import copy_data_file
import dateutil.parser
import definitions
import os

from sales_service import oppty_account_cleanup
from sales_service import oppty_history_gen
from sales_service import oppty_gen
from sales_service import oppty_lead_gen
from sales_service import oppty_line_item_gen
from sales_service import oppty_product_gen
from sales_service import oppty_forecasting_quota_gen
from sales_service import oppty_forecasting_user_gen
from sales_service import oppty_quota_gen
from sales_service import oppty_shape_gen

from sales_service import case_agent_work_gen
from sales_service import case_article_gen
from sales_service import case_history_gen
from sales_service import case_knowledge_article_gen
from sales_service import case_knowledge_article_data_cat_gen
from sales_service import case_knowledge_article_version_gen
from sales_service import case_knowledge_article_viewstat_gen
from sales_service import case_knowledge_article_votestat_gen
from sales_service import case_live_chat_event_gen
from sales_service import case_live_chat_gen
from sales_service import case_shape_gen
from sales_service import case_user_presence_gen

from sales_service import ss_account_gen
from sales_service import ss_contact_gen
from sales_service import ss_case_gen
from sales_service import ss_user_gen

from sales_service import sales_event_gen
from sales_service import sales_task_gen
from sales_service import service_event_gen
from sales_service import service_task_gen

from datetime import date
from datetime import datetime
from datetime import timedelta
from data_generator import DataGenerator

def run():
    data_gen = DataGenerator()
    today = date.today()
    today_datetime = datetime.combine(today, datetime.min.time())
    output_path = definitions.ss_oppty_temporal_path.format(today.isoformat())

    batch_id = datetime.now().strftime("%Y%m%d%-H%M%S%f")

    # make output directory if it doesn't exist
    if os.environ.get('WRITE_MODE') != 'S3' and not os.path.exists(output_path):
        os.makedirs(output_path)

    # generate opportunity shape
    oppty_shape_file = output_path + 'OpportunityShape.csv'
    oppty_shape_gen.run(batch_id, definitions.ss_source_oppty_shape, oppty_shape_file, today_datetime)

    # generate temporal opportunity shape
    oppty_file = output_path + 'Opportunity.csv'
    cutoff_date = today_datetime - timedelta(days=365 * 2)
    oppty_shape_gen.run(batch_id, oppty_shape_file, oppty_file, today_datetime,
                        lambda cv: dateutil.parser.parse(cv['CreatedDate__c']) >= cutoff_date)

    # generate accounts
    account_file = output_path + 'Account.csv'
    ss_account_gen.run(batch_id, oppty_file, account_file)

    # generate contacts
    contact_file = output_path + 'Contact.csv'
    ss_contact_gen.run(batch_id, account_file, contact_file)

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

    # generate tasks from opptys
    sales_tasks_file = output_path + 'SalesTask.csv'
    sales_task_gen.run(batch_id, oppty_file, sales_tasks_file, today_datetime)

    # generate events
    sales_event_file = output_path + 'SalesEvent.csv'
    sales_event_gen.run(batch_id, oppty_file, sales_event_file, today_datetime)

    # generate leads
    lead_file = output_path + 'Lead.csv'
    oppty_lead_gen.run(batch_id, oppty_file, lead_file, account_file, contact_file)

    # generate opportunities
    oppty_file = output_path + 'Opportunity.csv'
    oppty_gen.run(batch_id, oppty_file, oppty_file)

    # clean up accounts
    oppty_account_cleanup.run(account_file, account_file)

    # copy all files to the latest folder
    latest_output_path = definitions.ss_oppty_latest_path

    if os.environ.get('WRITE_MODE') != 'S3' and not os.path.exists(latest_output_path):
        os.makedirs(latest_output_path)

    latest_oppty_file = latest_output_path + 'Opportunity.csv'
    copy_data_file.run(oppty_file, latest_oppty_file)

    latest_account_file = latest_output_path + 'Account.csv'
    copy_data_file.run(account_file, latest_account_file)

    latest_contact_file = latest_output_path + 'Contact.csv'
    copy_data_file.run(contact_file, latest_contact_file)

    latest_product_file = latest_output_path + 'Product2.csv'
    copy_data_file.run(product_file, latest_product_file)

    latest_pricebook_file = latest_output_path + 'PricebookEntry.csv'
    copy_data_file.run(pricebook_file, latest_pricebook_file)

    latest_line_item_file = latest_output_path + 'OpportunityLineItem.csv'
    copy_data_file.run(line_item_file, latest_line_item_file)

    latest_history_file = latest_output_path + 'OpportunityHistory.csv'
    copy_data_file.run(history_file, latest_history_file)

    latest_sales_task_file = latest_output_path + 'SalesTask.csv'
    copy_data_file.run(sales_tasks_file, latest_sales_task_file)

    latest_sales_event_file = latest_output_path + 'SalesEvent.csv'
    copy_data_file.run(sales_event_file, latest_sales_event_file)

    latest_lead_file = latest_output_path + 'Lead.csv'
    copy_data_file.run(lead_file, latest_lead_file)

    #### section from service starts ####
    
    # generate case shape
    case_shape_file = output_path + 'CaseShape.csv'
    case_shape_gen.run(batch_id, definitions.ss_source_case_shape, case_shape_file, today_datetime)

    # generate case
    case_file = output_path + 'Case.csv'
    cutoff_date = today_datetime - timedelta(days=30 * 2)
    account_dataset = data_gen.load_dataset('account', account_file, ['External_Id__c'])
    account_ids = account_dataset.unique('External_Id__c')
    # we are going to use the same accounts that were generated for Opportunity
    ss_case_gen.run(batch_id, case_shape_file, case_file,
                        lambda cv: dateutil.parser.parse(cv['CreatedDate__c']) >= cutoff_date and cv['Account.External_Id__c'] in account_ids)

    # generate users
    user_file = output_path + 'User.csv'
    manager_file = output_path + 'Manager.csv'
    ss_user_gen.run(batch_id, case_file, user_file, manager_file)

    # generate user presence
    user_presence_file = output_path + 'UserServicePresence.csv'
    case_user_presence_gen.run(batch_id, user_file, user_presence_file)

    ###### sub section from Sales begins ######
    
    # generate forecasting quota
    forecasting_quota_file = output_path + 'ForecastingQuota.csv'
    oppty_forecasting_quota_gen.run(batch_id, user_file, forecasting_quota_file)

    # generate forecasting quota
    forecasting_user_file = output_path + 'ForecastingUser.csv'
    oppty_forecasting_user_gen.run(batch_id, user_file, forecasting_user_file)

    # generate quota
    quota_file = output_path + 'Quota.csv'
    oppty_quota_gen.run(batch_id, user_file, quota_file)
    
    ###### end of sub section from Sales ######

    # generate agent work
    agent_work_file = output_path + 'AgentWork.csv'
    agent_work_files = case_agent_work_gen.run(batch_id, case_file, agent_work_file, today_datetime)

    # generate tasks
    sales_tasks_dataset = data_gen.load_dataset('sales_tasks', sales_tasks_file, ['External_Id__c'])
    service_task_file = output_path + 'ServiceTask.csv'
    service_task_gen.run(batch_id, case_file, service_task_file, today_datetime, len(sales_tasks_dataset.data) + 1)

    # generate service tasks, from cases
    sales_events_dataset = data_gen.load_dataset('sales_events', sales_event_file, ['External_Id__c'])
    service_event_file = output_path + 'ServiceEvent.csv'
    service_event_gen.run(batch_id, case_file, service_event_file, today_datetime, len(sales_events_dataset.data) + 1)

    # generate case history
    history_file = output_path + 'CaseHistory.csv'
    case_history_gen.run(batch_id, case_file, history_file, today_datetime)

    # generate livechat transcripts
    livechat_file = output_path + 'LiveChatTranscript.csv'
    case_live_chat_gen.run(batch_id, case_file, livechat_file)

    livechat_events_file = output_path + 'LiveChatTranscriptEvent.csv'
    case_live_chat_event_gen.run(batch_id, livechat_file, livechat_events_file)

    # generate case articles
    
    article_file = output_path + 'CaseArticle.csv'
    case_article_gen.run(batch_id, case_file, article_file)

    ka_file = output_path + 'KCSArticle_ka.csv'
    case_knowledge_article_gen.run(batch_id, article_file, ka_file)

    kav_file = output_path + 'KCSArticle_kav.csv'
    case_knowledge_article_version_gen.run(batch_id, article_file, kav_file)

    ka_data_cat_file = output_path + 'KCSArticle_DataCategorySelection.csv'
    case_knowledge_article_data_cat_gen.run(batch_id, article_file, ka_data_cat_file)

    ka_votestat_file = output_path + 'KCSArticle_VoteStat.csv'
    case_knowledge_article_votestat_gen.run(batch_id, article_file, ka_votestat_file)

    ka_viewstat_file = output_path + 'KCSArticle_ViewStat.csv'
    case_knowledge_article_viewstat_gen.run(batch_id, article_file, ka_viewstat_file)

    # end of generate case articles

    # copy all files to the latest folder
    
    latest_output_path = definitions.ss_case_latest_path

    if os.environ.get('WRITE_MODE') != 'S3' and not os.path.exists(latest_output_path):
        os.makedirs(latest_output_path)

    latest_case_file = latest_output_path + 'Case.csv'
    copy_data_file.run(case_file, latest_case_file)

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

    latest_user_presence_file = latest_output_path + 'UserServicePresence.csv'
    copy_data_file.run(user_presence_file, latest_user_presence_file)

    for index, aw in enumerate(agent_work_files):
        latest_agent_work_file = latest_output_path + 'AgentWork-' + str(index) + '.csv'
        if index == 0:
            latest_agent_work_file = latest_output_path + 'AgentWork.csv'
        copy_data_file.run(aw, latest_agent_work_file)

    latest_service_task_file = latest_output_path + 'ServiceTask.csv'
    copy_data_file.run(service_task_file, latest_service_task_file)

    latest_service_event_file = latest_output_path + 'ServiceEvent.csv'
    copy_data_file.run(service_event_file, latest_service_event_file)

    latest_history_file = latest_output_path + 'CaseHistory.csv'
    copy_data_file.run(history_file, latest_history_file)

    latest_livechat_file = latest_output_path + 'LiveChatTranscript.csv'
    copy_data_file.run(livechat_file, latest_livechat_file)

    latest_livechat_events_file = latest_output_path + 'LiveChatTranscriptEvent.csv'
    copy_data_file.run(livechat_events_file, latest_livechat_events_file)

    latest_article_file = latest_output_path + 'CaseArticle.csv'
    copy_data_file.run(article_file, latest_article_file)

    latest_ka_file = latest_output_path + 'KCSArticle_ka.csv'
    copy_data_file.run(ka_file, latest_ka_file)

    latest_kav_file = latest_output_path + 'KCSArticle_kav.csv'
    copy_data_file.run(kav_file, latest_kav_file)

    latest_ka_data_cat_file = latest_output_path + 'KCSArticle_DataCategorySelection.csv'
    copy_data_file.run(ka_data_cat_file, latest_ka_data_cat_file)

    latest_ka_votestat_file = latest_output_path + 'KCSArticle_VoteStat.csv'
    copy_data_file.run(ka_votestat_file, latest_ka_votestat_file)

    latest_ka_viewstat_file = latest_output_path + 'KCSArticle_ViewStat.csv'
    copy_data_file.run(ka_viewstat_file, latest_ka_viewstat_file)

    #### section from service ends ####

if __name__ == "__main__":
    # execute only if running as a script
    run()
