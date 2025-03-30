##########################################################################
# Author: Amit Pratap                                                    #   
# Date: 30-03-2025                                                       #   
##########################################################################
import imaplib
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os
from bs4 import BeautifulSoup
import email
from email.header import decode_header
from datetime import datetime
import json

load_dotenv()

# Load environment variables
IMAP_SERVER = os.getenv("IMAP_SERVER", "imap.gmail.com")
PORT =  os.getenv("PORT") # Or the appropriate port for your provider
EMAIL_ACCOUNT = os.getenv("EMAIL_ACCOUNT")
PASSWORD = os.getenv("PASSWORD")
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")


def save_draft(send_to, subject, body=None):
    
    # Step 1: Create the email
    msg = MIMEMultipart()
    msg["From"] = EMAIL_ACCOUNT
    msg["To"] = send_to  # Leave empty if it's a draft
    msg["Subject"] = subject

    # Attach email body
    msg.attach(MIMEText(body, "plain"))

    # Convert message to raw email format
    raw_email = msg.as_string()

    # Step 2: Save as Draft using IMAP
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL_ACCOUNT, PASSWORD)
        
        # Select the Drafts folder
        mail.select("[Gmail]/Drafts")  # For Gmail, this is the default Drafts folder

        # Append the email to Drafts
        mail.append("[Gmail]/Drafts", None, None, raw_email.encode("utf-8"))

        print("Email saved as draft successfully!")

        mail.close()
        mail.logout()

    except Exception as e:
        print(f"Error: {e}")

def send_email(send_to, subject, body):
    try:
        server = smtplib.SMTP(SMTP_SERVER, PORT)
        server.starttls() # Secure the connection
        server.login(EMAIL_ACCOUNT, PASSWORD)  
        server.sendmail(EMAIL_ACCOUNT, send_to, f"Subject: {subject}\n" + body)
        print("Email sent successfully!")
    except Exception as e: 
        print(f"Error sending email: {e}")
    finally:
        server.quit()

class EmailData:
    def __init__(self, sender, subject, body, date):
        self.sender = sender
        self.subject = subject
        self.body = body
        self.date = date

    def to_dict(self):
        """Convert email data to a dictionary format"""
        return {
            "sender": self.sender,
            "subject": self.subject,
            "body": self.body,
            "date": self.date,
        }

def read_email():
    # Connect to the IMAP server
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(EMAIL_ACCOUNT, PASSWORD)

    # Select the inbox
    mail.select("inbox")

    # Define filters
    sender_email = "dspratap70@gmail.com"  # Filter by sender
    date_filter = "29-Mar-2025"#str(datetime.today().strftime("%d-%b-%Y"))#"10-Mar-2018"  # Filter for emails received after this date
    search_criteria = f'(SINCE "{date_filter}" UNSEEN)'    #f'(SINCE "{date_filter}")'

    # Search for emails based on multiple filters
    status, messages = mail.search(None, search_criteria)

    # Get email IDs
    email_ids = messages[0].split()

    email_list = []  # Store structured emails here

    # Fetch and process emails
    for email_id in email_ids:
        _, msg_data = mail.fetch(email_id, "(RFC822)")
        
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                # Parse email content
                msg = email.message_from_bytes(response_part[1])
                
                # Decode the email subject
                subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes) and encoding:
                    subject = subject.decode(encoding)

                # Get the sender
                from_email = msg["From"]
                date = msg["Date"]

                # Extract and clean the email body
                body = ""
                if msg.is_multipart():
                    for part in msg.walk():
                        content_type = part.get_content_type()
                        content_disposition = str(part.get("Content-Disposition"))

                        # Get the email body
                        if "attachment" not in content_disposition:
                            try:
                                payload = part.get_payload(decode=True).decode()
                            except (AttributeError, UnicodeDecodeError):
                                payload = None

                            if content_type == "text/plain":
                                body += payload or ""
                            elif content_type == "text/html":
                                soup = BeautifulSoup(payload, "html.parser")
                                body += soup.get_text(separator="\n")

                else:
                    try:
                        body = msg.get_payload(decode=True).decode()
                        soup = BeautifulSoup(body, "html.parser")
                        body = soup.get_text(separator="\n")
                    except:
                        pass
                # Remove empty lines and unnecessary text
                lines = body.split("\n")
                cleaned_lines = [line.strip() for line in lines if line.strip()]
                body = "\n".join(cleaned_lines)

                # Print cleaned email details
                print(f"From: {from_email}")
                print(f"Subject: {subject}")
                print(f"---\nBody:\n```plaintext\n{body}\n```\n---")

                # Store in EmailData class
                email_list.append(json.dumps(EmailData(from_email, subject, body, date).to_dict()))

    # Close and logout
    mail.close()
    mail.logout()


    return email_list