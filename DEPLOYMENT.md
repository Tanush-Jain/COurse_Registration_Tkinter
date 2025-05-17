# Deployment and Packaging Instructions

This document provides instructions to package and deploy the Course Registration System for Windows users.

## Using PyInstaller to Create a Standalone Executable

PyInstaller can bundle the Python application and all dependencies into a single executable file that can be run on Windows without requiring Python installation.

### Prerequisites

- Python 3.7 or higher installed on your development machine
- The project dependencies installed (`pip install -r requirements.txt`)
- PyInstaller installed (`pip install pyinstaller`)

### Steps to Create Executable

1. Open Command Prompt or PowerShell in the project directory.

2. Run PyInstaller with the following command:

   ```
   pyinstaller --onefile --windowed gui.py
   ```

   - `--onefile` creates a single executable file.
   - `--windowed` prevents opening a console window when running the GUI app.

3. After the build completes, the executable will be located in the `dist` folder as `gui.exe`.

4. You can share the `gui.exe` file with your friend. Make sure to also share the `setup_db.py` script and instructions to set up the MariaDB database.

### Notes

- The user must have MariaDB or MySQL server installed and running on their machine.
- The database connection settings in `database.py` may need to be updated to match the target machine's configuration.
- The super admin user can be created by running `python setup_db.py` on the target machine.

## Using MySQL Instead of MariaDB

- MariaDB is a fork of MySQL and is highly compatible.
- The `mysql-connector-python` library works with both MariaDB and MySQL.
- You can use MySQL server on Windows instead of MariaDB without changing the code.
- Just ensure the database connection parameters in `database.py` are updated accordingly (host, port, user, password).

## Additional Tips

- Test the executable on a clean Windows machine to verify all dependencies are bundled correctly.
- If you encounter missing DLL or library errors, you may need to include additional files or adjust PyInstaller options.
- For advanced packaging, consider creating an installer using tools like Inno Setup.

---

Feel free to reach out if you need help with any specific packaging or deployment issues.
