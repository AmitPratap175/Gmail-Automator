from src.graph import execute_graph
from src.utils import read_email, save_draft, send_email
import json

if __name__=="__main__":
    email_list = read_email()
    for email in email_list:

        # Convert email to dictionary
        email_info = json.loads(email)

        # Extract relevant information
        response = execute_graph(email)

        print(f"Sender: {email_info['sender']}")

        # Extract the response content
        save_draft(email_info["sender"], email_info["subject"], response)