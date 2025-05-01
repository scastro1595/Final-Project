# application.py
# Application class: linking users to jobs they apply for
import uuid


class Application:
    def __init__(self, user_email, job_id, job_title, company, status='Pending'):
        """
        Represents a job application with detailed tracking

        Args:
            user_email (str): Email of the applicant
            job_id (str): Unique identifier for the job
            job_title (str): Title of the job applied to
            company (str): Company offering the job
            status (str, optional): Current status of the application
        """
        self.id = str(uuid.uuid4())  # Unique application ID
        self.user_email = user_email
        self.job_id = job_id
        self.job_title = job_title
        self.company = company
        self.status = status  # 'Pending', 'Reviewed', 'Interviewing', 'Accepted', 'Rejected'
        self.created_at = str(uuid.uuid1())  # Timestamp for the application

    def update_status(self, new_status):
        """
        Update the status of the application

        Args:
            new_status (str): New status for the application
        """
        valid_statuses = ['Pending', 'Reviewed', 'Interviewing', 'Accepted', 'Rejected']
        if new_status in valid_statuses:
            self.status = new_status
        else:
            raise ValueError(f"Invalid status. Must be one of {valid_statuses}")

    def __str__(self):
        """
        String representation of the application

        Returns:
            str: Formatted application details
        """
        return f"Application for {self.job_title} at {self.company} - Status: {self.status}"

    def to_dict(self):
        """
        Convert application to a dictionary for easy serialization

        Returns:
            dict: Dictionary representation of the application
        """
        return {
            'id': self.id,
            'user_email': self.user_email,
            'job_id': self.job_id,
            'job_title': self.job_title,
            'company': self.company,
            'status': self.status,
            'created_at': self.created_at
        }


class MessageSystem:
    def __init__(self):
        """
        Manages messaging and applications across the system
        """
        self.messages = []
        self.applications = []

    def send_message(self, sender_email, receiver_email, content, context=None):
        """
        Send a message between users

        Args:
            sender_email (str): Email of the sender
            receiver_email (str): Email of the receiver
            content (str): Message content
            context (dict, optional): Additional context for the message

        Returns:
            dict: The created message
        """
        new_message = {
            'id': str(uuid.uuid4()),
            'sender_email': sender_email,
            'receiver_email': receiver_email,
            'content': content,
            'context': context or {},
            'timestamp': str(uuid.uuid1())
        }
        self.messages.append(new_message)
        return new_message

    def submit_application(self, user_email, job):
        """
        Submit a job application

        Args:
            user_email (str): Email of the applicant
            job (Job): Job object being applied to

        Returns:
            Application: The created application object
        """
        # Generate a unique job ID
        job_id = f"{job.company}_{job.title}".replace(" ", "_").lower()

        # Create application
        new_application = Application(
            user_email,
            job_id,
            job.title,
            job.company
        )

        # Add to applications list
        self.applications.append(new_application.to_dict())

        # Send automatic confirmation message
        self.send_message(
            job.company,
            user_email,
            f"Thank you for applying to {job.title}. Your application is now under review.",
            context={'application_id': new_application.id}
        )

        return new_application

    def get_user_applications(self, user_email):
        """
        Retrieve all applications for a specific user

        Args:
            user_email (str): Email of the user

        Returns:
            list: List of applications for the user
        """
        return [
            app for app in self.applications
            if app['user_email'] == user_email
        ]

    def get_user_messages(self, user_email):
        """
        Retrieve all messages for a specific user

        Args:
            user_email (str): Email of the user

        Returns:
            list: List of messages for the user
        """
        return [
            msg for msg in self.messages
            if msg['sender_email'] == user_email or msg['receiver_email'] == user_email
        ]

    def get_messages_for_receiver(self, receiver_email):
        """
        Retrieve messages specifically sent to a user

        Args:
            receiver_email (str): Email of the receiver

        Returns:
            list: List of messages sent to the user
        """
        return [
            msg for msg in self.messages
            if msg['receiver_email'] == receiver_email
        ]


# Global message system instance
message_system = MessageSystem()
