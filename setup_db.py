import mysql.connector
from mysql.connector import errorcode
import bcrypt
import sys
from models import User
from database import get_connection

# Database configuration
DB_CONFIG = {
    'user': 'root',
    'password': '2004',  # Updated to correct password
    'unix_socket': '/var/run/mysqld/mysqld.sock',  # Use socket for localhost connection
    'raise_on_warnings': True
}

def create_database(cursor):
    try:
        cursor.execute("CREATE DATABASE IF NOT EXISTS course_registration DEFAULT CHARACTER SET 'utf8'")
    except mysql.connector.Error as err:
        print(f"Failed creating database: {err}")
        exit(1)

def create_tables(cursor):
    TABLES = {}
    TABLES['users'] = (
        "CREATE TABLE IF NOT EXISTS users ("
        "  srn VARCHAR(20) NOT NULL PRIMARY KEY,"
        "  name VARCHAR(100) NOT NULL,"
        "  email VARCHAR(100) NOT NULL UNIQUE,"
        "  enrollment_year INT NOT NULL,"
        "  department VARCHAR(100) NOT NULL,"
        "  password_hash VARCHAR(100) NOT NULL,"
        "  is_admin BOOLEAN NOT NULL DEFAULT FALSE"
        ") ENGINE=InnoDB"
    )
    TABLES['courses'] = (
        "CREATE TABLE IF NOT EXISTS courses ("
        "  course_id VARCHAR(20) NOT NULL PRIMARY KEY,"
        "  course_name VARCHAR(100) NOT NULL,"
        "  course_code VARCHAR(20) NOT NULL UNIQUE,"
        "  credits INT NOT NULL,"
        "  department VARCHAR(100) NOT NULL,"
        "  picture VARCHAR(255)"
        ") ENGINE=InnoDB"
    )
    TABLES['instructors'] = (
        "CREATE TABLE IF NOT EXISTS instructors ("
        "  instructor_id VARCHAR(20) NOT NULL PRIMARY KEY,"
        "  name VARCHAR(100) NOT NULL,"
        "  email VARCHAR(100) NOT NULL UNIQUE,"
        "  department VARCHAR(100) NOT NULL"
        ") ENGINE=InnoDB"
    )
    TABLES['course_instructor'] = (
        "CREATE TABLE IF NOT EXISTS course_instructor ("
        "  course_id VARCHAR(20) NOT NULL,"
        "  instructor_id VARCHAR(20) NOT NULL,"
        "  PRIMARY KEY (course_id, instructor_id),"
        "  FOREIGN KEY (course_id) REFERENCES courses(course_id) ON DELETE CASCADE,"
        "  FOREIGN KEY (instructor_id) REFERENCES instructors(instructor_id) ON DELETE CASCADE"
        ") ENGINE=InnoDB"
    )
    TABLES['registrations'] = (
        "CREATE TABLE IF NOT EXISTS registrations ("
        "  srn VARCHAR(20) NOT NULL,"
        "  course_id VARCHAR(20) NOT NULL,"
        "  registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,"
        "  PRIMARY KEY (srn, course_id),"
        "  FOREIGN KEY (srn) REFERENCES users(srn) ON DELETE CASCADE,"
        "  FOREIGN KEY (course_id) REFERENCES courses(course_id) ON DELETE CASCADE"
        ") ENGINE=InnoDB"
    )

    for table_name in TABLES:
        table_description = TABLES[table_name]
        try:
            print(f"Creating table {table_name}... ", end='')
            cursor.execute(table_description)
            print("OK")
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
            else:
                print(err.msg)

def create_super_admin(cursor):
    # Check if super admin exists
    cursor.execute("SELECT * FROM users WHERE srn = %s", ('SHR',))
    if cursor.fetchone():
        print("Super admin user already exists.")
        return

    password = "Shrey123!@#"  # Changed to user requested password
    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    add_user = ("INSERT INTO users "
                "(srn, name, email, enrollment_year, department, password_hash, is_admin) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s)")
    user_data = ('SHR', 'Super Admin', 'superadmin@example.com', 2024, 'Administration', password_hash.decode('utf-8'), True)

    cursor.execute(add_user, user_data)
    print("Super admin user created with SRN 'SHR' and password 'Shrey123!@#'")

def reset_admin_password(new_password):
    cnx = get_connection()
    if cnx is None:
        print("Failed to connect to database.")
        return
    cursor = cnx.cursor()
    cursor.execute("SELECT * FROM users WHERE srn = %s", ('SUPERADMIN',))
    if cursor.fetchone():
        # Update password
        success = User.update_password('SUPERADMIN', new_password)
        if success:
            print(f"Admin password updated to: {new_password}")
        else:
            print("Failed to update admin password.")
    else:
        # Create admin user
        password_hash = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
        add_user = ("INSERT INTO users "
                    "(srn, name, email, enrollment_year, department, password_hash, is_admin) "
                    "VALUES (%s, %s, %s, %s, %s, %s, %s)")
        user_data = ('SUPERADMIN', 'Super Admin', 'superadmin@example.com', 2024, 'Administration', password_hash.decode('utf-8'), True)
        cursor.execute(add_user, user_data)
        cnx.commit()
        print(f"Admin user created with password: {new_password}")
    cursor.close()
    cnx.close()

def main():
    import mysql.connector
    from mysql.connector import errorcode

    try:
        cnx = mysql.connector.connect(
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            unix_socket=DB_CONFIG['unix_socket']
        )
        cursor = cnx.cursor()
        create_database(cursor)
        cnx.database = 'course_registration'
        create_tables(cursor)
        create_super_admin(cursor)
        cnx.commit()
        cursor.close()
        cnx.close()
        print("Database setup completed successfully.")
    except mysql.connector.Error as err:
        print(err)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--reset-admin-password":
        if len(sys.argv) < 3:
            print("Usage: python setup_db.py --reset-admin-password <new_password>")
        else:
            new_password = sys.argv[2]
            reset_admin_password(new_password)
    else:
        main()

def main():
    try:
        cnx = mysql.connector.connect(
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            unix_socket=DB_CONFIG['unix_socket']
        )
        cursor = cnx.cursor()
        create_database(cursor)
        cnx.database = 'course_registration'
        create_tables(cursor)
        create_super_admin(cursor)
        cnx.commit()
        cursor.close()
        cnx.close()
        print("Database setup completed successfully.")
    except mysql.connector.Error as err:
        print(err)

if __name__ == "__main__":
    main()
