# SkillMatcherApp.py
# Group 3 - Chelsea Bonyata, Stephanie Castro, Renzo Landicho, Amber Claudio
# Final Version - April 28, 2025
# This file runs the entire SkillMatcher GUI Application

import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox, filedialog, simpledialog
import os
import pickle

from user import User
from employer import Employer
from job import Job
from message import Message
from resume_parser import parse_resume
from sample_data import load_sample_data
from admin import Admin

# Import the new application system
from application import message_system

# GLOBALS
users = []
employers = []
messages = []
current_user = None
current_employer = None
jobs = []

# Load sample data
sample_users, sample_employers, sample_jobs = load_sample_data()
# Add sample data to our lists if they exist
if sample_users:
    users.extend(sample_users)
if sample_employers:
    employers.extend(sample_employers)
if sample_jobs:
    jobs.extend(sample_jobs)


def save_data():
    """Save all application data to files"""
    with open("users.pkl", "wb") as f:
        pickle.dump(users, f)
    with open("employers.pkl", "wb") as f:
        pickle.dump(employers, f)
    with open("jobs.pkl", "wb") as f:
        pickle.dump(jobs, f)

    # Save messages and applications
    with open("messages.pkl", "wb") as f:
        pickle.dump(message_system.messages, f)
    with open("applications.pkl", "wb") as f:
        pickle.dump(message_system.applications, f)


def load_data():
    """Load application data from files"""
    global users, employers, jobs

    # Load users, employers, and jobs
    if os.path.exists("users.pkl"):
        with open("users.pkl", "rb") as f:
            users = pickle.load(f)
    if os.path.exists("employers.pkl"):
        with open("employers.pkl", "rb") as f:
            employers = pickle.load(f)
    if os.path.exists("jobs.pkl"):
        with open("jobs.pkl", "rb") as f:
            jobs = pickle.load(f)

    # Load messages and applications to the message system
    if os.path.exists("messages.pkl"):
        with open("messages.pkl", "rb") as f:
            message_system.messages = pickle.load(f)
    if os.path.exists("applications.pkl"):
        with open("applications.pkl", "rb") as f:
            message_system.applications = pickle.load(f)


def register_screen():
    """Display the registration screen"""
    clear_screen()

    tk.Label(root, text="Register New Account", font=("Arial", 16)).pack(pady=10)

    tk.Label(root, text="First Name").pack()
    first_name_entry = tk.Entry(root, width=30)
    first_name_entry.pack(pady=5)

    tk.Label(root, text="Last Name").pack()
    last_name_entry = tk.Entry(root, width=30)
    last_name_entry.pack(pady=5)

    tk.Label(root, text="Email").pack()
    email_entry = tk.Entry(root, width=30)
    email_entry.pack(pady=5)

    tk.Label(root, text="Password").pack()
    password_entry = tk.Entry(root, show="*", width=30)
    password_entry.pack(pady=5)

    tk.Label(root, text="Role").pack()
    role_var = tk.StringVar(value="user")
    tk.Radiobutton(root, text="Job Seeker", variable=role_var, value="user").pack()
    tk.Radiobutton(root, text="Employer", variable=role_var, value="employer").pack()

    def register_action():
        """Handle the registration process"""
        first_name = first_name_entry.get().strip()
        last_name = last_name_entry.get().strip()
        email = email_entry.get().strip()
        password = password_entry.get().strip()
        role = role_var.get()

        if not (first_name and last_name and email and password):
            messagebox.showerror("Error", "All fields are required")
            return

        # Check if email already exists
        for user in users:
            if user.email == email:
                messagebox.showerror("Error", "Email already exists")
                return

        # Create new user with empty skills list
        new_user = User(first_name, last_name, email, password, role, [])

        # Debug print
        print(f"Registering new user: {first_name} {last_name}, Email: {email}, Role: {role}, Skills: []")

        users.append(new_user)
        save_data()
        messagebox.showinfo("Success", "Registration successful! You can now log in.")
        login_screen()

    tk.Button(root, text="Register", command=register_action, width=20).pack(pady=15)
    tk.Button(root, text="Back", command=welcome_screen, width=20).pack()


