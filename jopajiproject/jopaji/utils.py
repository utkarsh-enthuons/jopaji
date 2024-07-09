from django.conf import settings
from django.core.mail import EmailMultiAlternatives
import uuid
import random
import time
from django.core.mail import send_mail


def send_email_token(email, token):
    try:
        # email_token = str(uuid.uuid4())
        subject = 'Jopaji Foods Email Verification'
        text_content = 'sdf'
        html_content = f'<p>Thanks for starting the new Jopaji Foods account. We want to make sure it\'s really you. Please verify the email by clicking on following link.</p><a href="http://127.0.0.1:8000/email-verification/{token}" target="_blank">Click here</a> for verify email.'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email, ]
        msg = EmailMultiAlternatives(subject, text_content, email_from, recipient_list)
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        print(email, token, email_from)
    except Exception as e:
        print(e)
        return False


# OTP generate page.
OTP_EXPIRY_DURATION = 300  # 5 minutes in seconds


def generate_otp():
    otp = str(random.randint(100000, 999999))  # Generate a 6-digit OTP
    timestamp = int(time.time())  # Get current timestamp
    return otp, timestamp


def send_otp_email(email, otp):
    subject = 'Your One-Time Password (OTP)'
    message = f'Your OTP is: {otp}'
    sender_email = settings.EMAIL_HOST_USER
    send_mail(subject, message, sender_email, [email], fail_silently=False)
