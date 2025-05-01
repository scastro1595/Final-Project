# admin.py

class Admin:
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password
    def delete_user(self, users_list, user_to_delete):
        """
        Delete a specific user from the list of users

        Args:
            users_list (list): List of all users
            user_to_delete (User): User object to be deleted

        Returns:
            bool: True if user was successfully deleted, False otherwise
        """
        if user_to_delete in users_list and user_to_delete.role != 'admin':
            users_list.remove(user_to_delete)
            return True
        return False

    def delete_job(self, jobs_list, job_to_delete):
        """
        Delete a specific job from the list of jobs

        Args:
            jobs_list (list): List of all jobs
            job_to_delete (Job): Job object to be deleted

        Returns:
            bool: True if job was successfully deleted, False otherwise
        """
        if job_to_delete in jobs_list:
            jobs_list.remove(job_to_delete)
            return True
        return False
