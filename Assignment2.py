import tkinter as tk
from tkinter import ttk, messagebox
import csv
import re
import pandas as pd
import os


class User:
    def __init__(self, user_id, password, user_type):
        self.user_id = user_id
        self.password = password
        self.user_type = user_type
        self.blocked = False
        self.data = {}  # To store user-specific data


class Teacher(User):
    def __init__(
        self, user_id, password, name, email, dob, gender, joining_year, department
    ):
        super().__init__(user_id, password, "Teacher")
        self.name = name
        self.email = email
        self.dob = dob
        self.gender = gender
        self.joining_year = joining_year
        self.department = department
        self.courses_taught = []  # Added attribute


class Student(User):
    def __init__(
        self,
        user_id,
        password,
        name,
        email,
        dob,
        gender,
        roll_no,
        cg,
        department,
        semester,
    ):
        super().__init__(user_id, password, "Student")
        self.name = name
        self.email = email
        self.dob = dob
        self.gender = gender
        self.roll_no = roll_no
        self.cg = cg
        self.department = department
        self.semester = semester
        self.courses_taken = []  # Added attribute


class UGStudent(Student):
    def __init__(
        self,
        user_id,
        password,
        name,
        email,
        dob,
        gender,
        roll_no,
        cg,
        department,
        semester,
        program_type,
    ):
        super().__init__(
            user_id,
            password,
            name,
            email,
            dob,
            gender,
            roll_no,
            cg,
            department,
            semester,
        )
        self.program_type = program_type


class PGStudent(Student):
    def __init__(
        self,
        user_id,
        password,
        name,
        email,
        dob,
        gender,
        roll_no,
        cg,
        department,
        semester,
        research_area,
        guiding_professor,
    ):
        super().__init__(
            user_id,
            password,
            name,
            email,
            dob,
            gender,
            roll_no,
            cg,
            department,
            semester,
        )
        self.research_area = research_area
        self.guiding_professor = guiding_professor

class DetailsWindow:
    def __init__(self, root, user):
        self.root = root
        self.root.title("User Details")
        self.user = user

        self.create_details_page()

    def create_details_page(self):
        details_frame = ttk.Frame(self.root, padding="10")
        details_frame.grid(row=0, column=0, sticky="nsew")

        tk.Label(
            details_frame, text=f"Details for {self.user.name} ({self.user.user_type})"
        ).grid(row=0, column=0, columnspan=2, pady=10)

        tk.Label(details_frame, text="Name:").grid(row=1, column=0, pady=5)
        tk.Label(details_frame, text=self.user.name).grid(row=1, column=1, pady=5)

        tk.Label(details_frame, text="Email:").grid(row=2, column=0, pady=5)
        tk.Label(details_frame, text=self.user.email).grid(row=2, column=1, pady=5)

        tk.Label(details_frame, text="DOB:").grid(row=3, column=0, pady=5)
        tk.Label(details_frame, text=self.user.dob).grid(row=3, column=1, pady=5)

        # Additional labels based on user type
        if isinstance(self.user, Teacher):
            tk.Label(details_frame, text="Joining Year:").grid(row=4, column=0, pady=5)
            tk.Label(details_frame, text=self.user.joining_year).grid(
                row=4, column=1, pady=5
            )
            tk.Label(details_frame, text="Department:").grid(row=5, column=0, pady=5)
            tk.Label(details_frame, text=self.user.department).grid(
                row=5, column=1, pady=5
            )

            # Check if the courses_taught attribute exists before attempting to access it
            if hasattr(self.user, "courses_taught"):
                tk.Label(details_frame, text="Courses Taught:").grid(
                    row=6, column=0, pady=5
                )
                tk.Label(details_frame, text=", ".join(self.user.courses_taught)).grid(
                    row=6, column=1, pady=5
                )

        elif isinstance(self.user, UGStudent):
            tk.Label(details_frame, text="Program Type:").grid(row=4, column=0, pady=5)
            tk.Label(details_frame, text=self.user.program_type).grid(
                row=4, column=1, pady=5
            )

        elif isinstance(self.user, PGStudent):
            tk.Label(details_frame, text="Research Area:").grid(row=4, column=0, pady=5)
            tk.Label(details_frame, text=self.user.research_area).grid(
                row=4, column=1, pady=5
            )
            tk.Label(details_frame, text="Guiding Professor:").grid(
                row=5, column=0, pady=5
            )
            tk.Label(details_frame, text=self.user.guiding_professor).grid(
                row=5, column=1, pady=5
            )

    def run(self):
        self.root.mainloop()




