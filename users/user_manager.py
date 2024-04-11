from database.database_manager import DatabaseManager
from users.user import User
from config import DB_NAME

class UserManager:
    def __init__(self):
        self.db = DatabaseManager(DB_NAME)
        self.db.create_user_table("users", ["username TEXT", "email TEXT PRIMARY KEY", "password TEXT"])

    options = [
        "Exit",
        "Log in",
        "Create an account",
        "Delete an account"
    ]

    def login(self, email, password) -> str:
        """
        Log in a user
        :param email: str: email of the user
        :param password: str: password of the user
        :return: str: email of the user
        """
        user = self.db.get_record('users', 'email', email)
        if user:
            if User.verify_password(user[0][2], password):
                return user[0][1]
        raise ValueError("Invalid email or password!")

    def save_user(self, username, email, password) -> str:
        """
        Save a user to the database
        :param username: str: username of the user
        :param email: str: email of the user
        :param password: str: password of the user
        :return: str: email of the user
        """
        username = User.validate_username(username, self.db)
        email = User.validate_email(email, self.db)
        password = User.hash_password(User.validate_password(password))
        self.db.add_user('users', username, email, password)
        return email
    
    def delete_user(self, email):
        """
        Delete a user from the database
        :param email: str: email of the user
        """
        self.db.delete_user(email)
        return None

    @staticmethod
    def exit():
        raise KeyboardInterrupt