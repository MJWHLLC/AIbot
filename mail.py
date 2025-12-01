"""Email sending helpers for password-reset and invite flows.

This module provides a simple interface to send emails using Flask-Mail.
Email configuration comes from environment variables:
  - MAIL_SERVER: SMTP server (default: localhost)
  - MAIL_PORT: SMTP port (default: 25)
  - MAIL_USE_TLS: Enable TLS (default: False)
  - MAIL_USERNAME: SMTP username (optional)
  - MAIL_PASSWORD: SMTP password (optional)
  - MAIL_DEFAULT_SENDER: From address (required)
"""
from __future__ import annotations

import os
from typing import Optional
from flask_mail import Mail, Message

mail = Mail()


def init_mail(app):
    """Initialize Flask-Mail with the app."""
    mail.init_app(app)


def send_invite_email(to_email: str, username: str, invite_link: str) -> bool:
    """Send an invite email to a new user.
    
    Returns True if successful, False otherwise.
    """
    try:
        subject = "You're invited to Paralegal AI Assistant"
        body = f"""
Hello {username},

You have been invited to join the Paralegal AI Assistant. 
Click the link below to create your account and set your password:

{invite_link}

This link expires in 72 hours.

If you did not expect this invitation, please ignore this email.

Best regards,
Paralegal AI Assistant Team
        """
        msg = Message(subject=subject, recipients=[to_email], body=body)
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Error sending invite email: {e}")
        return False


def send_password_reset_email(to_email: str, username: str, reset_link: str) -> bool:
    """Send a password-reset email to a user.
    
    Returns True if successful, False otherwise.
    """
    try:
        subject = "Password Reset — Paralegal AI Assistant"
        body = f"""
Hello {username},

You requested a password reset for your Paralegal AI Assistant account.
Click the link below to set a new password:

{reset_link}

This link expires in 1 hour.

If you did not request a password reset, please ignore this email.

Best regards,
Paralegal AI Assistant Team
        """
        msg = Message(subject=subject, recipients=[to_email], body=body)
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Error sending password-reset email: {e}")
        return False