def login_screen():
    """Display the login screen"""
    clear_screen()

    tk.Label(root, text="Login", font=("Arial", 16)).pack(pady=10)

    tk.Label(root, text="Email").pack()
    email_entry = tk.Entry(root, width=30)
    email_entry.pack(pady=5)

    tk.Label(root, text="Password").pack()
    password_entry = tk.Entry(root, show="*", width=30)
    password_entry.pack(pady=5)

    def login_action():
        """Handle the login process"""
        global current_user
        email = email_entry.get().strip()
        password = password_entry.get().strip()

        # Debug print
        print(f"Attempting login with Email: {email}")

        for user in users:
            if user.email == email and user.password == password:
                current_user = user
                print(f"Login successful - User: {user.first_name}, Role: {user.role}")
                messagebox.showinfo("Success", f"Welcome, {user.first_name}!")

                if user.role == "user":
                    user_dashboard()
                elif user.role == "employer":
                    employer_dashboard()
                elif user.role == "admin":
                    admin_portal()
                return

        messagebox.showerror("Error", "Invalid email or password")

    tk.Button(root, text="Login", command=login_action, width=20).pack(pady=15)
    tk.Button(root, text="Back", command=welcome_screen, width=20).pack()


def upload_resume():
    """Handle resume upload and skill extraction"""
    if not current_user:
        messagebox.showerror("Error", "Please log in first.")
        return

    file_path = filedialog.askopenfilename(
        title="Select Resume",
        filetypes=[("Word Documents", "*.docx *.doc"), ("Text Files", "*.txt"), ("All Files", "*.*")]
    )

    if file_path:
        # Parse resume and extract skills
        extracted_skills = parse_resume(file_path)

        if extracted_skills:
            # Update the user's skills, avoiding duplicates
            for skill in extracted_skills:
                if skill not in current_user.skills:
                    current_user.skills.append(skill)

            # Save updated user data
            save_data()

            messagebox.showinfo(
                "Success",
                f"Resume uploaded! New skills extracted: {', '.join(extracted_skills)}"
            )
        else:
            messagebox.showwarning("Warning", "No skills extracted from the resume.")
    else:
        messagebox.showwarning("Warning", "No file selected.")


def apply_to_job(job):
    """
    Handle job application process

    Args:
        job (Job): The job to apply to
    """
    # Ensure a user is logged in
    if not current_user:
        messagebox.showerror("Error", "Please log in first.")
        return

    # Validate user skills
    if not current_user.skills:
        # Prompt to upload resume if no skills
        response = messagebox.askyesno(
            "Resume Recommended",
            "You haven't uploaded a resume or added skills. Would you like to upload one now?"
        )
        if response:
            upload_resume()
        return

    # Check for skill match
    skill_match = any(skill in job.skills_required for skill in current_user.skills)

    if not skill_match:
        # Warn about skill mismatch
        response = messagebox.askyesno(
            "Skill Mismatch",
            "Your skills don't fully match the job requirements. Do you still want to apply?"
        )
        if not response:
            return

    # Confirm application
    confirm = messagebox.askyesno(
        "Confirm Application",
        f"Do you want to apply to {job.title} at {job.company}?"
    )

    if confirm:
        try:
            # Submit application through message system
            application = message_system.submit_application(
                current_user.email,
                job
            )

            # Update user's applied jobs
            if job.title not in current_user.applied_jobs:
                current_user.applied_jobs.append(job.title)

            # Save data
            save_data()

            # Show success message
            messagebox.showinfo(
                "Application Submitted",
                f"You have successfully applied to {job.title} at {job.company}."
            )

        except Exception as e:
            messagebox.showerror("Application Error", str(e))


