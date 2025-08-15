# enums.py
from enum import Enum

class Role(str, Enum):
    HR = "HR"
    Intern = "Intern"
    Mentor = "Mentor"
    Admin = "Admin"

class CampaignStatus(str, Enum):
    Open = "Open"
    Closed = "Closed"

class ApplicationStatus(str, Enum):
    Pending = "Pending"
    Approved = "Approved"
    Rejected = "Rejected"

class AssignmentStatus(str, Enum):
    Pending = "Pending"
    Doing = "Doing"
    Done = "Done"
