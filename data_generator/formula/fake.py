from faker import Faker
from numpy.random import choice
from numpy.random import randint

fake = Faker()

###########################################
# Name formulas
###########################################


def name():
    """Fake name formula. Example: 'James Carter'"""
    return fake.name()


def name_male():
    """Fake male name formula. Example: 'Joseph Turner'"""
    return fake.name_male()


def name_female():
    """Fake female name formula. Example: 'Lauren Perez'"""
    return fake.name_female()


def first_name():
    """Fake first name formula. Example: 'Matthew'"""
    return fake.first_name()


def first_name_male():
    """Fake male first name formula. Example: 'Jordan'"""
    return fake.first_name_male()


def first_name_female():
    """Fake female first name formula. Example: 'Belinda'"""
    return fake.first_name_female()


def last_name():
    """"Fake last name formula. Example: 'Walker'"""
    return fake.last_name()


def last_name_male():
    """Fake male last name formula. Example: 'Goodwin'"""
    return fake.last_name_male()


def last_name_female():
    """Fake female last name formula. Example: 'Calhoun'"""
    return fake.last_name_female()


def prefix():
    """Fake name prefix formula. Example: 'Mrs.'"""
    return fake.prefix()


def prefix_male():
    """Fake male name prefix formula. Example: 'Mr.'"""
    return fake.prefix_male()


def prefix_female():
    """Fake female name prefix formula. Example: 'Mrs.'"""
    return fake.prefix_female()


def suffix():
    """Fake name suffix formula. Example: 'PhD'"""
    return fake.suffix()


def suffix_male():
    """Fake male name suffix formula. Example: 'Jr.'"""
    return fake.suffix_male()


def suffix_female():
    """Fake female name suffix formula. Example: 'PhD'"""
    return fake.suffix_female()


def phone_number():
    """Fake phone number formula. Example: '1-(235)142-8086'"""
    return '1-(' + fake.numerify(text="###") + ')' \
           + fake.numerify(text="###") + '-' \
           + fake.numerify(text="####")


def ssn():
    """Fake ssn formula. Example: '078-08-6469'"""
    return fake.ssn()

_gender = ['Male', 'Female']
def gender():
    return choice(_gender)


###########################################
# Address formulas
###########################################


def address():
    """Fake address formula. Example: '099 Ronald Stream\nRodriguezmouth, SD 36006-3834'"""
    return fake.address()


def building_number():
    """Fake building number formula. Example: '9012'"""
    return fake.building_number()


def street_name():
    """Fake street name formula. Example: 'Dixon Summit'"""
    return fake.street_name()


def street_address():
    """Fake street address formula. Example: '43363 Davis Circles Apt. 871'"""
    return fake.street_address()


def street_suffix():
    """Fake street suffix formula. Example: 'Harbor'"""
    return fake.street_suffix()


def secondary_address():
    """Fake secondary address formula. Example: 'Apt. 798'"""
    return fake.secondary_address()


def city():
    """Fake city formula. Example: 'North Misty'"""
    return fake.city()


def state():
    """Fake state formula. Example: 'Maine'"""
    return fake.state()

_state_abbr = [
    "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA",
    "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
    "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
    "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
    "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"
]
def state_abbr():
    """Fake state abbreviation formula. Example: 'CA'"""
    return choice(_state_abbr)


def zipcode():
    """Fake zip code formula. Example: '09658'"""
    return str(fake.zipcode())


def zipcode_plus4():
    """Fake zip code plus 4 additional digits formula. Example: '79879-8011'"""
    return fake.zipcode_plus4()


def country():
    """Fake country formula. Example: 'Uzbekistan'"""
    return fake.country()


def country_code():
    """Fake country code formula. Example 'AZ'"""
    return fake.country_code()


###########################################
# Company formulas
###########################################


def company():
    """Fake company name formula. Example: 'Haney Ltd'"""
    return fake.company()


def job():
    """Fake job formula. Example: 'Editorial assistant'"""
    return fake.job()


###########################################
# Internet formulas
###########################################


def ipv4():
    """Fake ipv4 formula. Example: '188.179.116.117'"""
    return fake.ipv4(network=False)


def ipv6():
    """Fake ipv6 formula. Example: '8262:139f:dffe:a8e7:8157:cb23:2590:48a1'"""
    return fake.ipv6(network=False)


def url():
    """Fake url formula. Example: 'http://www.mendez.com/'"""
    return fake.url()


def free_email():
    """Fake free email formula. Example: 'judithparsons@gmail.com'"""
    return fake.free_email()


def safe_email():
    """Fake safe email formula. Example: 'yorozco@example.com'"""
    return fake.safe_email()


def company_email():
    """Fake company email formula. Example: 'garciavanessa@myers.com'"""
    return fake.company_email()


###########################################
# Date formulas
###########################################


def date_time_between_dates(start, end):
    return fake.date_time_between_dates(datetime_start=start, datetime_end=end, tzinfo=None)


def body():
    return ' '.join(fake.sentences(nb=randint(1, 5)))

_browser = [
    'Chrome',
    'IE',
    'Firefox',
    'Safari',
    'Edge',
    'Other'
]
def browser():
    return choice(_browser, p=[.50, .20, .15, .08, .05, .02])


def md5():
    return fake.md5()


def user_agent():
    return fake.user_agent()


def sentence():
    return ' '.join(fake.sentences(nb=1))
