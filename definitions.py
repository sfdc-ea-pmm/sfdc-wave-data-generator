import random

source_data = 'sales/data/input/WA_Fn-UseC_-Sales-Win-Loss.csv'
source_users = 'sales/data/input/Users.csv'
source_oppty_shape = 'sales/data/input/OpportunityShape.csv'
oppty_temporal_path = 'sales/data/output/archive/{}/'
oppty_latest_path = 'sales/data/output/latest/'
oppty_shape = 'sales/data/output/OpportunityShape.csv'
oppty = 'sales/data/output/Opportunity.csv'
oppty_accounts = 'sales/data/output/Account.csv'
oppty_accounts_test = 'sales/data/output/Account Test.csv'
oppty_users = 'sales/data/output/User.csv'
oppty_managers = 'sales/data/output/Manager.csv'
oppty_products = 'sales/data/output/Product2.csv'
oppty_pricebook = 'sales/data/output/PricebookEntry.csv'
oppty_line_item = 'sales/data/output/OpportunityLineItem.csv'
oppty_history = 'sales/data/output/OpportunityHistory.csv'
oppty_cases = 'sales/data/output/Case.csv'
oppty_tasks = 'sales/data/output/Task.csv'
oppty_events = 'sales/data/output/Event.csv'
oppty_leads = 'sales/data/output/Lead.csv'
oppty_contacts = 'sales/data/output/Contact.csv'
oppty_forecasting_quota = 'sales/data/output/ForecastingQuota.csv'
oppty_forecasting_user = 'sales/data/output/ForecastingUser.csv'
oppty_quota = 'sales/data/output/Quota.csv'

case_temporal_path = 'service/data/output/archive/{}/'
case_latest_path = 'service/data/output/latest/'
source_case_data = 'service/data/input/Retail_ex_wpandq_filtered.csv'
source_case_shape = 'service/data/input/CaseShape.csv'
case_shape = 'service/data/output/CaseShape.csv'
case_data = 'service/data/output/Case.csv'
case_history = 'service/data/output/CaseHistory.csv'
case_accounts = 'service/data/output/Account.csv'
case_users = 'service/data/output/User.csv'
case_managers = 'service/data/output/Manager.csv'
case_contacts = 'service/data/output/Contact.csv'
case_articles = 'service/data/output/CaseArticle.csv'
case_knowledge_articles = 'service/data/output/KCSArticle_ka.csv'
case_knowledge_article_versions = 'service/data/output/KCSArticle_kav.csv'
case_knowledge_article_votestat = 'service/data/output/KCSArticle_VoteStat.csv'
case_knowledge_article_viewstat = 'service/data/output/KCSArticle_ViewStat.csv'
case_knowledge_article_datacat = 'service/data/output/KCSArticle_DataCategorySelection.csv'
case_events = 'service/data/output/Event.csv'
case_tasks = 'service/data/output/Task.csv'
case_livechat_transcripts = 'service/data/output/LiveChatTranscript.csv'
case_livechat_transcript_events = 'service/data/output/LiveChatTranscriptEvent.csv'
case_oppty = 'service/data/output/Opportunity.csv'
case_agent_work = 'service/data/output/AgentWork.csv'
case_user_presence = 'service/data/output/UserServicePresence.csv'

## sales_service ##
ss_source_oppty_shape = 'sales_service/data/input/OpportunityShape.csv'
ss_oppty_temporal_path = 'sales_service/data/output/archive/{}/'
ss_oppty_latest_path = 'sales_service/data/output/latest/'
ss_case_latest_path = 'sales_service/data/output/latest/'
ss_source_case_shape = 'sales_service/data/input/CaseShape.csv'
## /sales_service ##


# **********************
# Metadata Values Maps
# **********************

# supplies group map
supplies_group_map = {
    "Car Accessories": "Car Accessories",
    "Performance & Non-auto": "Performance & Non-auto",
    "Tires & Wheels": "Tires & Wheels",
    "Car Electronics": "Car Electronics"
}

isWon = {
    "Won": "true",
    "Loss": "false"
}

# supplies subgroup map
# supplies_subgroup_map = {
# 	"Exterior Accessories":"Exterior Accessories",
# 	"Motorcycle Parts":"Motorcycle Parts",
# 	"Shelters & RV":"Shelters & RV",
# 	"Garage & Car Care":"Garage & Car Care",
# 	"Batteries & Accessories":"Batteries & Accessories",
# 	"Performance Parts":"Performance Parts",
# 	"Towing & Hitches":"Towing & Hitches",
# 	"Replacement Parts":"Replacement Parts",
# 	"Tires & Wheels":"Tires & Wheels",
# 	"Interior Accessories":"Interior Accessories",
# 	"Car Electronics":"Car Electronics"
# }

supplies_subgroup_map = {
    "Exterior Accessories": "Exterior Accessories",
    "Motorcycle Parts": "Motorcycle Parts",
    "Shelters & RV": "RV Shelters",
    "Garage & Car Care": "Car Care",
    "Batteries & Accessories": "Batteries",
    "Performance Parts": "Performance",
    "Towing & Hitches": "Towing Equioment",
    "Replacement Parts": "Replacement Parts",
    "Tires & Wheels": "Tires and Wheels",
    "Interior Accessories": "Interior Accessories",
    "Car Electronics": "Electronics"
}

# region
# region_map = {
# 	"Northwest":"Northwest",
# 	"Pacific":"Pacific",
# 	"Midwest":"Midwest",
# 	"Southwest":"Southwest",
# 	"Mid-Atlantic":"Mid-Atlantic",
# 	"Northeast":"Northeast",
# 	"Southeast":"Southeast"
# }
region_map = {
    "Northwest": "US",
    "Pacific": "Canada",
    "Midwest": "UK",
    "Southwest": "Japan",
    "Mid-Atlantic": "Brazil",
    "Northeast": "China",
    "Southeast": "Germany"
}

