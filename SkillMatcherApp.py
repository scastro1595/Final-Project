# SkillMatcherApp.py
# Group 3 - Chelsea Bonyata, Stephanie Castro, Renzo Landicho, Amber Claudio
# Final Version - April 28, 2025
# This file runs the entire SkillMatcher GUI Application

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from resume_parser import parse_resume
from sample_data import sample_users, sample_employers, sample_jobs, sample_messages
from user import User
from employer import Employer
from admin import Admin
from application import Application
from message import Message


class SkillMatcherApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SkillMatcher Application")
        self.geometry("900x600")
        self.resizable(width=False, height=False)

        # In-memory 'database'
        self.users = sample_users.copy()
        self.employers = sample_employers.copy()
        self.admins = [Admin("Admin", "admin@skillmatcher.com", "adminpass")]
        self.jobs = sample_jobs.copy()
        self.messages = sample_messages.copy()
        self.applications = []

        # Session state
        self.current_user = None
        self.current_employer = None
        self.current_admin = None

        # Set up tabs
        self.tabControl = ttk.Notebook(self)
        self.home_tab = ttk.Frame(self.tabControl)
        self.upload_tab = ttk.Frame(self.tabControl)
        self.browse_tab = ttk.Frame(self.tabControl)
        self.matches_tab = ttk.Frame(self.tabControl)
        self.messages_tab = ttk.Frame(self.tabControl)
        self.profile_tab = ttk.Frame(self.tabControl)
        self.admin_tab = ttk.Frame(self.tabControl)

        self.tabControl.add(self.home_tab, text="Home")
        self.tabControl.add(self.upload_tab, text="Upload Resume")
        self.tabControl.add(self.browse_tab, text="Browse Jobs")
        self.tabControl.add(self.matches_tab, text="Matches")
        self.tabControl.add(self.messages_tab, text="Messages")
        self.tabControl.add(self.profile_tab, text="Profile")
        self.tabControl.add(self.admin_tab, text="Admin Panel")
        self.tabControl.pack(expand=1, fill="both")

        self.build_home_tab()
        self.build_upload_tab()
        self.build_browse_jobs_tab()
        self.build_matches_tab()
        self.build_messages_tab()
        self.build_profile_tab()
        self.build_admin_tab()


    def build_home_tab(self):
        title = tk.Label(self.home_tab, text="Welcome to SkillMatcher!", font=("Arial", 20))
        title.pack(pady=20)

        login_button = tk.Button(self.home_tab, text="Login", command=self.build_login_window, width=20)
        login_button.pack(pady=10)

        register_button = tk.Button(self.home_tab, text="Register", command=self.register_screen, width=20)
        register_button.pack(pady=10)

        logout_button = tk.Button(self.home_tab, text="Logout", command=self.logout, width=20)
        logout_button.pack(pady=10)

    def build_upload_tab(self):
        instruction = tk.Label(self.upload_tab, text="Upload your Resume (.txt, .docx, or .pdf)", font=("Arial", 14))
        instruction.pack(pady=20)

        upload_button = tk.Button(self.upload_tab, text="Choose File", command=self.upload_resume)
        upload_button.pack(pady=10)

        self.upload_result = tk.Label(self.upload_tab, text="", font=("Arial", 12))
        self.upload_result.pack(pady=10)

    def build_browse_jobs_tab(self):
        self.jobs_listbox = tk.Listbox(self.browse_tab, width=100, height=20)
        self.jobs_listbox.pack(pady=10)

        refresh_button = tk.Button(self.browse_tab, text="Refresh Jobs", command=self.refresh_jobs)
        refresh_button.pack(pady=5)

        apply_button = tk.Button(self.browse_tab, text="Apply to Selected Job", command=self.apply_to_selected_job)
        apply_button.pack(pady=5)

    def build_matches_tab(self):
        self.matches_listbox = tk.Listbox(self.matches_tab, width=100, height=20)
        self.matches_listbox.pack(pady=10)

        find_matches_button = tk.Button(self.matches_tab, text="Find Matching Jobs", command=self.find_matches)
        find_matches_button.pack(pady=5)

    def build_messages_tab(self):
        self.messages_listbox = tk.Listbox(self.messages_tab, width=100, height=15)
        self.messages_listbox.pack(pady=10)

        compose_button = tk.Button(self.messages_tab, text="Compose Message", command=self.compose_message)
        compose_button.pack(pady=5)

    def build_profile_tab(self):
        self.profile_info = tk.Label(self.profile_tab, text="Profile Details:", font=("Arial", 14))
        self.profile_info.pack(pady=20)

        self.profile_details = tk.Label(self.profile_tab, text="", font=("Arial", 12))
        self.profile_details.pack(pady=10)

        delete_resume_button = tk.Button(self.profile_tab, text="Delete Resume", command=self.delete_resume)
        delete_resume_button.pack(pady=5)

    def build_admin_tab(self):
        view_users_button = tk.Button(self.admin_tab, text="View All Users", command=self.view_users)
        view_users_button.pack(pady=10)

        view_jobs_button = tk.Button(self.admin_tab, text="View All Jobs", command=self.view_jobs)
        view_jobs_button.pack(pady=10)

        delete_user_button = tk.Button(self.admin_tab, text="Delete User", command=self.delete_user)
        delete_user_button.pack(pady=10)

        delete_job_button = tk.Button(self.admin_tab, text="Delete Job", command=self.delete_job)
        delete_job_button.pack(pady=10)

    def login_screen(self):
        login_window = tk.Toplevel(self)
        login_window.title("Login")
        login_window.geometry("300x300")

        tk.Label(login_window, text="Email:").pack()
        email_entry = tk.Entry(login_window)
        email_entry.pack()

        tk.Label(login_window, text="Password:").pack()
        password_entry = tk.Entry(login_window, show="*")
        password_entry.pack()

    def build_login_window(self):
        self.login_window = tk.Toplevel(self)
        self.login_window.title("Login")

        tk.Label(self.login_window, text="Email:").pack()
        self.email_entry = tk.Entry(self.login_window)
        self.email_entry.pack()

        tk.Label(self.login_window, text="Password:").pack()
        self.password_entry = tk.Entry(self.login_window, show="*")
        self.password_entry.pack()

        # ADD THIS BUTTON:
        tk.Button(self.login_window, text="Login", command=self.attempt_login).pack(pady=10)

    def attempt_login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()

        # Check if admin
        for admin in self.admins:
            if admin.email == email and admin.password == password:
                self.current_admin = admin
                messagebox.showinfo("Login Successful", f"Welcome Admin {admin.name}!")
                self.show_admin_panel()
                self.login_window.destroy()
                return

        # Check if employer
        for employer in self.employers:
            if employer.email == email and employer.password == password:
                self.current_employer = employer
                messagebox.showinfo("Login Successful", f"Welcome Employer {employer.company_name}!")
                self.login_window.destroy()
                return

        # Check if user
        for user in self.users:
            if user.email == email and user.password == password:
                self.current_user = user
                messagebox.showinfo("Login Successful", f"Welcome {user.first_name} {user.last_name}!")
                self.login_window.destroy()
                return

        # If no match
        messagebox.showerror("Login Failed", "Invalid email or password.")

    def register_screen(self):
        register_window = tk.Toplevel(self)
        register_window.title("Register")
        register_window.geometry("300x400")

        tk.Label(register_window, text="First Name:").pack()
        first_name_entry = tk.Entry(register_window)
        first_name_entry.pack()

        tk.Label(register_window, text="Last Name:").pack()
        last_name_entry = tk.Entry(register_window)
        last_name_entry.pack()

        tk.Label(register_window, text="Email:").pack()
        email_entry = tk.Entry(register_window)
        email_entry.pack()

        tk.Label(register_window, text="Password:").pack()
        password_entry = tk.Entry(register_window, show="*")
        password_entry.pack()

        tk.Label(register_window, text="Role: (user/employer)").pack()
        role_entry = tk.Entry(register_window)
        role_entry.pack()

        def attempt_register():
            first = first_name_entry.get()
            last = last_name_entry.get()
            email = email_entry.get()
            password = password_entry.get()
            role = role_entry.get().lower()
            self.register_user(first, last, email, password, role)
            register_window.destroy()

        tk.Button(register_window, text="Register", command=attempt_register).pack(pady=10)

    def register_user(self, first_name, last_name, email, password, role):
        if role.lower() == "user":
            new_user = User(first_name, last_name, email, password, [])
            self.users.append(new_user)
            messagebox.showinfo("Success", f"User {first_name} {last_name} registered.")
        elif role.lower() == "employer":
            new_employer = Employer(first_name, email, password)
            self.employers.append(new_employer)
            messagebox.showinfo("Success", f"Employer {first_name} registered.")
        else:
            messagebox.showerror("Error", "Invalid role specified. Use 'user' or 'employer'.")

    def upload_resume(self):
        file_path = filedialog.askopenfilename(filetypes=[("Documents", "*.txt *.docx *.pdf")])
        if file_path and self.current_user:
            skills = parse_resume(file_path)
            self.current_user.skills = skills
            self.upload_result.config(text="Resume uploaded and skills extracted!")
        else:
            messagebox.showerror("Error", "Please log in and select a valid file.")

    def authenticate_login(self, email, password):
        # Check Admin
        for admin in self.admins:
            if admin.email == email and admin.password == password:
                self.current_admin = admin
                messagebox.showinfo("Login Successful", "Logged in as Admin!")
                return

        # Check Users
        for user in self.users:
            if user.email == email and user.password == password:
                self.current_user = user
                messagebox.showinfo("Login Successful", f"Welcome, {user.first_name}!")
                self.update_profile_tab()
                return

        # Check Employers
        for employer in self.employers:
            if employer.email == email and employer.password == password:
                self.current_employer = employer
                messagebox.showinfo("Login Successful", f"Welcome, {employer.company_name}!")
                return

        messagebox.showerror("Login Failed", "No matching account found.")

    def logout(self):
        self.current_user = None
        self.current_employer = None
        self.current_admin = None
        messagebox.showinfo("Logout", "You have been logged out.")

    def delete_resume(self):
        if self.current_user:
            self.current_user.skills = []
            messagebox.showinfo("Resume Deleted", "Your resume and skills have been removed.")
            self.upload_result.config(text="")
        else:
            messagebox.showerror("Error", "Please log in first.")

    def refresh_jobs(self):
        self.jobs_listbox.delete(0, tk.END)
        for job in self.jobs:
            self.jobs_listbox.insert(tk.END, f"{job.title} at {job.company}")

    def apply_to_selected_job(self):
        if not self.current_user:
            messagebox.showerror("Error", "Login as a user to apply.")
            return

        selected = self.jobs_listbox.curselection()
        if not selected:
            messagebox.showerror("Error", "Please select a job first.")
            return

        job = self.jobs[selected[0]]
        new_application = Application(self.current_user, job)
        self.applications.append(new_application)
        messagebox.showinfo("Application Submitted", f"You applied to {job.title}.")

    def find_matches(self):
        if not self.current_user:
            messagebox.showerror("Error", "Login first to find matches.")
            return

        self.matches_listbox.delete(0, tk.END)
        user_skills = set(self.current_user.skills)

        for job in self.jobs:
            job_skills = set(job.required_skills)
            if user_skills.intersection(job_skills):
                self.matches_listbox.insert(tk.END, f"{job.title} at {job.company}")

    def compose_message(self):
        if not self.current_user and not self.current_employer:
            messagebox.showerror("Error", "Login first to send a message.")
            return

        msg_window = tk.Toplevel(self)
        msg_window.title("Compose Message")
        msg_window.geometry("300x300")

        tk.Label(msg_window, text="Receiver Email:").pack()
        receiver_entry = tk.Entry(msg_window)
        receiver_entry.pack()

        tk.Label(msg_window, text="Message:").pack()
        content_entry = tk.Text(msg_window, height=5, width=30)
        content_entry.pack()

        def send():
            receiver_email = receiver_entry.get()
            content = content_entry.get("1.0", tk.END).strip()

            # Find receiver
            receiver = next((u for u in self.users if u.email == receiver_email), None)
            if not receiver:
                receiver = next((e for e in self.employers if e.email == receiver_email), None)

            if receiver:
                sender = self.current_user or self.current_employer
                new_message = Message(sender, receiver, content)
                self.messages.append(new_message)
                messagebox.showinfo("Message Sent", "Your message has been sent.")
                msg_window.destroy()
            else:
                messagebox.showerror("Error", "Receiver not found.")

        tk.Button(msg_window, text="Send", command=send).pack(pady=10)

    def update_profile_tab(self):
        if self.current_user:
            details = f"Name: {self.current_user.first_name} {self.current_user.last_name}\nEmail: {self.current_user.email}\nSkills: {', '.join(self.current_user.skills)}"
            self.profile_details.config(text=details)
        else:
            self.profile_details.config(text="No user logged in.")

    def view_users(self):
        users_window = tk.Toplevel(self)
        users_window.title("Registered Users")
        users_window.geometry("400x400")

        for user in self.users:
            label = tk.Label(users_window, text=f"{user.first_name} {user.last_name} - {user.email}")
            label.pack()

    def view_jobs(self):
        if not self.jobs:
            messagebox.showinfo("Info", "No jobs available.")
            return

        jobs_window = tk.Toplevel(self)
        jobs_window.title("Available Jobs")
        jobs_window.geometry("500x400")

        for job in self.jobs:
            label = tk.Label(
                jobs_window,
                text=f"{job.title} at {job.company_name} in {job.location}\nRequired Skills: {', '.join(job.skills_required)}\nPosted by: {job.poster_email}",
                justify="left",
                anchor="w",
                padx=10,
                pady=5
            )
            label.pack(fill="both", padx=10, pady=5)

    def delete_user(self):
        delete_window = tk.Toplevel(self)
        delete_window.title("Delete User")
        delete_window.geometry("300x200")

        tk.Label(delete_window, text="Enter User Email to Delete:").pack()
        email_entry = tk.Entry(delete_window)
        email_entry.pack()

        def confirm_delete():
            email = email_entry.get()
            self.users = [u for u in self.users if u.email != email]
            messagebox.showinfo("Deleted", "User deleted if email matched.")
            delete_window.destroy()

        tk.Button(delete_window, text="Delete", command=confirm_delete).pack(pady=10)

    def delete_job(self):
        delete_window = tk.Toplevel(self)
        delete_window.title("Delete Job")
        delete_window.geometry("300x200")

        tk.Label(delete_window, text="Enter Job Title to Delete:").pack()
        title_entry = tk.Entry(delete_window)
        title_entry.pack()

        def confirm_delete_job():
            title = title_entry.get()
            self.jobs = [j for j in self.jobs if j.title != title]
            messagebox.showinfo("Deleted", "Job deleted if title matched.")
            delete_window.destroy()

        tk.Button(delete_window, text="Delete", command=confirm_delete_job).pack(pady=10)

# --------------------- Run App ------------------------

if __name__ == "__main__":
    app = SkillMatcherApp()
    app.mainloop()
