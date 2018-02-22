from numpy.random import choice
from numpy.random import randint


_event_subject = [
    "Onsite Account Review with Executive Team",
    "Executive Discovery Meeting",
    "Quarterly Review",
    "Investigate Open Case",
    "Account Planning",
    "Review Final Presentation",
    "Develop Mutual Plan Document",
    "Breakfast with CFO",
    "Meeting with VP Sales",
    "Week Wrap Up",
    "Forecast Meeting",
    "Account Review",
    "Training Class",
    "Training",
    "Customer Briefing",
    "Conference Call",
    "Project Planning Meeting",
    "Weekly Team Meeting",
    "Manager Off-Site",
    "All Hands Meeting",
    "Executive Offsite",
    "Deal Review",
    "Team Meeting",
    "Customer Progress Check-In",
    "Coaching 1:1",
    "Confirming Final Contract Details",
    "Next 1:1",
    "Pipeline 1:1",
    "Discovery and Qualification call",
    "Onsite customer workshop",
    "Mobile Best Practices Session",
    "Pipeline Review",
    "Board presentation run-through",
    "Closing Meeting",
    "Territory Plan Review",
    "Close plan review with customer",
    "Project stakeholder update",
    "Internal team strategy meeting",
    "Discovery call",
    "Post-meeting follow-up",
    "Discovery meeting with key executives",
    "Call with Director of Marketing",
    "Demonstration to Board of Directors",
    "Discovery Call with Customer",
    "Discovery Meeting with CIO",
    "Executive Lunch Meeting",
    "Account Strategy Meeting",
    "Discovery Meeting",
    "Team Best Practices Sharing",
    "Discuss ideal candidate characteristics",
    "Phone Interview",
    "Follow up Meeting",
    "Call",
    "Send Letter",
    "Other",
    "Send Quote"
]
def event_subject():
    return choice(_event_subject)


_event_subject_simple = [
    "Call",
    "Send Letter",
    "Send Quote",
    "Other"
]
def event_subject_simple():
    return choice(_event_subject_simple, p=[.35, .35, .10, .20])


def event_subtype():
    return 'Event'


def event_call_duration():
    return randint(0, 2) * randint(1, 60)
