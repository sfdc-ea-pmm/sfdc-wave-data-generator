from numpy.random import choice


_lead_status = [
    "Contacted",
    "Approved",
    "Archived",
    "Draft",
    "Open",
    "Pending",
    "Working",
    "Qualified - Convert",
    "Submitted",
    "Rejected",
    "New"
]
def lead_status():
    return choice(_lead_status)


_lead_source = [
    "Inbound Call",
    "Data.com",
    "Cold Call",
    "Partner",
    "Referral",
    "Marketing Event",
    "Social Media",
    "Community",
    "Website"
]
def lead_source():
    return choice(_lead_source)


_lead_industry = [
    "Other",
    "Retail",
    "Consulting",
    "Hospitality",
    "Machinery",
    "Transportation",
    "Finance",
    "Media",
    "Agriculture",
    "Engineering",
    "Banking",
    "Energy",
    "Communications",
    "Insurance",
    "Chemicals",
    "Government",
    "Electronics",
    "Environmental",
    "Food & Beverage",
    "Apparel",
    "Healthcare & Life Sciences",
    "Biotechnology",
    "Entertainment",
    "Technology"
]
def lead_industry():
    return choice(_lead_industry)


_lead_rating = [
    "Hot",
    "Warm",
    "Cool"
]
def lead_rating():
    return choice(_lead_rating)


def lead_is_unread_by_owner():
    return choice(['true', 'false'], p=[.70, .30])