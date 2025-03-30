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


if __name__ == "__main__":

    send_to = "suneater175@gmail.com"
    # Email body
    body = """\
Dear [Recipient's Name],

I hope you are doing well. I am writing to remind you about our upcoming meeting scheduled for [Date] at [Time]. 
We will be discussing [Brief Agenda] and reviewing key points related to [Project/Topic].

Please let me know if you have any specific topics you'd like to add to the agenda. Looking forward to your insights and a productive discussion.

Best regards,  
[Your Name]  
[Your Position]  
[Your Contact Information]
    """
    subject = "Meeting Reminder"

    save_draft(send_to, subject, body)
    send_email(send_to, subject, body)
