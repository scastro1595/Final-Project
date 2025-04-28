# employer.py
# Employer class: register, login, post jobs, delete jobs, view applicants



class Employer:
    def __init__(self, company_name, email, password):
        self.company_name = company_name
        self.email = email
        self.password = password
        self.posted_jobs = []  # List of Job objects posted
        self.messages = []  # Inbox messages

    def post_job(self, job):
        self.posted_jobs.append(job)

    def delete_job(self, job_id):
        self.posted_jobs = [job for job in self.posted_jobs if job.job_id != job_id]

    def view_applicants(self, applications):
        # Filter applications related to this employer's jobs
        my_job_ids = [job.job_id for job in self.posted_jobs]
        return [app for app in applications if app.job_id in my_job_ids]

    def receive_message(self, message):
        self.messages.append(message)

    def view_inbox(self):
        return self.messages
