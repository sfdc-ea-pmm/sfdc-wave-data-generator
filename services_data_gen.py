import case_account_gen
import case_agent_work_gen
import case_article_gen
import case_contact_gen
import case_event_gen
import case_gen
import case_history_gen
import case_knowledge_article_gen
import case_knowledge_article_data_cat_gen
import case_knowledge_article_version_gen
import case_knowledge_article_viewstat_gen
import case_knowledge_article_votestat_gen
import case_live_chat_event_gen
import case_live_chat_gen
import case_oppty_gen
import case_shape_gen
import case_task_gen
import case_user_gen
import case_user_presence_gen
import copy_data_file
import dateutil.parser
import definitions
import os

from datetime import date
from datetime import datetime
from datetime import timedelta


def run():
    today = date.today()
    today_datetime = datetime.combine(today, datetime.min.time())
    output_path = definitions.case_temporal_path.format(today.isoformat())

    batch_id = datetime.now().strftime("%Y%m%d%-H%M%S%f")

    # make output directory if it doesn't exist
    if os.environ.get('WRITE_MODE') != 'S3' and not os.path.exists(output_path):
        os.makedirs(output_path)

    # generate case shape
    case_shape_file = output_path + 'CaseShape.csv'
    case_shape_gen.run(batch_id, definitions.source_case_shape, case_shape_file, today_datetime)

    # generate case
    case_file = output_path + 'Case.csv'
    cutoff_date = today_datetime - timedelta(days=30 * 2)
    case_gen.run(batch_id, case_shape_file, case_file,
                        lambda cv: dateutil.parser.parse(cv['CreatedDate__c']) >= cutoff_date)

    # generate accounts
    account_file = output_path + 'Account.csv'
    case_account_gen.run(batch_id, case_file, account_file)

    # generate contacts
    contact_file = output_path + 'Contact.csv'
    case_contact_gen.run(batch_id, account_file, contact_file)

    # generate users
    user_file = output_path + 'User.csv'
    manager_file = output_path + 'Manager.csv'
    case_user_gen.run(batch_id, case_file, user_file, manager_file)

    # generate user presence
    user_presence_file = output_path + 'UserServicePresence.csv'
    case_user_presence_gen.run(batch_id, user_file, user_presence_file)

    # generate agent work
    agent_work_file = output_path + 'AgentWork.csv'
    agent_work_files = case_agent_work_gen.run(batch_id, case_file, agent_work_file, today_datetime)

    # generate opportunities
    oppty_file = output_path + "Opportunity.csv"
    case_oppty_gen.run(batch_id, account_file, oppty_file, case_shape_file)

    # generate events
    event_file = output_path + 'Event.csv'
    case_event_gen.run(batch_id, case_file, event_file, today_datetime)

    # generate tasks
    task_file = output_path + 'Task.csv'
    case_task_gen.run(batch_id, case_file, task_file, today_datetime)

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


    # copy all files to the latest folder
    latest_output_path = definitions.case_latest_path

    if os.environ.get('WRITE_MODE') != 'S3' and not os.path.exists(latest_output_path):
        os.makedirs(latest_output_path)

    latest_case_shape_file = latest_output_path + 'CaseShape.csv'
    copy_data_file.run(case_shape_file, latest_case_shape_file)

    latest_case_file = latest_output_path + 'Case.csv'
    copy_data_file.run(case_file, latest_case_file)

    latest_account_file = latest_output_path + 'Account.csv'
    copy_data_file.run(account_file, latest_account_file)

    latest_contact_file = latest_output_path + 'Contact.csv'
    copy_data_file.run(contact_file, latest_contact_file)

    latest_user_file = latest_output_path + 'User.csv'
    copy_data_file.run(user_file, latest_user_file)

    latest_manager_file = latest_output_path + 'Manager.csv'
    copy_data_file.run(manager_file, latest_manager_file)

    latest_user_presence_file = latest_output_path + 'UserServicePresence.csv'
    copy_data_file.run(user_presence_file, latest_user_presence_file)

    for index, aw in enumerate(agent_work_files):
        latest_agent_work_file = latest_output_path + 'AgentWork-' + str(index) + '.csv'
        if index == 0:
            latest_agent_work_file = latest_output_path + 'AgentWork.csv'
        copy_data_file.run(aw, latest_agent_work_file)

    latest_oppty_file = latest_output_path + "Opportunity.csv"
    copy_data_file.run(oppty_file, latest_oppty_file)

    latest_event_file = latest_output_path + 'Event.csv'
    copy_data_file.run(event_file, latest_event_file)

    latest_task_file = latest_output_path + 'Task.csv'
    copy_data_file.run(task_file, latest_task_file)

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


if __name__ == "__main__":
    # execute only if running as a script
    run()
