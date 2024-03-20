from tasks.database_manager import DatabaseManager
from users.user import User
from config import DB_NAME

from rich.prompt import Prompt

class UserManager:
    def __init__(self):
        self.db = DatabaseManager(DB_NAME)
        self.db.create_user_table("users", ["user_id TEXT", "username TEXT", "email TEXT", "password TEXT"])

    options = [
        "Log in",
        "Create an account",
        "Exit"
    ]

    def login(self, email, password):
        user = self.db.get_record('users', 'email', email)
        if user:
            if User.verify_password(user[0][3], password):
                return user.user_id
        return None

    def save_user(self, username, email, password):
        username = User.validate_username(username, self.db)
        email = User.validate_email(email, self.db)
        password = User.hash_password(User.validate_password(password))
        user_id = User.generate_user_id()

        self.db.add_user(user_id, username, email, password)
        return User(user_id, username, email, password)

    def user_command(self, option: int):
        match option:
            case 1:
                self.login(Prompt.ask("Email"), Prompt.ask("Password"))
            case 2:
                ## FIXME: This is not working
                self.save_user(*User.create_user())
                pass
                
            case 3:
                self.exit()

    def create_user():
        username = Prompt.ask("Username")
        email = Prompt.ask("Email")
        password = Prompt.ask("Password", password=True)
        return username, email, password

    @staticmethod
    def exit():
        raise KeyboardInterrupt