def find_matches():
    """Find jobs matching user's skills"""
    clear_screen()
    tk.Label(root, text="Matching Jobs", font=("Arial", 16)).pack(pady=10)

    if not current_user.skills:
        tk.Label(root, text="Upload your resume first to find matching jobs!", font=("Arial", 12)).pack(pady=10)
        tk.Button(root, text="Upload Resume", command=upload_resume).pack(pady=10)
    else:
        matches_frame = tk.Frame(root)
        matches_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        canvas = tk.Canvas(matches_frame)
        scrollbar = tk.Scrollbar(matches_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        matches_found = False
        for job in jobs:
            # Check if any of the user's skills match the job's required skills
            if any(skill in job.skills_required for skill in current_user.skills):
                job_frame = tk.Frame(scrollable_frame, relief=tk.RAISED, borderwidth=1)
                job_frame.pack(fill=tk.X, pady=5)

                # Job details
                tk.Label(job_frame, text=job.title, font=("Arial", 12, "bold")).pack(anchor=tk.W)
                tk.Label(job_frame, text=f"Company: {job.company}").pack(anchor=tk.W)
                tk.Label(job_frame, text=f"Location: {job.location}").pack(anchor=tk.W)
                tk.Label(job_frame, text=f"Skills Required: {', '.join(job.skills_required)}").pack(anchor=tk.W)

                # Apply button for each job
                apply_btn = tk.Button(
                    job_frame,
                    text="Apply",
                    command=lambda j=job: apply_to_job(j)
                )
                apply_btn.pack(anchor=tk.E, padx=10, pady=5)

                matches_found = True

        if not matches_found:
            tk.Label(scrollable_frame, text="No matching jobs found.", font=("Arial", 12)).pack(pady=20)

    # Back to Dashboard button
    tk.Button(root, text="Back to Dashboard", command=user_dashboard).pack(pady=10)


def browse_jobs():
    """Browse all available jobs"""
    clear_screen()
    tk.Label(root, text="All Available Jobs", font=("Arial", 16)).pack(pady=10)

    # Create a scrollable frame for jobs
    matches_frame = tk.Frame(root)
    matches_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

    canvas = tk.Canvas(matches_frame)
    scrollbar = tk.Scrollbar(matches_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    if not jobs:
        tk.Label(scrollable_frame, text="No jobs available at this time.", font=("Arial", 12)).pack(pady=20)
    else:
        for job in jobs:
            job_frame = tk.Frame(scrollable_frame, relief=tk.RAISED, borderwidth=1)
            job_frame.pack(fill=tk.X, pady=5)

            # Job details
            tk.Label(job_frame, text=job.title, font=("Arial", 12, "bold")).pack(anchor=tk.W)
            tk.Label(job_frame, text=f"Company: {job.company}").pack(anchor=tk.W)
            tk.Label(job_frame, text=f"Location: {job.location}").pack(anchor=tk.W)
            tk.Label(job_frame, text=f"Skills Required: {', '.join(job.skills_required)}").pack(anchor=tk.W)

            # Apply button for each job
            apply_btn = tk.Button(
                job_frame,
                text="Apply",
                command=lambda j=job: apply_to_job(j)
            )
            apply_btn.pack(anchor=tk.E, padx=10, pady=5)

    # Back to Dashboard button
    tk.Button(root, text="Back to Dashboard", command=user_dashboard).pack(pady=10)


def user_dashboard():
    """Display the user dashboard"""
    clear_screen()

    tk.Label(root, text=f"Welcome, {current_user.first_name}!", font=("Arial", 16)).pack(pady=10)
    tk.Label(root, text=f"Role: {current_user.role}", font=("Arial", 12)).pack()

    # Display current skills
    skills_text = ", ".join(current_user.skills) if current_user.skills else "No skills added yet"
    tk.Label(root, text=f"Your Skills: {skills_text}").pack(pady=10)

    tk.Button(root, text="Upload Resume", command=upload_resume, width=20).pack(pady=5)
    tk.Button(root, text="Find Matching Jobs", command=find_matches, width=20).pack(pady=5)
    tk.Button(root, text="Browse All Jobs", command=browse_jobs, width=20).pack(pady=5)
    tk.Button(root, text="Messages", command=open_messages_tab, width=20).pack(pady=5)
    tk.Button(root, text="Logout", command=logout, width=20).pack(pady=5)

def open_messages_tab():
    """Enhanced messaging system with improved UI and functionality"""
    if not current_user:
        messagebox.showerror("Error", "Please log in first.")
        return

    clear_screen()
    tk.Label(root, text="Messages", font=("Arial", 16)).pack(pady=10)

    # Create main frame with tabs
    notebook = ttk.Notebook(root)
    notebook.pack(expand=True, fill="both", padx=10, pady=10)

    # Applications Tab
    applications_frame = tk.Frame(notebook)
    notebook.add(applications_frame, text="Applications")

    # Inbox Tab
    inbox_frame = tk.Frame(notebook)
    notebook.add(inbox_frame, text="Inbox")

    # Sent Messages Tab
    sent_messages_frame = tk.Frame(notebook)
    notebook.add(sent_messages_frame, text="Sent Messages")

    # Applications Section
    tk.Label(applications_frame, text="My Job Applications", font=("Arial", 14)).pack(pady=5)

    # Applications Listbox
    applications_listbox = tk.Listbox(applications_frame, width=60, height=10)
    applications_listbox.pack(pady=10)

    # Populate applications
    user_applications = message_system.get_user_applications(current_user.email)
    if user_applications:
        for app in user_applications:
            applications_listbox.insert(tk.END,
                f"{app['job_title']} at {app['company']} - Status: {app['status']}")
    else:
        applications_listbox.insert(tk.END, "No applications submitted yet.")

    # Inbox Section
    tk.Label(inbox_frame, text="Received Messages", font=("Arial", 14)).pack(pady=5)

    # Inbox Listbox
    inbox_listbox = tk.Listbox(inbox_frame, width=60, height=10)
    inbox_listbox.pack(pady=10)

    # Get user's received messages
    received_messages = message_system.get_messages_for_receiver(current_user.email)
    if received_messages:
        for msg in received_messages:
            inbox_listbox.insert(tk.END,
                f"From: {msg['sender_email']}\nMessage: {msg['content']}")
    else:
        inbox_listbox.insert(tk.END, "No messages received.")

    # Sent Messages Section
    tk.Label(sent_messages_frame, text="Sent Messages", font=("Arial", 14)).pack(pady=5)

    # Sent Messages Listbox
    sent_messages_listbox = tk.Listbox(sent_messages_frame, width=60, height=10)
    sent_messages_listbox.pack(pady=10)

    # Get user's sent messages
    sent_messages = [
        msg for msg in message_system.messages
        if msg['sender_email'] == current_user.email
    ]

    if sent_messages:
        for msg in sent_messages:
            sent_messages_listbox.insert(tk.END,
                f"To: {msg['receiver_email']}\nMessage: {msg['content']}")
    else:
        sent_messages_listbox.insert(tk.END, "No messages sent yet.")

    # Send New Message Button
    def send_new_message():
        # Open a dialog to send a new message
        receiver_email = simpledialog.askstring("Send Message", "Enter receiver's email:")
        if receiver_email:
            message_content = simpledialog.askstring("Send Message", "Enter your message:")
            if message_content:
                try:
                    message_system.send_message(
                        current_user.email,
                        receiver_email,
                        message_content
                    )
                    save_data()
                    messagebox.showinfo("Success", "Message sent successfully!")
                    # Refresh the messages view
                    open_messages_tab()
                except Exception as e:
                    messagebox.showerror("Error", str(e))

    # Buttons
    send_message_btn = tk.Button(
        root,
        text="Send New Message",
        command=send_new_message
    )
    send_message_btn.pack(pady=10)

    # Back to Dashboard Button
    back_btn = tk.Button(
        root,
        text="Back to Dashboard",
        command=user_dashboard
    )
    back_btn.pack(pady=10)

def employer_dashboard():
    """Display the employer dashboard"""
    clear_screen()

    tk.Label(root, text=f"Welcome, {current_user.first_name}! (Employer)", font=("Arial", 16)).pack(pady=10)

    tk.Button(root, text="Post a Job", command=post_job_screen, width=20).pack(pady=5)
    tk.Button(root, text="View Your Posted Jobs", command=view_my_jobs, width=20).pack(pady=5)
    tk.Button(root, text="Messages", command=open_messages_tab, width=20).pack(pady=5)
    tk.Button(root, text="Logout", command=logout, width=20).pack(pady=5)

def post_job_screen():
    """Screen to post a new job"""
    clear_screen()

    tk.Label(root, text="Post a New Job", font=("Arial", 16)).pack(pady=10)

    tk.Label(root, text="Job Title").pack()
    title_entry = tk.Entry(root, width=30)
    title_entry.pack(pady=5)

    tk.Label(root, text="Location").pack()
    location_entry = tk.Entry(root, width=30)
    location_entry.pack(pady=5)

    tk.Label(root, text="Description").pack()
    description_entry = tk.Text(root, width=30, height=5)
    description_entry.pack(pady=5)

    tk.Label(root, text="Required Skills (comma separated)").pack()
    skills_entry = tk.Entry(root, width=30)
    skills_entry.pack(pady=5)

    def post_job():
        """Handle job posting"""
        title = title_entry.get().strip()
        location = location_entry.get().strip()
        description = description_entry.get("1.0", tk.END).strip()
        skills_text = skills_entry.get().strip()

        if not (title and location and description and skills_text):
            messagebox.showerror("Error", "All fields are required")
            return

        # Parse skills
        skills_list = [skill.strip() for skill in skills_text.split(",") if skill.strip()]

        # Create new job
        new_job = Job(title, current_user.first_name, location, description, skills_list)
        jobs.append(new_job)

        # Save data
        save_data()
        messagebox.showinfo("Success", "Job posted successfully!")

        # Return to employer dashboard
        employer_dashboard()

    tk.Button(root, text="Post Job", command=post_job, width=20).pack(pady=15)
    tk.Button(root, text="Back", command=employer_dashboard, width=20).pack()

def view_my_jobs():
    """View jobs posted by the current employer"""
    clear_screen()

    tk.Label(root, text="Your Posted Jobs", font=("Arial", 16)).pack(pady=10)

    # Create a scrollable frame for jobs
    matches_frame = tk.Frame(root)
    matches_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

    canvas = tk.Canvas(matches_frame)
    scrollbar = tk.Scrollbar(matches_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    jobs_found = False

    for job in jobs:
        if job.company == current_user.first_name:
            job_frame = tk.Frame(scrollable_frame, relief=tk.RAISED, borderwidth=1)
            job_frame.pack(fill=tk.X, pady=5)

            tk.Label(job_frame, text=f"{job.title}", font=("Arial", 12, "bold")).pack(anchor=tk.W)
            tk.Label(job_frame, text=f"Location: {job.location}").pack(anchor=tk.W)
            tk.Label(job_frame, text=f"Skills Required: {', '.join(job.skills_required)}").pack(anchor=tk.W)

            jobs_found = True

    if not jobs_found:
        tk.Label(scrollable_frame, text="You haven't posted any jobs yet.", font=("Arial", 12)).pack(pady=20)

    # Back to Dashboard button
    tk.Button(root, text="Back to Dashboard", command=employer_dashboard).pack(pady=10)

def admin_portal():
    """Display the admin portal"""
    clear_screen()

    tk.Label(root, text="Admin Portal", font=("Arial", 16)).pack(pady=10)

    tk.Button(root, text="View All Users", command=view_users, width=20).pack(pady=5)
    tk.Button(root, text="View All Jobs", command=view_all_jobs, width=20).pack(pady=5)
    tk.Button(root, text="Delete Users", command=delete_users, width=20).pack(pady=5)
    tk.Button(root, text="Logout", command=logout, width=20).pack(pady=5)

def view_users():
    """View all registered users"""
    clear_screen()

    tk.Label(root, text="Registered Users", font=("Arial", 16)).pack(pady=10)

    # Create a scrollable frame for users
    matches_frame = tk.Frame(root)
    matches_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

    canvas = tk.Canvas(matches_frame)
    scrollbar = tk.Scrollbar(matches_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    for user in users:
        user_frame = tk.Frame(scrollable_frame, relief=tk.RAISED, borderwidth=1)
        user_frame.pack(fill=tk.X, padx=20, pady=5)

        tk.Label(user_frame, text=f"{user.first_name} {user.last_name}", font=("Arial", 12, "bold")).pack(anchor=tk.W)
        tk.Label(user_frame, text=f"Email: {user.email}").pack(anchor=tk.W)
        tk.Label(user_frame, text=f"Role: {user.role}").pack(anchor=tk.W)

        skills_text = ", ".join(user.skills) if hasattr(user, 'skills') and user.skills else "None"
        tk.Label(user_frame, text=f"Skills: {skills_text}").pack(anchor=tk.W)

    tk.Button(root, text="Back", command=admin_portal, width=20).pack(pady=15)

def view_all_jobs():
    """View all jobs in the system"""
    clear_screen()

    tk.Label(root, text="All Jobs", font=("Arial", 16)).pack(pady=10)

    # Create a scrollable frame for jobs
    matches_frame = tk.Frame(root)
    matches_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

    canvas = tk.Canvas(matches_frame)
    scrollbar = tk.Scrollbar(matches_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    for job in jobs:
        job_frame = tk.Frame(scrollable_frame, relief=tk.RAISED, borderwidth=1)
        job_frame.pack(fill=tk.X, padx=20, pady=5)

        tk.Label(job_frame, text=f"{job.title}", font=("Arial", 12, "bold")).pack(anchor=tk.W)
        tk.Label(job_frame, text=f"Company: {job.company}").pack(anchor=tk.W)
        tk.Label(job_frame, text=f"Location: {job.location}").pack(anchor=tk.W)
        tk.Label(job_frame, text=f"Skills Required: {', '.join(job.skills_required)}").pack(anchor=tk.W)

    tk.Button(root, text="Back", command=admin_portal, width=20).pack(pady=15)


def delete_users():
    """Screen to delete users"""
    clear_screen()

    tk.Label(root, text="Delete Users", font=("Arial", 16)).pack(pady=10)

    # Create a frame for user selection
    frame = tk.Frame(root)
    frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

    # Create a canvas with scrollbar
    canvas = tk.Canvas(frame)
    scrollbar = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Var to track selected users
    selected_users = []

    def on_user_select(user, var):
        if var.get():
            selected_users.append(user)
        else:
            selected_users.remove(user)

    # Create checkboxes for each user
    for user in users:
        # Skip admin users
        if user.role == 'admin':
            continue

        # Create a frame for each user
        user_frame = tk.Frame(scrollable_frame, relief=tk.RAISED, borderwidth=1)
        user_frame.pack(fill=tk.X, padx=5, pady=5)

        # Checkbox variable
        var = tk.BooleanVar()

        # Checkbox
        cb = tk.Checkbutton(
            user_frame,
            text=f"{user.first_name} {user.last_name} ({user.email})",
            variable=var,
            command=lambda u=user, v=var: on_user_select(u, v)
        )
        cb.pack(side=tk.LEFT)

    def delete_selected_users():
        """Remove selected users"""
        if not selected_users:
            messagebox.showwarning("Warning", "No users selected")
            return

        # Confirm deletion
        confirm = messagebox.askyesno(
            "Confirm Deletion",
            f"Are you sure you want to delete {len(selected_users)} user(s)?"
        )

        if confirm:
            for user in selected_users:
                if user.role != 'admin':  # Prevent deleting admin users
                    users.remove(user)

            save_data()
            messagebox.showinfo("Success", f"{len(selected_users)} user(s) deleted")
            delete_users()  # Refresh the view

    # Delete button
    delete_btn = tk.Button(
        root,
        text="Delete Selected Users",
        command=delete_selected_users
    )
    delete_btn.pack(pady=10)

    # Back button
    back_btn = tk.Button(
        root,
        text="Back to Admin Portal",
        command=admin_portal
    )
    back_btn.pack(pady=10)

def welcome_screen():
    """Display the welcome screen"""
    clear_screen()

    tk.Label(root, text="SkillMatcher App", font=("Arial", 18)).pack(pady=20)

    tk.Button(root, text="Register", command=register_screen, width=20, height=2).pack(pady=10)
    tk.Button(root, text="Login", command=login_screen, width=20, height=2).pack(pady=10)
    tk.Button(root, text="Admin Portal", command=admin_portal, width=20, height=2).pack(pady=10)

def logout():
    """Log out the current user and return to welcome screen"""
    global current_user
    current_user = None
    welcome_screen()

def clear_screen():
    """Clear all widgets from the screen"""
    for widget in root.winfo_children():
        widget.destroy()

# App Launch
# App Launch
def main():
    global root
    root = tk.Tk()
    root.title("SkillMatcher App")
    root.geometry("500x600")

    # Try to load saved data first
    load_data()

    # If no users were loaded, use the sample data
    if not users:
        users.extend(sample_users)
        employers.extend(sample_employers)
        jobs.extend(sample_jobs)
        save_data()

    # Start with welcome screen
    welcome_screen()

    root.mainloop()

if __name__ == "__main__":
    main()
