import os

from dotenv import load_dotenv

load_dotenv()

TIME_FORMAT = "%Y-%m-%d %H:%M:%S"
DB_NAME = "database.db"

SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")