region_state_map = {
    "Pacific": ['AK', 'WA', 'OR', 'CA', 'HI'],
    "Northwest": ['MT', 'ID', 'WY', 'NV', 'UT', 'CO', 'AZ', 'NM'],
    "Midwest": ['ND', 'MN', 'SD', 'NE', 'IA', 'KS', 'MO', 'WI', 'MI', 'IL', 'IN', 'OH'],
    "Southwest": ['TX', 'OK', 'AR', 'LA'],
    "Mid-Atlantic": ['NY', 'NJ', 'PA'],
    "Northeast": ['ME', 'NH', 'VT', 'NH', 'MA', 'CT', 'RI'],
    "Southeast": ['DE', 'MD', 'WV', 'VA', 'NC', 'SC', 'GA', 'FL', 'AL', 'MS', 'TN', 'KY']
}

# West Sales = 00E460000011ltqEAA
# East Sales = 00E460000011ltwEAA
# Central Sales = 00E460000011ltrEAA
region_territory_mapping = {
    "Pacific": "West Sales",
    "Northwest": "West Sales",
    "Midwest": "Central Sales",
    "Southwest": "Central Sales",
    "Mid-Atlantic": "Central Sales",
    "Northeast": "East Sales",
    "Southeast": "East Sales"
}

# route to market
route = {
    "Fields Sales": "Fields Sales",
    "Reseller": "Reseller",
    "Other": "Other",
    "Telesales": "Telesales",
    "Telecoverage": "Telecoverage"
}

# Client Size By Revenue
client_size_rev = {
    "1": "Corporate",
    "2": "SMB",
    "3": "Mid-Market",
    "4": "Enterprise",
    "5": "T100"
}

client_size_rev_bands = {
    "Corporate": [2000, 10000],
    "SMB": [10000, 50000],
    "Mid-Market": [50000, 500000],
    "Enterprise": [500000, 2000000],
    "T100": [2000000, 10000000]
}

# Client Size By Employee Count
client_size_employees = {
    "1": "0 - 250",
    "2": "250 - 1000",
    "3": "1000 - 5000",
    "4": "5000 - 25000",
    "5": "25000+"
}

# Client Size By Employee Count
client_size_employees_bands = {
    "0 - 250": [0, 250],
    "250 - 1000": [251, 1000],
    "1000 - 5000": [1001, 5000],
    "5000 - 25000": [5001, 25000],
    "25000+": [25001, 150000]
}

# Revenue From Client Past Two Years
client_past_revenue = {
    "0": "0",
    "1": "1 - 10000",
    "2": "10000 - 50000",
    "3": "50000 - 150000",
    "4": "> 150000"
}

client_past_revenue_bands = {
    "0": [0, 1],
    "1 - 10000": [5000, 10000],
    "10000 - 50000": [10001, 50000],
    "50000 - 150000": [50001, 150000],
    "> 150000": [150000, 1000000]
}

# Competitor Type
# Map to competitor?
# competitor_type = {
# 	"Unknown":"Unknown",
# 	"Known":"Known",
# 	"None":"None"	
# }

competitor_type = {
    "Unknown": "Challenger Inc.",
    "Known": "Moparts",
    "None": "Fredericks"
}

# Deal Size Category
deal_size = {
    "1": "1",
    "2": "2",
    "3": "3",
    "4": "4",
    "5": "5",
    "6": "6",
    "7": "7",
}

# stageNames
stagename = {
    'Qualification': 'Qualification',
    'Discovery': 'Discovery',
    'Proposal/Quote': 'Proposal/Quote',
    'Negotiation': 'Negotiation',
    'Closed Won': 'Closed Won',
    'Closed Lost': 'Closed Lost'
}

# stageNames
stage_name = ['Qualification', 'Discovery', 'Proposal/Quote', 'Negotiation', 'Closed Won', 'Closed Lost']

# probability
probabilities = [20, 35, 75, 90, 100, 0]

# forecast
forecast_category = ['Closed', 'BestCase', 'Forecast', 'Omitted', 'Pipeline']
forecast_category_name = {
    'Closed': 'Closed',
    'BestCase': 'Best Case',
    'Forecast': 'Commit',
    'Omitted': 'Omitted',
    'Pipeline': 'Pipeline'
}


# region - states


# REVENUE
# convert categorical from 1-5 to SMB etc.
def convert_revenue_size(revenue_cat):
    return client_size_rev[revenue_cat]


# this is where we convert from categorical into continuous - but kind of random
def generate_revenue_size(revenue_cat):
    # tier out by 100,000,000,000
    low = (int(revenue_cat) - 1) * 100
    high = int(revenue_cat) * 100
    return random.randint(low, high) * 10


# EMPLOYEE
# this is where we convert from categorical into continuous
def generate_employee_size(employee_cat):
    # tier out by 1000
    low = (int(employee_cat) - 1) * 100
    high = int(employee_cat) * 100
    return random.randint(low, high) * 10


# EMPLOYEE
# this is where we convert from categorical into continuous
# range should be 1,000 - 1000000
def generate_client_past_revenue(client_past_revenue):
    if client_past_revenue is '0':
        return 0
    elif client_past_revenue is '1':
        return random.randint(1000, 200000)
    else:
        baseval = int(client_past_revenue)
        return random.randint(baseval * 200000, (baseval + 1) * 200000)
