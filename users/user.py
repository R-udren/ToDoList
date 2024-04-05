import re
import hashlib
import secrets
import binascii



class User:
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    @staticmethod
    def validate_username(username, db):
        if not username:
            raise ValueError("Username cannot be empty")
        if db.username_exists(username):
            raise ValueError("Username already exists")
        return username

    @staticmethod
    def validate_email(email, db):
        email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if not re.fullmatch(email_regex, email):
            raise ValueError("Invalid email address")
        if db.email_exists(email):
            raise ValueError("Email already exists")
        return email

    @staticmethod
    def validate_password(password):
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not re.match(r"^[A-Za-z0-9@#$%^&+=]*$", password):
            raise ValueError("Password can only contain letters, numbers, and @#$%^&+=")
        return password

    @staticmethod
    def hash_password(password):
        """Hash a password for storing."""
        salt = secrets.token_hex(16)
        pwdhash = hashlib.pbkdf2_hmac('sha256', User.validate_password(password).encode('utf-8'),
                                    salt.encode('ascii'), 100000)
        pwdhash = binascii.hexlify(pwdhash).decode('ascii')
        return (salt + pwdhash)

    @staticmethod
    def verify_password(db_password, provided_password):
        """Verify a stored password against one provided by user"""
        salt = db_password[:32]
        stored_password = db_password[32:]
        pwdhash = hashlib.pbkdf2_hmac('sha256',
                                      provided_password.encode('utf-8'),
                                      salt.encode('ascii'),
                                      100000)
        pwdhash = binascii.hexlify(pwdhash).decode('ascii')
        return pwdhash == stored_password