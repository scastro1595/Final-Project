# job.py

class Job:
    def __init__(self, title, company_name, location, skills_required, poster_email):
        self.title = title
        self.company_name = company_name
        self.location = location
        self.skills_required = skills_required  # list of skills
        self.poster_email = poster_email
