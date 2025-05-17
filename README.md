<<<<<<< HEAD
# COurse_Registration_Tkinter
I built a Course_Registration platform in python using libraries ->Tkinter and for database as mariaDB. 
=======
# Course Registration System

This is a Python-based Course Registration System with a Tkinter GUI and MariaDB backend. It supports user login/signup, admin and user portals, course and instructor management, and course registration.

## Features

- Login and Signup with password hashing and validation
- Admin Portal:
  - Add Courses with details and picture upload
  - Add Instructors and assign them to courses
  - View registered students per course and export to CSV
  - List all students
- User Portal:
  - View available courses with instructor info
  - Register for courses with confirmation messages
- Secure password storage using bcrypt
- SQL injection prevention with parameterized queries
- Dynamic UI updates and scrolling support

## Setup Instructions (Windows)

### Prerequisites

- Python 3.7 or higher installed
- MariaDB Server installed and running locally
- Git (optional, for cloning the repo)

### Install MariaDB

Download and install MariaDB from [https://mariadb.org/download/](https://mariadb.org/download/).

Make sure the MariaDB server is running and you have the root password.

### Clone the Repository

```bash
git clone <repository-url>
cd <repository-folder>
```

Or download the source code as a ZIP and extract it.

### Create a Virtual Environment and Install Dependencies

Open Command Prompt or PowerShell in the project directory and run:

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Configure Database Connection

Edit `database.py` and update the `DB_CONFIG` dictionary with your MariaDB root password and socket if needed.

Example:

```python
DB_CONFIG = {
    'user': 'root',
    'password': 'your_mariadb_root_password',
    'host': '127.0.0.1',
    'database': 'course_registration',
    'raise_on_warnings': True
}
```

### Initialize the Database and Super Admin User

Run the setup script to create the database schema and super admin user:

```bash
python setup_db.py
```

The super admin credentials are:

- SRN: `SUPERADMIN`
- Password: `SuperAdminPassword123!`

### Run the Application

Start the GUI application:

```bash
python gui.py
```

### Usage

- Login as super admin or create new users via Sign Up.
- Admin users can add courses, instructors, and view registrations.
- Students can view courses and register.

## Notes

- Passwords are securely hashed using bcrypt.
- All database queries use parameterized statements to prevent SQL injection.
- The GUI uses Tkinter with scrollable course lists and dynamic updates.
- **MySQL Compatibility:** This project uses `mysql-connector-python` which supports both MariaDB and MySQL. You can use MySQL server on Windows instead of MariaDB without code changes. Just update the connection settings accordingly in `database.py`.

## Troubleshooting

- Ensure MariaDB server is running before starting the app.
- Verify database connection settings in `database.py`.
- If you encounter issues with socket connection on Windows, try changing `unix_socket` to `host` and `port`.

## License

This project is provided as-is for educational purposes.

---

Feel free to share this project with your friends and modify it as needed.
>>>>>>> 8b65aae (Initial comit of the course registration system)
