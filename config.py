import os

from dotenv import load_dotenv

load_dotenv()

TIME_FORMAT = "%Y-%m-%d %H:%M:%S"
DB_NAME = "database.db"
CSV_NAME = "tasks.csv"

SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")

PASSWORD_ATTEMPTS = 3  # If -1, no limit

remember = False
remember_email = None