class Application:
    def __init__(self, root):
        self.root = root
        self.root.title("University System")

        self.users = []  # To store user data
        self.current_user = None  # Current user
        self.new_user_registered = (
            False  # Flag to track whether a new user is registered
        )

        # Initialize login/signup frame as None
        self.login_signup_frame = None

        # Load existing data from CSV file
        self.load_data_from_csv()

        # Creating login/signup page
        self.create_login_signup_page()

    def load_data_from_csv(self):
        df = pd.DataFrame()  # Initialize df outside the if block

        if os.path.exists("user_data.csv") and os.path.getsize("user_data.csv") > 0:
            df = pd.read_csv("user_data.csv")
            self.users = []

            for _, row in df.iterrows():
                user_type = row.get(
                    "user_type", ""
                )  # Use get to handle missing columns
                user_id = row.get("user_id", "")
                password = row.get("password", "")

                if user_type == "Teacher":
                    user = Teacher(
                        user_id,
                        password,
                        row.get("name", ""),
                        row.get("email", ""),
                        row.get("dob", ""),
                        row.get("gender", ""),
                        row.get("joining_year", ""),
                        row.get("department", ""),
                    )

                    # Check if 'courses_taught' is a valid string before splitting
                    courses_taught = row.get("courses_taught", "")
                    user.courses_taught = (
                        [course.strip() for course in courses_taught.split(",")]
                        if isinstance(courses_taught, str)
                        else []
                    )
                elif user_type == "UG Student":
                    user = UGStudent(
                        user_id,
                        password,
                        row.get("name", ""),
                        row.get("email", ""),
                        row.get("dob", ""),
                        row.get("gender", ""),
                        row.get("roll_no", ""),
                        row.get("cg", ""),
                        row.get("department", ""),
                        row.get("semester", ""),
                        row.get("program_type", ""),
                    )
                elif user_type == "PG Student":
                    user = PGStudent(
                        user_id,
                        password,
                        row.get("name", ""),
                        row.get("email", ""),
                        row.get("dob", ""),
                        row.get("gender", ""),
                        row.get("roll_no", ""),
                        row.get("cg", ""),
                        row.get("department", ""),
                        row.get("semester", ""),
                        row.get("research_area", ""),
                        row.get("guiding_professor", ""),
                    )
                else:
                    continue  # Skip unknown user types

                self.users.append(user)

    def save_data_to_csv(self):
        data = {
            "user_id": [],
            "password": [],
            "user_type": [],
            "name": [],
            "email": [],
            "dob": [],
            "gender": [],
            "joining_year": [],
            "department": [],
            "courses_taught": [],
            "roll_no": [],
            "cg": [],
            "semester": [],
            "program_type": [],
            "research_area": [],
            "guiding_professor": [],
        }

        for user in self.users:
            data["user_id"].append(user.user_id)
            data["password"].append(user.password)
            data["user_type"].append(user.user_type)
            data["name"].append(user.name)
            data["email"].append(user.email)
            data["dob"].append(user.dob)
            data["gender"].append(user.gender)

            if isinstance(user, Teacher):
                data["joining_year"].append(user.joining_year)
                data["department"].append(user.department)
                data["courses_taught"].append(", ".join(user.courses_taught))
                data["roll_no"].append("")
                data["cg"].append("")
                data["semester"].append("")
                data["program_type"].append("")
                data["research_area"].append("")
                data["guiding_professor"].append("")
            elif isinstance(user, UGStudent):
                data["joining_year"].append("")
                data["department"].append("")
                data["courses_taught"].append("")
                data["roll_no"].append(user.roll_no)
                data["cg"].append(user.cg)
                data["semester"].append(user.semester)
                data["program_type"].append(user.program_type)
                data["research_area"].append("")
                data["guiding_professor"].append("")
            elif isinstance(user, PGStudent):
                data["joining_year"].append("")
                data["department"].append("")
                data["courses_taught"].append("")
                data["roll_no"].append(user.roll_no)
                data["cg"].append(user.cg)
                data["semester"].append(user.semester)
                data["program_type"].append("")
                data["research_area"].append(user.research_area)
                data["guiding_professor"].append(user.guiding_professor)

        df = pd.DataFrame(data)
        df.to_csv("user_data.csv", index=False)

    def create_login_signup_page(self):
        # Check if login_signup_frame already exists
        if self.login_signup_frame:
            self.login_signup_frame.destroy()  # Destroy the existing login_signup_frame

        login_signup_frame = ttk.Frame(self.root, padding="10")
        login_signup_frame.grid(row=0, column=0, sticky="nsew")
        ttk.Button(
            login_signup_frame, text="Deregister", command=self.deregister_user
        ).grid(row=0, column=2, padx=5)

        ttk.Button(login_signup_frame, text="Login", command=self.login).grid(
            row=0, column=0, padx=5
        )
        ttk.Button(login_signup_frame, text="Signup", command=self.signup).grid(
            row=0, column=1, padx=5
        )

        # If a new user is registered, proceed to the main page
        if self.new_user_registered:
            self.populate_email_field()  # Populate email field

            self.create_main_page()
            self.new_user_registered = False  # Reset the flag

        self.login_signup_frame = login_signup_frame  # Store the login/signup frame

    def login(self):
        login_window = tk.Toplevel(self.root)
        login_window.title("Login")

        tk.Label(login_window, text="User ID:").grid(row=0, column=0, pady=5)
        tk.Label(login_window, text="Password:").grid(row=1, column=0, pady=5)

        user_id_entry = tk.Entry(login_window)
        password_entry = tk.Entry(login_window, show="*")

        user_id_entry.grid(row=0, column=1, pady=5)
        password_entry.grid(row=1, column=1, pady=5)

        login_button = ttk.Button(
            login_window,
            text="Login",
            command=lambda: self.authenticate(
                login_window, user_id_entry.get(), password_entry.get()
            ),
        )
        login_button.grid(row=2, column=0, columnspan=2, pady=10)
        # Counter for login attempts
        self.login_attempts = 0

        # Handle window closure
        login_window.protocol(
            "WM_DELETE_WINDOW", lambda: self.handle_window_close(login_window)
        )

    def authenticate(self, login_window, user_id, password):
        user = self.find_user(user_id)

        if user and user.password == password:
            # Reset login attempts on successful login
            self.login_attempts = 0

            self.current_user = user
            login_window.withdraw()  # Hide the login window instead of destroying it
            self.create_main_page()
        else:
            # Increment login attempts
            self.login_attempts += 1

            # Check if the user has exhausted the allowed attempts
            if self.login_attempts >= 3:
                # Block the user in the CSV file
                if user:
                    user.blocked = True
                    self.save_data_to_csv()

             # Display a message box indicating that the user is blocked
                messagebox.showerror(
                    "Account Blocked",
                    "You have entered the wrong password multiple times. Your account has been blocked.",
                )
                # login_window.destroy()  # Close the login window

                # Go back to the login/signup page
                self.create_login_signup_page()
            else:
                # Display an error message for wrong password
                if(self.login_attempts < 3):
                    messagebox.showerror(
                    "Authentication Failed", "Invalid User ID or Password"
                )
                if(self.login_attempts >= 3):
                    messagebox.showerror(
                    "Account Blocked"
                )



    def signup(self):
        signup_window = tk.Toplevel(self.root)
        signup_window.title("Signup")

        tk.Label(signup_window, text="User ID (Email):").grid(row=0, column=0, pady=5)
        tk.Label(signup_window, text="Password:").grid(row=1, column=0, pady=5)
        tk.Label(signup_window, text="Confirm Password:").grid(row=2, column=0, pady=5)
        tk.Label(signup_window, text="User Type:").grid(row=3, column=0, pady=5)

        user_id_entry = tk.Entry(signup_window)
        password_entry = tk.Entry(signup_window, show="*")
        confirm_password_entry = tk.Entry(signup_window, show="*")
        user_type_var = tk.StringVar()
        user_type_combobox = ttk.Combobox(
            signup_window,
            textvariable=user_type_var,
            values=["Teacher", "UG Student", "PG Student"],
        )
        user_type_combobox.set("Teacher")

        user_id_entry.grid(row=0, column=1, pady=5)
        password_entry.grid(row=1, column=1, pady=5)
        confirm_password_entry.grid(row=2, column=1, pady=5)
        user_type_combobox.grid(row=3, column=1, pady=5)

        signup_button = ttk.Button(
            signup_window,
            text="Signup",
            command=lambda: self.register_user(
                signup_window,
                user_id_entry.get(),
                password_entry.get(),
                confirm_password_entry.get(),
                user_type_var.get(),
            ),
        )
        signup_button.grid(row=4, column=0, columnspan=2, pady=10)

        # Handle window closure
        signup_window.protocol(
            "WM_DELETE_WINDOW", lambda: self.handle_window_close(signup_window)
        )

    def register_user(
        self, signup_window, user_id, password, confirm_password, user_type
        ):
        if not self.is_valid_password(password, confirm_password):
            messagebox.showerror(
                "Invalid Password",
                "Password must be 8-12 characters long and contain at least one upper case, one digit, one lower case, and one special character.",
            )
            return

        if not self.is_valid_email(user_id):
            messagebox.showerror("Invalid Email", "Please enter a valid email address.")
            return

        if not self.is_unique_user_id(user_id):
            messagebox.showerror(
                "Duplicate User ID",
                "User ID already exists. Please choose a different one.",
            )
            return

        new_user = None

        if user_type == "Teacher":
            new_user = Teacher(user_id, password, "", "", "", "", "", "")
        elif user_type == "UG Student":
            new_user = UGStudent(user_id, password, "", "", "", "", "", "", "", "", "")
        elif user_type == "PG Student":
            new_user = PGStudent(
                user_id, password, "", "", "", "", "", "", "", "", "", ""
            )
        else:
            messagebox.showerror(
                "Invalid User Type", "Please select a valid user type."
            )
            return

        self.users.append(new_user)
        self.current_user = new_user
        self.new_user_registered = True  # Set the flag

        # Save the user data to the CSV file
        self.save_data_to_csv()
        signup_window.destroy()

        # If login/signup page is already created, update it; otherwise, create it
        if hasattr(self, "login_signup_frame"):
            self.create_login_signup_page()
        else:
            self.create_main_page()

    def is_valid_password(self, password, confirm_password):
        if len(password) < 8 or len(password) > 12:
            return False

        if not re.search("[A-Z]", password):
            return False

        if not re.search("[a-z]", password):
            return False

        if not re.search("[0-9]", password):
            return False

        if not re.search("[!@#$%&*]", password):
            return False

        if password != confirm_password:
            return False

        if " " in password:
            return False

        return True

    def is_valid_email(self, email):
        # A simple check for a valid email format
        return re.match(r"[^@]+@[^@]+\.[^@]+", email)

    def is_unique_user_id(self, user_id):
        for user in self.users:
            if user.user_id == user_id:
                return False
        return True

    def find_user(self, user_id):
        # Iterate through the list of users and find the matching user_id
        for user in self.users:
           
                

            if user.user_id == user_id :
                
                return user
        return None


    def edit_profile(self):
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Edit Profile")

        tk.Label(edit_window, text="New Name:").grid(row=0, column=0, pady=5)
        new_name_entry = tk.Entry(edit_window)
        new_name_entry.grid(row=0, column=1, pady=5)

        tk.Label(edit_window, text="New DOB:").grid(row=1, column=0, pady=5)
        new_dob_entry = tk.Entry(edit_window)
        new_dob_entry.grid(row=1, column=1, pady=5)

        tk.Label(edit_window, text="New Gender:").grid(row=2, column=0, pady=5)
        new_gender_entry = tk.Entry(edit_window)
        new_gender_entry.grid(row=2, column=1, pady=5)

        tk.Label(edit_window, text="New Department:").grid(row=3, column=0, pady=5)
        new_department_entry = tk.Entry(edit_window)
        new_department_entry.grid(row=3, column=1, pady=5)

        if isinstance(self.current_user, Teacher):
            tk.Label(edit_window, text="New Joining Year:").grid(
                row=4, column=0, pady=5
            )
            new_joining_year_entry = tk.Entry(edit_window)
            new_joining_year_entry.grid(row=4, column=1, pady=5)

            tk.Label(
                edit_window, text="New Courses Taught (comma-separated):"
            ).grid(row=5, column=0, pady=5)
            new_courses_taught_entry = tk.Entry(edit_window)
            new_courses_taught_entry.grid(row=5, column=1, pady=5)

        elif isinstance(self.current_user, UGStudent):
            tk.Label(edit_window, text="New Roll No:").grid(
                row=4, column=0, pady=5
            )
            new_roll_no_entry = tk.Entry(edit_window)
            new_roll_no_entry.grid(row=4, column=1, pady=5)

            tk.Label(edit_window, text="New Semester:").grid(
                row=5, column=0, pady=5
            )
            new_semester_entry = tk.Entry(edit_window)
            new_semester_entry.grid(row=5, column=1, pady=5)

            tk.Label(edit_window, text="New CGPA:").grid(
                row=6, column=0, pady=5
            )
            new_cg_entry = tk.Entry(edit_window)
            new_cg_entry.grid(row=6, column=1, pady=5)

            tk.Label(edit_window, text="New Program Type:").grid(
                row=7, column=0, pady=5
            )
            new_program_type_entry = tk.Entry(edit_window)
            new_program_type_entry.grid(row=7, column=1, pady=5)

        elif isinstance(self.current_user, PGStudent):
            tk.Label(edit_window, text="New Roll No:").grid(
                row=4, column=0, pady=5
            )
            new_roll_no_entry = tk.Entry(edit_window)
            new_roll_no_entry.grid(row=4, column=1, pady=5)

            tk.Label(edit_window, text="New Semester:").grid(
                row=5, column=0, pady=5
            )
            new_semester_entry = tk.Entry(edit_window)
            new_semester_entry.grid(row=5, column=1, pady=5)

            tk.Label(edit_window, text="New CGPA:").grid(
                row=6, column=0, pady=5
            )
            new_cg_entry = tk.Entry(edit_window)
            new_cg_entry.grid(row=6, column=1, pady=5)

            tk.Label(edit_window, text="New Research Area:").grid(
                row=7, column=0, pady=5
            )
            new_research_area_entry = tk.Entry(edit_window)
            new_research_area_entry.grid(row=7, column=1, pady=5)

            tk.Label(edit_window, text="New Guiding Professor:").grid(
                row=8, column=0, pady=5
            )
            new_guiding_professor_entry = tk.Entry(edit_window)
            new_guiding_professor_entry.grid(row=8, column=1, pady=5)

        # Set default values in the entry fields
        new_name_entry.insert(0, self.current_user.name)
        new_dob_entry.insert(0, self.current_user.dob)
        new_gender_entry.insert(0, self.current_user.gender)
        new_department_entry.insert(0, self.current_user.department)

        if isinstance(self.current_user, Teacher):
            new_joining_year_entry.insert(0, self.current_user.joining_year)
            new_courses_taught_entry.insert(
                0, ", ".join(self.current_user.courses_taught)
            )

        elif isinstance(self.current_user, UGStudent):
            new_roll_no_entry.insert(0, self.current_user.roll_no)
            new_semester_entry.insert(0, self.current_user.semester)
            new_cg_entry.insert(0, self.current_user.cg)
            new_program_type_entry.insert(0, self.current_user.program_type)

        elif isinstance(self.current_user, PGStudent):
            new_roll_no_entry.insert(0, self.current_user.roll_no)
            new_semester_entry.insert(0, self.current_user.semester)
            new_cg_entry.insert(0, self.current_user.cg)
            new_research_area_entry.insert(0, self.current_user.research_area)
            new_guiding_professor_entry.insert(0, self.current_user.guiding_professor)

        ttk.Button(
            edit_window,
            text="Save Changes",
            command=lambda: self.save_changes(
                edit_window,
                new_name_entry.get(),
                new_gender_entry.get(),
                new_dob_entry.get(),
                new_department_entry.get(),
                new_joining_year_entry.get()
                if isinstance(self.current_user, Teacher)
                else None,
                
                new_program_type_entry.get()
                if isinstance(self.current_user, UGStudent)
                else None,
                new_research_area_entry.get()
                if isinstance(self.current_user, PGStudent)
                else None,
                new_guiding_professor_entry.get()
                if isinstance(self.current_user, PGStudent)
                else None,
                new_courses_taught_entry.get()
                if isinstance(self.current_user, Teacher)
                else None,
                new_roll_no_entry.get()
                if isinstance(self.current_user, (UGStudent, PGStudent))
                else None,
                new_semester_entry.get()
                if isinstance(self.current_user, (UGStudent, PGStudent))
                else None,
                new_cg_entry.get()
                if isinstance(self.current_user, (UGStudent, PGStudent))
                else None,
            ),
        ).grid(row=9, column=0, columnspan=2, pady=10)


    def save_changes(
        self,
        edit_window,
        new_name,
        new_gender,
        new_dob,
        new_department,
        new_joining_year,
        new_program_type,
        new_research_area,
        new_guiding_professor,
        new_courses_taught,
        new_roll_no,
        new_semester,
        new_cg,
         ):
        # Update the user data with the new values
        self.current_user.name = new_name if new_name else self.current_user.name
        self.current_user.gender = new_gender if new_gender else self.current_user.gender
        self.current_user.dob = new_dob if new_dob else self.current_user.dob
        self.current_user.department = new_department if new_department else self.current_user.department

        # Update the new attributes
        if isinstance(self.current_user, Teacher):
            self.current_user.joining_year = (
                new_joining_year if new_joining_year else self.current_user.joining_year
            )
            self.current_user.courses_taught = (
                [course.strip() for course in new_courses_taught.split(",")]
                if new_courses_taught
                else self.current_user.courses_taught
            )

        elif isinstance(self.current_user, UGStudent):
            self.current_user.roll_no = new_roll_no if new_roll_no else self.current_user.roll_no
            self.current_user.semester = new_semester if new_semester else self.current_user.semester
            self.current_user.cg = new_cg if new_cg else self.current_user.cg
            self.current_user.program_type = (
                new_program_type if new_program_type else self.current_user.program_type
            )

        elif isinstance(self.current_user, PGStudent):
            self.current_user.roll_no = new_roll_no if new_roll_no else self.current_user.roll_no
            self.current_user.semester = new_semester if new_semester else self.current_user.semester
            self.current_user.cg = new_cg if new_cg else self.current_user.cg
            self.current_user.research_area = (
                new_research_area if new_research_area else self.current_user.research_area
            )
            self.current_user.guiding_professor = (
                new_guiding_professor if new_guiding_professor else self.current_user.guiding_professor
            )

        #  Close the edit window
        edit_window.destroy()

        # Show the login/signup page again without recreating it
        self.create_login_signup_page()
        self.save_data_to_csv()

    def create_main_page(self):
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky="nsew")

        tk.Label(
            self.main_frame,
            text=f"Welcome, {self.current_user.name} ",
        ).grid(row=0, column=0, columnspan=2, pady=10)

        tk.Label(self.main_frame, text="Name:").grid(row=1, column=0, pady=5)
        tk.Label(self.main_frame, text=self.current_user.name).grid(
            row=1, column=1, pady=5
        )

        tk.Label(self.main_frame, text="Email:").grid(row=2, column=0, pady=5)
        tk.Label(self.main_frame, text=self.current_user.user_id).grid(
            row=2, column=1, pady=5
        )  # Display the prepopulated email

        tk.Label(self.main_frame, text="DOB:").grid(row=3, column=0, pady=5)
        tk.Label(self.main_frame, text=self.current_user.dob).grid(
            row=3, column=1, pady=5
        )

        tk.Label(self.main_frame, text="Gender:").grid(row=4, column=0, pady=5)
        tk.Label(self.main_frame, text=self.current_user.gender).grid(
            row=4, column=1, pady=5
        )

        tk.Label(self.main_frame, text="Department:").grid(row=5, column=0, pady=5)
        tk.Label(self.main_frame, text=self.current_user.department).grid(
            row=5, column=1, pady=5
        )

        if isinstance(self.current_user, Teacher):
            tk.Label(self.main_frame, text="Joining Year:").grid(
                row=6, column=0, pady=5
            )
            tk.Label(self.main_frame, text=self.current_user.joining_year).grid(
                row=6, column=1, pady=5
            )
            tk.Label(self.main_frame, text="Courses Taught:").grid(
                row=7, column=0, pady=5
            )
            tk.Label(
                self.main_frame, text=", ".join(self.current_user.courses_taught)
            ).grid(row=7, column=1, pady=5)

        elif isinstance(self.current_user, UGStudent) or isinstance(
            self.current_user, PGStudent
        ):
            tk.Label(self.main_frame, text="Roll No:").grid(row=6, column=0, pady=5)
            tk.Label(self.main_frame, text=self.current_user.roll_no).grid(
                row=6, column=1, pady=5
            )

            tk.Label(self.main_frame, text="Semester:").grid(row=7, column=0, pady=5)
            tk.Label(self.main_frame, text=self.current_user.semester).grid(
                row=7, column=1, pady=5
            )

            tk.Label(self.main_frame, text="CGPA:").grid(row=8, column=0, pady=5)
            tk.Label(self.main_frame, text=self.current_user.cg).grid(
                row=8, column=1, pady=5
            )

            if isinstance(self.current_user, UGStudent):
                tk.Label(self.main_frame, text="Program Type:").grid(
                    row=9, column=0, pady=5
                )
                tk.Label(self.main_frame, text=self.current_user.program_type).grid(
                    row=9, column=1, pady=5
                )

            elif isinstance(self.current_user, PGStudent):
                tk.Label(self.main_frame, text="Research Area:").grid(
                    row=9, column=0, pady=5
                )
                tk.Label(self.main_frame, text=self.current_user.research_area).grid(
                    row=9, column=1, pady=5
                )
                tk.Label(self.main_frame, text="Guiding Professor:").grid(
                    row=10, column=0, pady=5
                )
                tk.Label(
                    self.main_frame, text=self.current_user.guiding_professor
                ).grid(row=10, column=1, pady=5)

        ttk.Button(
                self.main_frame, text="Edit Profile", command=self.edit_profile
            ).grid(row=11, column=0, columnspan=2, pady=10)

        ttk.Button(self.main_frame, text="Logout", command=self.logout).grid(
                row=12, column=0, pady=10
            )

    def logout(self):
        # Go back to the login/signup page
        self.create_login_signup_page()

    def populate_email_field(self):
        # If the current user is not None, and the login/signup frame exists
        if (
            self.current_user
            and hasattr(self, "login_signup_frame")
            and self.login_signup_frame.winfo_exists()
        ):
            # Find the Entry widget for email on the login/signup frame
            for widget in self.login_signup_frame.winfo_children():
                if (
                    isinstance(widget, tk.Entry)
                    and widget.grid_info()["row"] == 0
                    and widget.grid_info()["column"] == 1
                ):
                    # Set the email field with the user's email
                    widget.insert(0, self.current_user.email)
                    break

    def deregister_user(self):
        deregister_window = tk.Toplevel(self.root)
        deregister_window.title("Deregister User")

        tk.Label(deregister_window, text="User ID:").grid(row=0, column=0, pady=5)
        tk.Label(deregister_window, text="Password:").grid(row=1, column=0, pady=5)

        user_id_entry = tk.Entry(deregister_window)
        password_entry = tk.Entry(deregister_window, show="*")

        user_id_entry.grid(row=0, column=1, pady=5)
        password_entry.grid(row=1, column=1, pady=5)

        deregister_button = ttk.Button(
            deregister_window,
            text="Deregister",
            command=lambda: self.authenticate_deregistration(
                deregister_window, user_id_entry.get(), password_entry.get()
            ),
        )
        deregister_button.grid(row=2, column=0, columnspan=2, pady=10)

        # Handle window closure
        deregister_window.protocol(
            "WM_DELETE_WINDOW", lambda: self.handle_window_close(deregister_window)
        )

    def authenticate_deregistration(self, deregister_window, user_id, password):
        user = self.find_user(user_id)

        if user and user.password == password:
            # Ask for confirmation before proceeding with deregistration
            confirmation = messagebox.askyesno(
                "Confirm Deregistration",
                "Are you sure you want to deregister? This action cannot be undone.",
            )
            if confirmation:
                # Remove user data from CSV and local data structure
                self.users.remove(user)
                self.save_data_to_csv()

                # Display a message box indicating successful deregistration
                messagebox.showinfo(
                    "Deregistration Successful",
                    "Your account has been deregistered. All your data has been deleted.",
                )

                # Close the deregister window
                deregister_window.destroy()

                # Go back to the login/signup page
                self.create_login_signup_page()
        else:
            messagebox.showerror("Authentication Failed", "Invalid User ID or Password")

    def run(self):
        self.root.mainloop()

    def handle_window_close(self, window):
        # Handle the window closure based on the window type (login or signup)
        if (
            window.winfo_exists()
        ):  # Check if the window still exists (not already destroyed)
            window.withdraw()  # Destroy the window


if __name__ == "__main__":
    root = tk.Tk()
    app = Application(root)
    app.run()
