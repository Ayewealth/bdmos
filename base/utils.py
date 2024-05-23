from django.core.mail import EmailMessage
from django.conf import settings
from .models import Email


def send_single_email(to_email, subject, body):
    """
    Send a single email.
    """
    try:
        msg = EmailMessage(
            subject, body, settings.DEFAULT_FROM_EMAIL, [to_email])
        msg.send()
        # Log the email
        Email.objects.create(to=to_email, subject=subject, body=body)
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False


def send_bulk_email(to_emails, subject, body):
    """
    Send an email to multiple recipients.
    """
    try:
        msg = EmailMessage(
            subject, body, settings.DEFAULT_FROM_EMAIL, to_emails)
        msg.send()
        # Log each email
        for to_email in to_emails:
            Email.objects.create(to=to_email, subject=subject, body=body)
        return True
    except Exception as e:
        print(f"Failed to send emails: {e}")
        return False
