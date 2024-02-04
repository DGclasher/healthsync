import os
from app import app
from decouple import config
from flask import current_app
from flask_mail import Message

def send_email(email, name, prescription_path):
    with app.app_context():
        try:
            msg = Message(
                f"Your prescription has been generated",
                sender=config("MAIL_USERNAME"),
                recipients=email
            )
            msg.body = f"Dear {name}\nYour prescription has been generated, please find it in the attachment."
            fp = open(prescription_path, 'rb')
            msg.attach(prescription_path.split("/")[2], 'application/pdf', fp.read())
            current_app.mail.send(msg)
            os.remove(prescription_path)
        except Exception as e:
            print(e)

