from user import User
from employer import Employer
from job import Job
from message import Message

# Sample Users
sample_users = [
    User(first_name="Alice", last_name="Johnson", email="alice@example.com", password="pass123", skills=["python", "sql"]),
    User(first_name="Bob", last_name="Smith", email="bob@example.com", password="pass123", skills=["javascript", "html", "css"]),
    User(first_name="Charlie", last_name="Davis", email="charlie@example.com", password="pass123", skills=["java", "project management"])
]

# Sample Employers
sample_employers = [
    Employer(company_name="Tech Solutions Inc.", email="hr@techsolutions.com", password="employerpass"),
    Employer(company_name="Creative Agency", email="jobs@creativeagency.com", password="employerpass")
]

# Sample Jobs
sample_jobs = [
    Job(
        title="Software Engineer",
        company_name="Tech Solutions Inc.",
        location="New York",
        skills_required=["python", "sql"],
        poster_email="hr@techsolutions.com"
    ),
    Job(
        title="Frontend Developer",
        company_name="Creative Agency",
        location="San Francisco",
        skills_required=["html", "css", "javascript"],
        poster_email="jobs@creativeagency.com"
    ),
    Job(
        title="Data Analyst",
        company_name="Data Insights Co.",
        location="Chicago",
        skills_required=["python", "sql", "excel"],
        poster_email="hr@datainsights.com"
    ),
    Job(
        title="Marketing Specialist",
        company_name="Creative Agency",
        location="Los Angeles",
        skills_required=["marketing", "content creation"],
        poster_email="jobs@creativeagency.com"
    )
]

# Sample Messages
sample_messages = [
    Message(sender_email="hr@techsolutions.com", receiver_email="alice@example.com", content="We reviewed your resume and would like to connect!"),
    Message(sender_email="jobs@creativeagency.com", receiver_email="bob@example.com", content="Your skills match our opening, let's schedule an interview!")
]
