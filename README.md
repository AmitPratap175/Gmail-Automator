# Gmail-Automator

Gmail-Automator is a Python-based tool designed to automate the process of sending emails via Gmail. It provides a simple interface for users to send emails programmatically, which can be particularly useful for tasks such as sending notifications, reports, or any other automated email communications.

## Features

- **Automated Email Sending**: Send emails programmatically using Gmail's SMTP server.
- **Customizable Email Content**: Personalize the subject and body of your emails.
- **Attachment Support**: Attach files to your emails.
- **Secure Authentication**: Utilizes Gmail's secure authentication mechanisms to ensure the safety of your credentials.

## Prerequisites

Before using Gmail-Automator, ensure you have the following:

- **Python 3.x**: The tool is developed using Python 3. Ensure you have Python 3.x installed on your system.
- **Gmail Account**: A valid Gmail account to send emails.
- **App Password**: For security reasons, it's recommended to use an app password instead of your main Gmail password. You can generate an app password from your Google Account settings.

## Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/AmitPratap175/Gmail-Automator.git
   ```

2. **Navigate to the Project Directory**:

   ```bash
   cd Gmail-Automator
   ```

3. **Install Required Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

   *Note: Ensure you have `pip` installed. The `requirements.txt` file contains all the necessary Python packages required to run the tool.*

## Configuration

1. **Set Up Environment Variables**:

   Create a `.env` file in the project directory and add the following:

   ```
   EMAIL_ADDRESS=your-email@gmail.com
   EMAIL_PASSWORD=your-app-password
   ```

   Replace `your-email@gmail.com` with your Gmail address and `your-app-password` with the app password you generated.

## Usage

1. **Prepare Your Email Content**:

   Define the recipient, subject, body, and any attachments you wish to include.

2. **Run the Script**:

   ```bash
   python main.py
   ```

   The script will read the configuration from the `.env` file and send the email as specified.

## Security Considerations

- **App Passwords**: Using app passwords enhances security by not exposing your main Gmail password. Always keep your app passwords confidential.
- **Environment Variables**: Storing credentials in environment variables (like the `.env` file) is a common practice to keep them out of the source code. Ensure that the `.env` file is not included in version control systems.

## Contributing

Contributions to Gmail-Automator are welcome! If you have suggestions, improvements, or bug fixes, please fork the repository and submit a pull request.
