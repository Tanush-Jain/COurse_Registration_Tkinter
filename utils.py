import re
import bcrypt

def hash_password(password: str) -> str:
    """
    Hash a password for storing.
    """
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed.decode('utf-8')

def check_password(password: str, hashed: str) -> bool:
    """
    Check a password against an existing hash.
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def validate_srn(srn: str) -> bool:
    """
    Validate SRN format.
    Relaxed to accept any non-empty string up to 100 characters.
    """
    if not srn:
        return False
    if len(srn) > 100:
        return False
    return True

def validate_password(password: str) -> bool:
    """
    Validate password complexity:
    - At least 8 characters
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one digit
    - At least one special character
    """
    if len(password) < 8:
        return False
    if not re.search(r'[A-Z]', password):
        return False
    if not re.search(r'[a-z]', password):
        return False
    if not re.search(r'[0-9]', password):
        return False
    if not re.search(r'[\W_]', password):
        return False
    return True
