import os

from numpy.random import choice
from numpy.random import randint

_account_rating = [
    "Hot",
    "Warm",
    "Cool"
]
def account_rating():
    return choice(_account_rating)


_account_ownership = [
    "Private",
    "Public",
    "Other",
    "Subsidiary"
]
def account_ownership():
    return choice(_account_ownership, p=[.50, .15, .25, .10])


def account_year_started():
    return randint(1880, 2010)


_account_industry = [
    "Energy",
    "Electronics",
    "Environmental",
    "Manufacturing",
    "Biotechnology",
    "Utilities",
    "Engineering",
    "Banking",
    "Shipping",
    "Media",
    "Healthcare & Life Sciences",
    "Entertainment",
    "Consulting",
    "Education",
    "Machinery",
    "Other",
    "Government",
    "Telecommunications",
    "Food & Beverage",
    "Retail",
    "Recreation",
    "Financial Services",
    "Construction",
    "Technology",
    "Communications",
    "Chemicals",
    "Insurance",
    "Agriculture",
    "Not For Profit",
    "Apparel",
    "Hospitality",
    "Transportation"
]
def account_industry():
    return choice(_account_industry)


_account_source = [
    "Community",
    "Inbound Call",
    "Cold Call",
    "Website",
    "Partner",
    "Referral",
    "Marketing Event",
    "Data.com",
    "Social Media"
]
def account_source():
    return choice(_account_source)


_account_type = [
    'Enterprise',
    'Mid-Market',
    'Small Business'
]
def account_type():
    return choice(_account_type, p=[.05, .15, .80])


region_state_map = {
    "Pacific": ['AK', 'WA', 'OR', 'CA', 'HI'],
    "Northwest": ['MT', 'ID', 'WY', 'NV', 'UT', 'CO', 'AZ', 'NM'],
    "Midwest": ['ND', 'MN', 'SD', 'NE', 'IA', 'KS', 'MO', 'WI', 'MI', 'IL', 'IN', 'OH'],
    "Southwest": ['TX', 'OK', 'AR', 'LA'],
    "Mid-Atlantic": ['NY', 'NJ', 'PA'],
    "Northeast": ['ME', 'NH', 'VT', 'NH', 'MA', 'CT', 'RI'],
    "Southeast": ['DE', 'MD', 'WV', 'VA', 'NC', 'SC', 'GA', 'FL', 'AL', 'MS', 'TN', 'KY']
}


client_past_revenue_bands = {
    "0": [0, 1],
    "1 - 10000": [5000, 10000],
    "10000 - 50000": [10001, 50000],
    "50000 - 150000": [50001, 150000],
    "> 150000": [150000, 1000000]
}


client_size_rev_bands = {
    "Corporate": [2000, 10000],
    "SMB": [10000, 50000],
    "Mid-Market": [50000, 500000],
    "Enterprise": [500000, 2000000],
    "T100": [2000000, 10000000]
}


client_size_employees_bands = {
    "0 - 250": [0, 250],
    "250 - 1000": [251, 1000],
    "1000 - 5000": [1001, 5000],
    "5000 - 25000": [5001, 25000],
    "25000+": [25001, 150000]
}

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
_account_name = [line.rstrip('\n').replace('"', '') for line in open(os.path.join(__location__, 'account_names.txt'))]

_used_account_name = set()
def account_name():
    name_len = len(_account_name)
    name_index = randint(0, name_len)
    while name_index in _used_account_name:
        name_index = randint(0, name_len)
    _used_account_name.add(name_index)
    return _account_name[name_index]
