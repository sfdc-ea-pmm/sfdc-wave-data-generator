from numpy.random import choice
from numpy.random import randint


_task_status = [
    'Completed',
    'Not Started',
    'In Progress',
    'On Hold',
    'Open'
]
def task_status():
    return choice(_task_status, p=[.30, .25, .20, .20, .05])


_task_priority = [
    'Normal',
    'High'
]
def task_priority():
    return choice(_task_priority, p=[.90, .10])


_task_subtype = [
    'Task',
    'Email',
    'Call'
]
def task_subtype():
    return choice(_task_subtype, p=[.90, .05, .05])

def oppty_task_subtype():
    return choice(_task_subtype, p=[.50, .30, .20])


_task_subject = [
    "Send Letter",
    "Call",
    "Other",
    "Send Quote",
    "Follow-up",
    "Update Account Plan for Strategy Review",
    "Prepare for Discovery Meeting",
    "Review referrals",
    "Review Job Requisition",
    "Discovery Call",
    "Lunch Meeting",
    "Review Meeting Notes",
    "Share Notes from Discussion",
    "Conversation with Product Management",
    "Prep for Sales Discussion",
    "Review Proposal and Update Pricing",
    "Develop Business Case",
    "Draft Proposal for Customer",
    "Arrange Team Strategy Meeting",
    "Prepare for Qualification Call",
    "Revise Quote Based on Customer Conversation",
    "Review Proposal",
    "Project Discovery Call",
    "Complete and Send Close Plan",
    "Mid-Year Review",
    "Channel Plan Status Call",
    "Channel Account Planning",
    "Onsite Presentation and Discussion",
    "Opportunity Close Plan Development",
    "Discovery Meeting with Stakeholders",
    "Conference Call with VP of Operations",
    "Develop Account Plan",
    "Onsite Presentation to Executive Team",
    "Discuss Revised Quote",
    "Develop Content and Positioning for Keynote Presentation",
    "Reserve Venue for Customer Conference",
    "Develop Outbound Call Script and Offers",
    "Arrange Travel for Guest Speaker",
    "Review Campaign Success and Plan Next Phase",
    "Run Facebook Promotion to Boost Engagement",
    "Design Social Command Center Requirements and Layout",
    "Review Social Listening and Identify Keywords",
    "Attend Social Media Best Practices Webinar",
    "Social Media Strategy Meeting",
    "Engage Featured Speaker for Webinar",
    "Develop Content for Webinar",
    "Review Ad Text Options for A/B Testing",
    "Approve Ad Designs",
    "Complete Mutual Plan Document",
    "Complete My 2nd Team Presentation",
    "Cleanup Current Pipeline by End of Month",
    "Setup & Run the First Manager Certification Class",
    "Meeting to Discuss Objection Handling Best Practices",
    "Certification Training Review",
    "Work with Marketing Team",
    "Meeting with Engineering Team",
    "2nd Mock Presentation",
    "Sign Up for KB Training",
    "Follow-up with Customer",
    "Commitment: 20 Calls a Week to New Logos",
    "Customer Success Review",
    "Customer Service Follow-Up Call",
    "Customer Feedback Session",
    "Complete Product Certification",
    "Meeting Debrief and Follow-Ups",
    "Reply to Customer Questions.",
    "Call Customer for Update",
    "Kickoff Meeting with Stakeholders",
    "Onsite Meeting with Executive Team",
    "Finalize Contract",
    "Project Update Call",
    "Travel Time",
    "Send Thank You to Customer",
    "Quick Call with Director of Finance",
    "Prep Sales Presentation",
    "Product Demonstration with Team",
    "Follow-Up From Meeting",
    "Post-Meeting Follow-Up",
    "Sales Call with VP of Marketing",
    "Notes From Discussion",
    "Call with Decision Maker",
    "Connect with VP of Operations",
    "Request Account Review",
    "Discovery Notes",
    "Left Voicemail",
    "Discovery Meeting Request",
    "Notes From Discussion with VP of Finance",
    "Update Quote with Revised Pricing",
    "Qualification Notes",
    "Follow Up To My Message",
    "Deal Discussion with Team",
    "Inbound Call",
    "Call with VP of Sales",
    "Cold Call to Director of Operations",
    "Send Revised Pricing",
    "Call with Director of Sales",
    "Sales Presentation Follow-Up",
    "Check In with Customer",
    "Connect with VP of Sales",
    "Demonstration to Project Team",
    "Executive Meeting Follow-up",
    "Your customer has opened a Case",
    "Schedule Negotiation Call",
    "Schedule Discovery Call",
    "Discuss Requirements with CIO",
    "Review Proof-of-Concept with Project Team",
    "Feature Request Submitted",
    "Your Customer Has a Question About Their Bill",
    "Send New Quote",
    "Send Thank You Email",
    "Check-in with Customer",
    "Send Updated Quote",
    "Call with VP of Marketing",
    "Manager Deal Update",
    "Sales Presentation",
    "Discuss Customer Requirements",
    "Request Requirements Document",
    "Left Voicemail",
    "Demonstration to Key Stakeholders",
    "Touch Base with Director of Sales",
    "Product Demo For Executive Team",
    "Review Discovery Notes",
    "Negotiate Terms",
    "Call with Project Team",
    "Call Connect with VP of Service",
    "Quick Call with VP of IT",
    "Deal Discussion",
    "Call to Schedule Presentation",
    "Follow Up with Customer",
    "Qualification Notes from Meeting",
    "Send Thank You Message",
    "Call for Update on Project",
    "Send Updated Pricing and Contract",
    "Cold Call to Director of Services",
    "Review Product Roadmap",
    "Discovery Call Request",
    "Send Questionnaire to Customer",
    "Request Needs List",
    "Discovery Call with Customer",
    "Call Connect with VP of Sales",
    "Touch Base with Key Decision Maker",
    "Called Decision Maker - CIO",
    "Notes from Discovery Meeting",
    "Negotiate Terms and Conditions",
    "Account Review Call",
    "Call with VP of Customer Service",
    "Call Connect with CEO",
    "Quick Call to Update Customer",
    "Follow Up to My Message",
    "Discovery Call Notes",
    "Qualification Call Notes",
    "Request Questions From Customer",
    "Send Needs Questionnaire",
    "Notes from Discovery Call",
    "Notes from Customer Discussion",
    "Discovery Session Notes",
    "Qualification Meeting Notes",
    "Send Updated Pricing",
    "Sales Presentation to Executive Team",
    "Request Needs Document",
    "Review Needs List",
    "Touch Base with Champion",
    "Product Demo for Executive Team",
    "Notes from Stakeholder Meeting",
    "Notes from Discussion",
    "Negotiate Terms of Contract",
    "Call to Schedule Sales Presentation",
    "Follow up with Customer",
    "Send Revised Pricing to Customer",
    "Cold Call",
    "Qualification Call with Stakeholders",
    "Request Requirements List from Prospect",
    "Demonstration for Key Stakeholders",
    "Call Follow-Up and Thank You",
    "Update with Customer",
    "Finalize Board Presentation",
    "Sales Presentation to Project Team",
    "Get Requirements from Prospect",
    "Call Connect with CIO",
    "Introductory Call with Director of Finance",
    "Quick Call with VP of Operations",
    "Internal Deal Discussion",
    "Identify Keywords That Drive Traffic",
    "Review Current Results and Revise ROI",
    "Generate Quote with T&C's",
    "Finalize List of Target Companies to Engage",
    "Agree on Next Steps",
    "Cold Call with Prospect",
    "Call with Director of Operations",
    "Price Discussion",
    "Send Out Proposal and Pricing",
    "Closing Call",
    "Lead Qualification Call",
    "Review Case with Customer",
    "Follow-up Call",
    "Tradeshow Preparation",
    "Review Updated Sales Presentation",
    "Discovery Call with Management Team",
    "Lead Source Details",
    "Finalize Contract and Discuss Terms",
    "Follow Up and Qualification",
    "Qualification Call"
]
def task_subject():
    return choice(_task_subject)


_task_subject_simple = [
    'Call',
    'Send Letter',
    'Send Quote',
    'Other'
]
def task_subject_simple():
    return choice(_task_subject_simple, p=[.35, .35, .10, .20])


_task_call_type = [
    'Inbound',
    'Internal',
    'Outbound'
]
def task_call_type():
    return choice(_task_call_type)


_task_call_disposition = [
    'Call Successful',
    'Appointment Set',
    'Call Unsuccessful',
    'Contacted',
    'Left Voicemail',
    'Left Message',
    'Busy',
    'No Answer'
]
def task_call_disposition():
    return choice(_task_call_disposition, p=[.45, .25, .05, .05, .05, .05, .05, .05])

_task_call_disposition_simple = [
    'Hot',
    'Warm',
    'Cold'
]
def task_call_disposition_simple():
    return choice(_task_call_disposition_simple, p=[.25, .50, .25])



def task_call_duration():
    return str(randint(3, 361)) + '0'
