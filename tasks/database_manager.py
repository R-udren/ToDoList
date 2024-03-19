import sqlite3

import re
import uuid

import hashlib
import os
import binascii

class DatabaseManager:
    def __init__(self, db_name: str):
        self.db_name = db_name
        self.db = sqlite3.connect(db_name)
        self.cursor = self.db.cursor()

    def create_task_table(self, table_name: str, columns: list):
        columns.insert(0, 'user_id TEXT')
        columns.append('FOREIGN KEY(user_id) REFERENCES users(id)')
        columns = ', '.join(columns)
        self.cursor.execute(f'CREATE TABLE IF NOT EXISTS {table_name} ({columns})')
        self.db.commit()

    def add_record(self, table_name: str, values: list):
        placeholders = ', '.join(['?' for _ in values])
        self.cursor.execute(f'INSERT INTO {table_name} VALUES ({placeholders})', values)
        self.db.commit()
        

    def get_record(self, table_name: str, column_name: str, value: str):
        self.cursor.execute(f'SELECT * FROM {table_name} WHERE {column_name} = ?', (value,))
        return self.cursor.fetchall()

    def read_records(self, table_name: str, user_id : str):
        self.cursor.execute(f'SELECT * FROM {table_name} WHERE user_id = ?', (user_id,))
        return self.cursor.fetchall()

    def clear_table(self, table_name: str, user_id : str):
        self.cursor.execute(f'DELETE FROM {table_name} WHERE user_id = ?', (user_id,))
        self.db.commit()

    ## TODO: Add create_user_table function

    def close(self):
        self.db.close()

class User:
    def __init__(self, username, email, password):
        self.user_id = self.generate_user_id()
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
        ## TODO: Add username_exists function to database
        if db.username_exists(username):
            raise ValueError("Username already exists")
        return username

    @staticmethod
    def validate_email(email, db):
        email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if not re.fullmatch(email_regex, email):
            raise ValueError("Invalid email address")
        ## TODO: Add email_exists function to database
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
    def verify_password(stored_password, provided_password):
        """Verify a stored password against one provided by user"""
        salt = stored_password[:64]
        stored_password = stored_password[64:]
        pwdhash = hashlib.pbkdf2_hmac('sha512', 
                                      provided_password.encode('utf-8'), 
                                      salt.encode('ascii'), 
                                      100000)
        pwdhash = binascii.hexlify(pwdhash).decode('ascii')
        return pwdhash == stored_password




class UserManager:
    def __init__(self, db):
        self.db = db

    def create_user(self, username, email, password):
        username = User.validate_username(username, self.db)
        email = User.validate_email(email, self.db)
        password = User.hash_password(password)
        user_id = User.generate_user_id()

        ## TODO: Add add_user function to database
        self.db.add_user(user_id, username, email, password)
        return User(user_id, username, email, password)