import mysql.connector
from mysql.connector import errorcode

# Database configuration
DB_CONFIG = {
    'user': 'root',
    'password': '2004',  # Updated to the correct MariaDB root password
    'unix_socket': '/var/run/mysqld/mysqld.sock',  # Use socket for localhost connection
    'raise_on_warnings': True
}

def create_database_and_tables():
    try:
        cnx = mysql.connector.connect(
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            unix_socket=DB_CONFIG['unix_socket']
        )
        cursor = cnx.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS course_registration DEFAULT CHARACTER SET 'utf8'")
        cursor.execute("USE course_registration")

        # Create tables if not exist
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            srn VARCHAR(20) NOT NULL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) NOT NULL UNIQUE,
            enrollment_year INT NOT NULL,
            department VARCHAR(100) NOT NULL,
            password_hash VARCHAR(100) NOT NULL,
            is_admin BOOLEAN NOT NULL DEFAULT FALSE
        ) ENGINE=InnoDB
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS courses (
            course_id VARCHAR(20) NOT NULL PRIMARY KEY,
            course_name VARCHAR(100) NOT NULL,
            course_code VARCHAR(20) NOT NULL UNIQUE,
            credits INT NOT NULL,
            department_offering VARCHAR(100) NOT NULL,
            picture VARCHAR(255)
        ) ENGINE=InnoDB
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS instructors (
            instructor_id VARCHAR(20) NOT NULL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) NOT NULL UNIQUE,
            department VARCHAR(100) NOT NULL
        ) ENGINE=InnoDB
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS course_instructor (
            course_id VARCHAR(20) NOT NULL,
            instructor_id VARCHAR(20) NOT NULL,
            PRIMARY KEY (course_id, instructor_id),
            FOREIGN KEY (course_id) REFERENCES courses(course_id) ON DELETE CASCADE,
            FOREIGN KEY (instructor_id) REFERENCES instructors(instructor_id) ON DELETE CASCADE
        ) ENGINE=InnoDB
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS registrations (
            srn VARCHAR(20) NOT NULL,
            course_id VARCHAR(20) NOT NULL,
            registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (srn, course_id),
            FOREIGN KEY (srn) REFERENCES users(srn) ON DELETE CASCADE,
            FOREIGN KEY (course_id) REFERENCES courses(course_id) ON DELETE CASCADE
        ) ENGINE=InnoDB
        """)
        cnx.commit()
        cursor.close()
        cnx.close()
        print("Database and tables ensured.")
    except mysql.connector.Error as err:
        print(f"Error creating database or tables: {err}")

def get_connection():
    try:
        cnx = mysql.connector.connect(
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            unix_socket=DB_CONFIG['unix_socket'],
            database='course_registration'
        )
        return cnx
    except mysql.connector.Error as err:
        print(f"Error getting connection: {err}")
        return None

def execute_query(query, params=None, fetchone=False, fetchall=False, commit=False):
    """
    Execute a parameterized query safely.
    :param query: SQL query string with placeholders
    :param params: tuple or list of parameters
    :param fetchone: if True, fetch one result
    :param fetchall: if True, fetch all results
    :param commit: if True, commit the transaction
    :return: fetched data or None
    """
    cnx = get_connection()
    if cnx is None:
        return None
    cursor = cnx.cursor(dictionary=True)
    try:
        cursor.execute(query, params)
        if commit:
            cnx.commit()
        if fetchone:
            result = cursor.fetchone()
        elif fetchall:
            result = cursor.fetchall()
        else:
            result = None
        cursor.close()
        cnx.close()
        return result
    except mysql.connector.Error as err:
        print(f"Database query error: {err}")
        cursor.close()
        cnx.close()
        return None
