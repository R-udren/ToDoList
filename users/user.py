import re
import uuid

import hashlib
import os
import binascii

class User:
    def __init__(self, user_id, username, email, password):
        self.user_id = user_id
        self.username = self.validate_username(username)
        self.email = self.validate_email(email)
        self.password = self.validate_password(password)

    @staticmethod
    def generate_user_id():
        return str(uuid.uuid4())

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
        return password
    
    @staticmethod
    def hash_password(password):
        
        """Hash a password for storing."""
        salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
        pwdhash = hashlib.pbkdf2_hmac('sha512', User.validate_password(password).encode('utf-8'), 
                                    salt, 100000)
        pwdhash = binascii.hexlify(pwdhash)
        return (salt + pwdhash).decode('ascii')
    
    @staticmethod
    def verify_password(db_password, provided_password):
        """Verify a stored password against one provided by user"""
        salt = db_password[:64]
        stored_password = db_password[64:]
        pwdhash = hashlib.pbkdf2_hmac('sha512', 
                                      provided_password.encode('utf-8'), 
                                      salt.encode('ascii'), 
                                      100000)
        pwdhash = binascii.hexlify(pwdhash).decode('ascii')
        return pwdhash == stored_password