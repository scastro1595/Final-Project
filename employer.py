# employer.py
# Employer class: register, login, post jobs, delete jobs, view applicants

from job import Job

class Employer:
    def __init__(self, company_name, email, password):
        self.company_name = company_name
        self.email = email
        self.password = password
        self.posted_jobs = []  # List of Job objects

    def post_job(self, title, location, description, required_skills):
        new_job = Job(title, self.company_name, location, description, required_skills)
        self.posted_jobs.append(new_job)
        return new_job

    def delete_job(self, job_to_delete):
        if job_to_delete in self.posted_jobs:
            self.posted_jobs.remove(job_to_delete)
            return True
        return False

    def view_posted_jobs(self):
        return self.posted_jobs
