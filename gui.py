import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from models import User, Course, Instructor, Registration
from utils import validate_srn, validate_password
import os
import csv

class CourseRegistrationApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Course Registration System")
        self.geometry("900x600")
        self.resizable(False, False)
        self.current_user = None
        self.frames = {}

        container = ttk.Frame(self)
        container.pack(fill="both", expand=True)

        for F in (LoginPage, SignUpPage, AdminPortal, UserPortal):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(LoginPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def login(self, srn_or_email, password):
        # Reload user from database to ensure fresh data
        print(f"Login called with srn_or_email: '{srn_or_email}' and password: '{password}'")
        user = User.get_user_by_srn(srn_or_email)
        if not user:
            user = User.get_user_by_email(srn_or_email)
        if user:
            print(f"Login attempt for user: {user.srn}, email: {user.email}")
            print(f"Stored password hash: {user.password_hash}")
        else:
            print("No user found with given SRN or email.")
        if user and user.check_password(password):
            self.current_user = user
            if user.is_admin:
                self.frames[AdminPortal].refresh()
                self.show_frame(AdminPortal)
            else:
                self.frames[UserPortal].refresh()
                self.show_frame(UserPortal)
        else:
            print("Password check failed or user not found.")
            messagebox.showerror("Login Failed", "Incorrect username/SRN or password.")

    def signup(self, srn, name, email, enrollment_year, department, password):
        if not validate_srn(srn):
            messagebox.showerror("Invalid SRN", "Please enter a valid SRN.")
            return
        if not validate_password(password):
            messagebox.showerror("Invalid Password", "Password must be at least 8 characters long and include uppercase, lowercase, digit, and special character.")
            return
        if User.get_user_by_srn(srn) or User.get_user_by_email(email):
            messagebox.showerror("User Exists", "User with this SRN or Email already exists.")
            return
        success = User.create_user(srn, name, email, enrollment_year, department, password)
        if success:
            messagebox.showinfo("Success", "Sign up successful! Logging you in...")
            self.login(srn, password)
        else:
            messagebox.showerror("Error", "Failed to create user. Please try again.")

class LoginPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        ttk.Label(self, text="Login", font=("Helvetica", 20)).pack(pady=20)

        self.srn_email_var = tk.StringVar()
        self.password_var = tk.StringVar()

        ttk.Label(self, text="Username/SRN:").pack(pady=5)
        self.srn_email_entry = ttk.Entry(self, textvariable=self.srn_email_var)
        self.srn_email_entry.pack()

        ttk.Label(self, text="Password:").pack(pady=5)
        self.password_entry = ttk.Entry(self, textvariable=self.password_var, show="*")
        self.password_entry.pack()

        ttk.Button(self, text="Login", command=self.login).pack(pady=10)

        signup_label = ttk.Label(self, text="Don't have an account? Sign Up", foreground="blue", cursor="hand2")
        signup_label.pack()
        signup_label.bind("<Button-1>", lambda e: controller.show_frame(SignUpPage))

    def login(self):
        srn_email = self.srn_email_var.get().strip()
        password = self.password_var.get()
        self.controller.login(srn_email, password)

class SignUpPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        ttk.Label(self, text="Sign Up", font=("Helvetica", 20)).pack(pady=20)

        self.srn_var = tk.StringVar()
        self.name_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.enrollment_year_var = tk.StringVar()
        self.department_var = tk.StringVar()
        self.password_var = tk.StringVar()

        form_frame = ttk.Frame(self)
        form_frame.pack(pady=10)

        ttk.Label(form_frame, text="SRN:").grid(row=0, column=0, sticky="e", pady=2)
        ttk.Entry(form_frame, textvariable=self.srn_var).grid(row=0, column=1, pady=2)

        ttk.Label(form_frame, text="Name:").grid(row=1, column=0, sticky="e", pady=2)
        ttk.Entry(form_frame, textvariable=self.name_var).grid(row=1, column=1, pady=2)

        ttk.Label(form_frame, text="Email:").grid(row=2, column=0, sticky="e", pady=2)
        ttk.Entry(form_frame, textvariable=self.email_var).grid(row=2, column=1, pady=2)

        ttk.Label(form_frame, text="Enrollment Year:").grid(row=3, column=0, sticky="e", pady=2)
        ttk.Entry(form_frame, textvariable=self.enrollment_year_var).grid(row=3, column=1, pady=2)

        ttk.Label(form_frame, text="Department:").grid(row=4, column=0, sticky="e", pady=2)
        ttk.Entry(form_frame, textvariable=self.department_var).grid(row=4, column=1, pady=2)

        ttk.Label(form_frame, text="Password:").grid(row=5, column=0, sticky="e", pady=2)
        ttk.Entry(form_frame, textvariable=self.password_var, show="*").grid(row=5, column=1, pady=2)

        ttk.Button(self, text="Sign Up", command=self.signup).pack(pady=10)

        login_label = ttk.Label(self, text="Already have an account? Login", foreground="blue", cursor="hand2")
        login_label.pack()
        login_label.bind("<Button-1>", lambda e: controller.show_frame(LoginPage))

    def signup(self):
        srn = self.srn_var.get().strip()
        name = self.name_var.get().strip()
        email = self.email_var.get().strip()
        enrollment_year = self.enrollment_year_var.get().strip()
        department = self.department_var.get().strip()
        password = self.password_var.get()

        if not enrollment_year.isdigit():
            messagebox.showerror("Invalid Input", "Enrollment year must be a number.")
            return

        self.controller.signup(srn, name, email, int(enrollment_year), department, password)

class AdminPortal(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.course_picture_path = None

        ttk.Label(self, text="Admin Portal", font=("Helvetica", 20)).pack(pady=10)

        tab_control = ttk.Notebook(self)
        tab_control.pack(expand=1, fill="both")

        # Add Course Tab
        self.add_course_tab = ttk.Frame(tab_control)
        tab_control.add(self.add_course_tab, text="Add Course")
        self._build_add_course_tab()

        # Add Instructor Tab
        self.add_instructor_tab = ttk.Frame(tab_control)
        tab_control.add(self.add_instructor_tab, text="Add Instructor")
        self._build_add_instructor_tab()

        # View Registered Students Tab
        self.view_registered_tab = ttk.Frame(tab_control)
        tab_control.add(self.view_registered_tab, text="View Registered Students")
        self._build_view_registered_tab()

        # List All Students Tab
        self.list_students_tab = ttk.Frame(tab_control)
        tab_control.add(self.list_students_tab, text="List All Students")
        self._build_list_students_tab()

        # Logout Tab
        # Removed logout tab as per user request

        # Bind tab change event to refresh courses dropdown dynamically
        tab_control.bind("<<NotebookTabChanged>>", self._on_tab_changed)

    def _on_tab_changed(self, event):
        selected_tab = event.widget.select()
        tab_text = event.widget.tab(selected_tab, "text")
        if tab_text == "Add Instructor":
            self._refresh_courses_dropdown()
        elif tab_text == "Logout":
            # When logout tab is selected, immediately logout and return to login page
            self.controller.current_user = None
            self.controller.show_frame(LoginPage)

    def refresh(self):
        self._refresh_courses_dropdown()
        self._refresh_students_list()

    def _build_add_course_tab(self):
        frame = self.add_course_tab
        labels = ["Course Name", "Course ID", "Course Code", "Credits", "Department Offering", "Picture"]
        self.course_vars = {label: tk.StringVar() for label in labels}

        form_frame = ttk.Frame(frame)
        form_frame.pack(pady=10, padx=10, anchor="w")

        for i, label in enumerate(labels[:-1]):
            ttk.Label(form_frame, text=label + ":").grid(row=i, column=0, sticky="e", pady=2)
            ttk.Entry(form_frame, textvariable=self.course_vars[label]).grid(row=i, column=1, pady=2)

        # Picture upload button
        ttk.Label(form_frame, text="Picture:").grid(row=5, column=0, sticky="e", pady=2)
        pic_frame = ttk.Frame(form_frame)
        pic_frame.grid(row=5, column=1, pady=2, sticky="w")
        self.pic_label = ttk.Label(pic_frame, text="No file selected")
        self.pic_label.pack(side="left")
        ttk.Button(pic_frame, text="Browse", command=self._browse_picture).pack(side="left", padx=5)

        ttk.Button(frame, text="Add Course", command=self._add_course).pack(pady=10)

        self.course_cards_frame = ttk.Frame(frame)
        self.course_cards_frame.pack(fill="both", expand=True, padx=10, pady=10)

    def _browse_picture(self):
        file_path = filedialog.askopenfilename(
            title="Select Course Picture",
            filetypes=[("Image Files", "*.png *.jpg *.jpeg *.gif"), ("All Files", "*.*")]
        )
        if file_path:
            self.course_picture_path = file_path
            self.pic_label.config(text=os.path.basename(file_path))

    def _add_course(self):
        course_name = self.course_vars["Course Name"].get().strip()
        course_id = self.course_vars["Course ID"].get().strip()
        course_code = self.course_vars["Course Code"].get().strip()
        credits = self.course_vars["Credits"].get().strip()
        department = self.course_vars["Department Offering"].get().strip()
        picture = self.course_picture_path

        if not course_name or not course_id or not course_code or not credits or not department:
            messagebox.showerror("Input Error", "Please fill in all required fields.")
            return
        if not credits.isdigit():
            messagebox.showerror("Input Error", "Credits must be a number.")
            return

        success, msg = Course.add_course(course_id, course_name, course_code, int(credits), department, picture)
        if success:
            messagebox.showinfo("Success", msg)
            self._display_course_card(course_id)
            # Clear form
            for var in self.course_vars.values():
                var.set("")
            self.pic_label.config(text="No file selected")
            self.course_picture_path = None
            self._refresh_courses_dropdown()
        else:
            messagebox.showerror("Error", msg)

    def _display_course_card(self, course_id):
        # Clear previous cards
        for widget in self.course_cards_frame.winfo_children():
            widget.destroy()

        courses = Course.get_all_courses()
        for course in courses:
            card = ttk.Frame(self.course_cards_frame, relief="raised", borderwidth=2, padding=10)
            card.pack(pady=5, fill="x")

            ttk.Label(card, text=f"Course Name: {course.course_name}", font=("Helvetica", 14, "bold")).pack(anchor="w")
            ttk.Label(card, text=f"Course Code: {course.course_code}").pack(anchor="w")
            ttk.Label(card, text=f"Credits: {course.credits}").pack(anchor="w")
            ttk.Label(card, text=f"Department: {course.department_offering}").pack(anchor="w")

    def _build_add_instructor_tab(self):
        frame = self.add_instructor_tab
        labels = ["Instructor ID", "Name", "Email", "Department"]
        self.instructor_vars = {label: tk.StringVar() for label in labels}

        form_frame = ttk.Frame(frame)
        form_frame.pack(pady=10, padx=10, anchor="w")

        for i, label in enumerate(labels):
            ttk.Label(form_frame, text=label + ":").grid(row=i, column=0, sticky="e", pady=2)
            ttk.Entry(form_frame, textvariable=self.instructor_vars[label]).grid(row=i, column=1, pady=2)

        ttk.Label(form_frame, text="Assign to Course:").grid(row=len(labels), column=0, sticky="e", pady=2)
        self.course_assign_var = tk.StringVar()
        self.course_assign_dropdown = ttk.Combobox(form_frame, textvariable=self.course_assign_var, state="readonly")
        self.course_assign_dropdown.grid(row=len(labels), column=1, pady=2)

        ttk.Button(frame, text="Add Instructor", command=self._add_instructor).pack(pady=10)

        # Listbox to show instructors and their assigned courses
        ttk.Label(frame, text="Instructors and Assigned Courses:", font=("Helvetica", 12)).pack(pady=5)
        self.instructor_listbox = tk.Listbox(frame, width=100, height=10)
        self.instructor_listbox.pack(pady=5)

        self._refresh_instructor_list()

    def _refresh_courses_dropdown(self):
        courses = Course.get_all_courses()
        course_ids = [course.course_id for course in courses]
        self.course_assign_dropdown['values'] = course_ids

    def _refresh_instructor_list(self):
        self.instructor_listbox.delete(0, tk.END)
        instructors = Instructor.get_all_instructors_with_courses()
        for inst in instructors:
            assigned_course = inst['course_id'] if inst['course_id'] else 'None'
            line = f"ID: {inst['instructor_id']}, Name: {inst['name']}, Email: {inst['email']}, Department: {inst['department']}, Assigned Course: {assigned_course}"
            self.instructor_listbox.insert(tk.END, line)

    def _add_instructor(self):
        instructor_id = self.instructor_vars["Instructor ID"].get().strip()
        name = self.instructor_vars["Name"].get().strip()
        email = self.instructor_vars["Email"].get().strip()
        department = self.instructor_vars["Department"].get().strip()
        course_id = self.course_assign_var.get()

        if not instructor_id or not name or not email or not department or not course_id:
            messagebox.showerror("Input Error", "Please fill in all fields and select a course.")
            return

        success, msg = Instructor.add_instructor(instructor_id, name, email, department)
        if success:
            assigned, assign_msg = Instructor.assign_instructor_to_course(instructor_id, course_id)
            if assigned:
                messagebox.showinfo("Success", f"Instructor '{name}' added and assigned to course '{course_id}'.")
                # Clear form
                for var in self.instructor_vars.values():
                    var.set("")
                self.course_assign_var.set("")
                self._refresh_instructor_list()
            else:
                messagebox.showerror("Error", assign_msg)
        else:
            messagebox.showerror("Error", msg)

    def _build_view_registered_tab(self):
        frame = self.view_registered_tab

        ttk.Label(frame, text="Select Course:").pack(pady=5)
        self.course_select_var = tk.StringVar()
        self.course_select_dropdown = ttk.Combobox(frame, textvariable=self.course_select_var, state="readonly")
        self.course_select_dropdown.pack(pady=5)
        self.course_select_dropdown.bind("<<ComboboxSelected>>", self._display_registered_students)

        # Populate the dropdown with course IDs on tab build
        courses = Course.get_all_courses()
        course_ids = [course.course_id for course in courses]
        self.course_select_dropdown['values'] = course_ids

        self.students_listbox = tk.Listbox(frame, width=100, height=15)
        self.students_listbox.pack(pady=10)

        ttk.Button(frame, text="Export to CSV", command=self._export_students_csv).pack(pady=5)

    def _display_registered_students(self, event=None):
        course_id = self.course_select_var.get()
        if not course_id:
            return
        students = Registration.get_students_by_course(course_id)
        self.students_listbox.delete(0, tk.END)
        for student in students:
            line = f"SRN: {student['srn']}, Name: {student['name']}, Email: {student['email']}, Enrollment Year: {student['enrollment_year']}, Department: {student['department']}"
            self.students_listbox.insert(tk.END, line)

    def _export_students_csv(self):
        course_id = self.course_select_var.get()
        if not course_id:
            messagebox.showerror("Error", "Please select a course first.")
            return
        students = Registration.get_students_by_course(course_id)
        if not students:
            messagebox.showinfo("No Data", "No students registered for this course.")
            return
        file_path = filedialog.asksaveasfilename(defaultextension=".csv",
                                                 filetypes=[("CSV files", "*.csv")])
        if file_path:
            with open(file_path, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(["SRN", "Name", "Email", "Enrollment Year", "Department"])
                for student in students:
                    writer.writerow([student['srn'], student['name'], student['email'], student['enrollment_year'], student['department']])
            messagebox.showinfo("Exported", f"Student list exported to {file_path}")

    def _build_list_students_tab(self):
        frame = self.list_students_tab
        ttk.Label(frame, text="All Students", font=("Helvetica", 16)).pack(pady=10)
        self.all_students_listbox = tk.Listbox(frame, width=100, height=20)
        self.all_students_listbox.pack(pady=10)

    def _refresh_students_list(self):
        students = Registration.get_all_students()
        self.all_students_listbox.delete(0, tk.END)
        for student in students:
            line = f"SRN: {student['srn']}, Name: {student['name']}, Email: {student['email']}, Enrollment Year: {student['enrollment_year']}, Department: {student['department']}"
            self.all_students_listbox.insert(tk.END, line)

class UserPortal(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        ttk.Label(self, text="User Portal", font=("Helvetica", 20)).pack(pady=10)

        tab_control = ttk.Notebook(self)
        tab_control.pack(expand=1, fill="both")

        self.courses_tab = ttk.Frame(tab_control)
        tab_control.add(self.courses_tab, text="Courses")
        self._build_courses_tab()

        self.logout_tab = ttk.Frame(tab_control)
        tab_control.add(self.logout_tab, text="Logout")
        self._build_logout_tab()

    def _build_logout_tab(self):
        # Removed logout tab build method as per user request
        pass

    def _logout(self):
        # Removed logout method as per user request
        pass

    def _build_courses_tab(self):
        frame = self.courses_tab

        # Add a canvas and scrollbar for scrolling
        canvas = tk.Canvas(frame)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        self.courses_frame = ttk.Frame(canvas)

        self.courses_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.courses_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def refresh(self):
        for widget in self.courses_frame.winfo_children():
            widget.destroy()
        courses = Course.get_all_courses()
        for course in courses:
            card = ttk.Frame(self.courses_frame, relief="raised", borderwidth=2, padding=10)
            card.pack(pady=5, fill="x")

            card.bind("<Enter>", lambda e, c=card: c.configure(style="Card.TFrame"))
            card.bind("<Leave>", lambda e, c=card: c.configure(style="TFrame"))

            ttk.Label(card, text=f"Course Name: {course.course_name}", font=("Helvetica", 14, "bold")).pack(anchor="w")
            ttk.Label(card, text=f"Course Code: {course.course_code}").pack(anchor="w")
            ttk.Label(card, text=f"Credits: {course.credits}").pack(anchor="w")
            ttk.Label(card, text=f"Department: {course.department_offering}").pack(anchor="w")

            instructors = Instructor.get_instructors_by_course(course.course_id)
            instructor_names = ", ".join([inst.name for inst in instructors]) if instructors else "N/A"
            ttk.Label(card, text=f"Instructor(s): {instructor_names}").pack(anchor="w")

            register_button = ttk.Button(card, text="Register", command=lambda c=course: self._register_course(c))
            register_button.pack(anchor="e", pady=5)

    def _register_course(self, course):
        user = self.controller.current_user
        if not user:
            messagebox.showerror("Error", "User not logged in.")
            return
        success, msg = Registration.register_student(user.srn, course.course_id)
        if success:
            messagebox.showinfo("Success", msg)
            # Refresh the View Registered Students tab if visible
            admin_portal = self.controller.frames.get(AdminPortal)
            if admin_portal:
                admin_portal._display_registered_students()
        else:
            messagebox.showerror("Error", msg)

if __name__ == "__main__":
    app = CourseRegistrationApp()

    # Style for hover effect on course cards
    style = ttk.Style()
    style.configure("Card.TFrame", relief="raised", borderwidth=4)

    app.mainloop()
