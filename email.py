import smtplib

from config import SENDER_EMAIL, SENDER_PASSWORD, RECEIVER_EMAIL

def send_email(subject, message, from_addr, to_addr, password):
    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()
        connection.login(user=from_addr, password=password)
        connection.sendmail(from_addr, to_addr, f"Subject: {subject}\n\n{message}")


if __name__ == "__main__":
    send_email("Hello", "This is a test email", SENDER_EMAIL, RECEIVER_EMAIL, SENDER_PASSWORD)