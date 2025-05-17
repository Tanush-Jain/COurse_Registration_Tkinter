from database import create_database_and_tables
from setup_db import main as setup_super_admin

def initialize():
    print("Creating database and tables...")
    create_database_and_tables()
    print("Creating super admin user...")
    setup_super_admin()
    print("Initialization complete.")

if __name__ == "__main__":
    initialize()
