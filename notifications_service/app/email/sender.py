import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from typing import Optional

load_dotenv()

class EmailSender:
    def __init__(self):
        self.smtp_host = os.getenv("EMAIL_HOST", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("EMAIL_PORT", 587))
        self.smtp_user = os.getenv("EMAIL_USER")
        self.smtp_password = os.getenv("EMAIL_PASSWORD")
        self.smtp_from = os.getenv("EMAIL_FROM", "noreply@educenter.com")
        
        if not self.smtp_user or not self.smtp_password:
            raise ValueError("EMAIL_USER and EMAIL_PASSWORD must be set in environment variables")
    
    def send_email(
        self,
        to_email: str,
        subject: str,
        message: str,
        html_message: Optional[str] = None
    ) -> bool:
        """
        Send an email using SMTP
        
        Returns:
            bool: True if email sent successfully, False otherwise
        """
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.smtp_from
            msg['To'] = to_email
            
            # Add plain text version
            msg.attach(MIMEText(message, 'plain'))
            
            # Add HTML version if provided
            if html_message:
                msg.attach(MIMEText(html_message, 'html'))
            else:
                # Simple HTML version from plain text
                html_content = f"<html><body><p>{message.replace(chr(10), '<br>')}</p></body></html>"
                msg.attach(MIMEText(html_content, 'html'))
            
            # Connect to SMTP server and send
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()  # Secure the connection
                server.login(self.smtp_user, self.smtp_password)
                server.send_message(msg)
            
            return True
            
        except Exception as e:
            print(f"Failed to send email: {e}")
            return False
    
    def send_simple_email(self, to_email: str, subject: str, message: str) -> bool:
        """Simple wrapper for sending plain text emails"""
        return self.send_email(to_email, subject, message)

# Singleton instance
email_sender = EmailSender()