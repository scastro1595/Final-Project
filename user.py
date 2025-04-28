# user.py
# User class: registration, login, profile management, applying to jobs



class User:
    def __init__(self, first_name, last_name, email, password, skills=None, resume_text=None):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.skills = skills if skills else []
        self.resume_text = resume_text
        self.applied_jobs = []  # List of Job IDs the user has applied to
        self.messages = []  # Inbox messages

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def add_skill(self, skill):
        if skill not in self.skills:
            self.skills.append(skill)

    def set_resume_text(self, resume_text):
        self.resume_text = resume_text

    def apply_for_job(self, job_id):
        if job_id not in self.applied_jobs:
            self.applied_jobs.append(job_id)

    def receive_message(self, message):
        self.messages.append(message)

    def view_inbox(self):
        return self.messages
