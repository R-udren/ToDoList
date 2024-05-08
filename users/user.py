import binascii
import hashlib
import re
import secrets


class User:
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    @staticmethod
    def validate_username(username, db):
        if not username or username.isspace():
            raise ValueError("Username cannot be empty")
        if db.username_exists(username):
            raise ValueError("Username already exists")
        return username

    @staticmethod
    def is_email_correct(email):
        email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if not re.fullmatch(email_regex, email):
            return False
        return True

    @staticmethod
    def is_password_correct(password):
        if len(password) < 8:
            return False
        if not re.match(r"^[A-Za-z0-9@#$%^&+=]*$", password):
            return False
        return True

    @staticmethod
    def validate_email(email, db):
        if not email:
            raise ValueError("Email cannot be empty")
        if not User.is_email_correct(email):
            raise ValueError("Email is not valid")
        if db.email_exists(email):
            raise ValueError("Email already exists")
        return email

    @staticmethod
    def validate_password(password):
        if password is None:
            raise ValueError("Password cannot be empty")
        if not User.is_password_correct(password):
            raise ValueError("Password is not valid")
        return password

    @staticmethod
    def hash_password(password):
        """Hash a password for storing."""
        salt = secrets.token_hex(16)
        pwdhash = hashlib.pbkdf2_hmac('sha256', User.validate_password(password).encode('utf-8'),
                                      salt.encode('ascii'), 100000)
        pwdhash = binascii.hexlify(pwdhash).decode('ascii')
        return salt + pwdhash

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
