from database import execute_query
from utils import hash_password, check_password

class User:
    def __init__(self, srn, name, email, enrollment_year, department, password_hash, is_admin=False):
        self.srn = srn
        self.name = name
        self.email = email
        self.enrollment_year = enrollment_year
        self.department = department
        self.password_hash = password_hash
        self.is_admin = is_admin

    @staticmethod
    def get_user_by_srn(srn):
        query = "SELECT * FROM users WHERE srn = %s"
        result = execute_query(query, (srn,), fetchone=True)
        if result:
            return User(**result)
        return None

    @staticmethod
    def get_user_by_email(email):
        query = "SELECT * FROM users WHERE email = %s"
        result = execute_query(query, (email,), fetchone=True)
        if result:
            return User(**result)
        return None

    @staticmethod
    def create_user(srn, name, email, enrollment_year, department, password):
        password_hash = hash_password(password)
        query = ("INSERT INTO users "
                 "(srn, name, email, enrollment_year, department, password_hash, is_admin) "
                 "VALUES (%s, %s, %s, %s, %s, %s, %s)")
        params = (srn, name, email, enrollment_year, department, password_hash, False)
        result = execute_query(query, params, commit=True)
        return result is not None

    def check_password(self, password):
        return check_password(password, self.password_hash)

class Course:
    def __init__(self, course_id, course_name, course_code, credits, department_offering, picture=None):
        self.course_id = course_id
        self.course_name = course_name
        self.course_code = course_code
        self.credits = credits
        self.department_offering = department_offering
        self.picture = picture

    @staticmethod
    def add_course(course_id, course_name, course_code, credits, department_offering, picture=None):
        query = ("INSERT INTO courses "
                 "(course_id, course_name, course_code, credits, department_offering, picture) "
                 "VALUES (%s, %s, %s, %s, %s, %s)")
        params = (course_id, course_name, course_code, credits, department_offering, picture)
        try:
            result = execute_query(query, params, commit=True)
            return True, "Course added successfully."
        except Exception as e:
            if "Duplicate entry" in str(e):
                return False, "Duplicate Course ID or Code."
            else:
                return False, f"Error: {str(e)}"

    @staticmethod
    def get_all_courses():
        query = "SELECT * FROM courses"
        results = execute_query(query, fetchall=True)
        if results:
            return [Course(**row) for row in results]
        return []

    @staticmethod
    def get_course_by_id(course_id):
        query = "SELECT * FROM courses WHERE course_id = %s"
        result = execute_query(query, (course_id,), fetchone=True)
        if result:
            return Course(**result)
        return None

class Instructor:
    def __init__(self, instructor_id, name, email, department):
        self.instructor_id = instructor_id
        self.name = name
        self.email = email
        self.department = department

    @staticmethod
    def add_instructor(instructor_id, name, email, department):
        query = ("INSERT INTO instructors "
                 "(instructor_id, name, email, department) "
                 "VALUES (%s, %s, %s, %s)")
        params = (instructor_id, name, email, department)
        try:
            result = execute_query(query, params, commit=True)
            return True, "Instructor added successfully."
        except Exception as e:
            if "Duplicate entry" in str(e):
                return False, "Duplicate Instructor ID or Email."
            else:
                return False, f"Error: {str(e)}"

    @staticmethod
    def assign_instructor_to_course(instructor_id, course_id):
        query = ("INSERT INTO course_instructor (course_id, instructor_id) VALUES (%s, %s)")
        params = (course_id, instructor_id)
        try:
            result = execute_query(query, params, commit=True)
            return True, "Instructor assigned to course successfully."
        except Exception as e:
            if "Duplicate entry" in str(e):
                return False, "Instructor already assigned to this course."
            else:
                return False, f"Error: {str(e)}"

    @staticmethod
    def get_instructors_by_course(course_id):
        query = ("SELECT i.* FROM instructors i "
                 "JOIN course_instructor ci ON i.instructor_id = ci.instructor_id "
                 "WHERE ci.course_id = %s")
        results = execute_query(query, (course_id,), fetchall=True)
        if results:
            return [Instructor(**row) for row in results]
        return []

    @staticmethod
    def get_all_instructors_with_courses():
        query = (
            "SELECT i.instructor_id, i.name, i.email, i.department, ci.course_id "
            "FROM instructors i LEFT JOIN course_instructor ci ON i.instructor_id = ci.instructor_id"
        )
        results = execute_query(query, fetchall=True)
        if results:
            return results
        return []

class Registration:
    @staticmethod
    def register_student(srn, course_id):
        query = ("INSERT INTO registrations (srn, course_id) VALUES (%s, %s)")
        params = (srn, course_id)
        try:
            result = execute_query(query, params, commit=True)
            return True, "Successfully registered for the course."
        except Exception as e:
            if "Duplicate entry" in str(e):
                return False, "You have already registered for this course."
            else:
                return False, f"Error: {str(e)}"

    @staticmethod
    def get_students_by_course(course_id):
        query = ("SELECT u.srn, u.name, u.email, u.enrollment_year, u.department "
                 "FROM users u JOIN registrations r ON u.srn = r.srn "
                 "WHERE r.course_id = %s")
        results = execute_query(query, (course_id,), fetchall=True)
        if results:
            return results
        return []

    @staticmethod
    def get_all_students():
        query = "SELECT srn, name, email, enrollment_year, department FROM users WHERE is_admin = FALSE"
        results = execute_query(query, fetchall=True)
        if results:
            return results
        return []
