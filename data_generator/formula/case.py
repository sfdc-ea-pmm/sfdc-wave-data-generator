from numpy.random import choice
from numpy.random import normal

_case_origin = [
    'Phone',
    'Q&A',
    'Website',
    'Chat',
    'Facebook',
    'Email',
    'Mobile Device',
    'Community',
    'Twitter',
    'LinkedIn',
    'Google',
    'Instagram'
]
def case_origin():
    return choice(_case_origin)


_case_type = [
    'Product Support',
    'Account Support',
    'General',
    'Technical Issue'
]
def case_type():
    return choice(_case_type)


_case_status = [
    'Closed',
    'New',
    'Working',
    'Attention',
    'Escalated',
    'Waiting on Customer'
]
def case_status():
    return choice(_case_status, p=[.95, .01, .01, .01, .01, .01])


_case_priority = [
    'Medium',
    'High',
    'Low',
    'Critical'
]
def case_priority():
    return choice(_case_priority)


_case_subject = [
    "Where can I download your mobile app?",
    "I have a question about my contract.",
    "I received the wrong invoice.",
    "Billing statement reprint",
    "I have a product suggestion.",
    "Please send shipping confirmation.",
    "Was our last payment correct?",
    "Product is shutting down intermittently",
    "How do I become a partner?",
    "How much do I owe on my bill?",
    "Customer service hours of operation.",
    "Question about taxes on my order.",
    "How do I obtain your annual report?",
    "Do you sell replacement parts?",
    "How do I create a secure password?",
    "Can I access your community from my mobile device?",
    "Billing issue",
    "How do I get started with your service?",
    "Question on my most recent order.",
    "Billing statement incorrect",
    "How do I set up auto-renewal?",
    "Where do I submit a product suggestion?",
    "What are your support hours?",
    "Is my personal information safe?",
    "Please expedite my order.",
    "Can you help me get set up?",
    "Product setup issues",
    "Product damaged, mishandled during shipping.",
    "Shipping container appears damaged",
    "Expediting my order?",
    "I can't understand the installation instructions",
    "Incorrect bill",
    "How do I troubleshoot a product issue?",
    "Bill payment clarification.",
    "Where do I send my check?",
    "Troubleshooting issues with the product",
    "Purchase order question",
    "How do I check my order status?",
    "Billing address change",
    "How can I request a new feature?",
    "Can you expedite my order?",
    "How do I exchange a product?",
    "Error on my bill",
    "I have a question about my order.",
    "How do I change my password?",
    "Customer called to make a payment",
    "What’s the product warranty policy?",
    "Customer would like to upgrade",
    "What does your service contract cover?",
    "Need most recent invoice",
    "How do I change my communication preferences?",
    "Can I use your app on my phone?",
    "Question about my last billing statement",
    "Assembly instruction help",
    "Problem with my bill",
    "Items missing from shipment.",
    "How do I set up auto-payment?",
    "What's included in your service contract?",
    "How do I sign up for your email newsletter?",
    "Need guidance getting started with my installation",
    "How do I upgrade?",
    "How is my password stored?",
    "Projector getting over heated",
    "Need additional product information",
    "Product manual is missing",
    "How do I diagnose this product issue?",
    "Where do I get your mobile app?",
    "I need to pay my invoice.",
    "Can't understand installation instructions",
    "Setup Instructions are missing",
    "Where can I purchase your products?",
    "Question about my invoice",
    "Please change my contact information.",
    "What are your service hours?",
    "Does your app work on my mobile device?",
    "Initiating return process."
]
def case_subject():
    return choice(_case_subject)


def case_is_escalated():
    return choice(['false', 'true'], p=[.97, .03])


def case_csat():
    csat = int(normal(75, 10))
    if csat > 100:
        return 100
    elif csat < 0:
        return 0
    else:
        return csat
