import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os

# Role-wise email groups
ROLE_MEMBERS = {
    "A": ["alice_ops@example.com", "precu.college@gmail.com","bhavyacodes19@gmail.com"], # Operations/Safety
    "B": ["priya23704@gmail.com","hvrdummy456@gmail.com"],    # Finance
    "C": ["riya.college0125@gmail.com", "chetan_hr@example.com","priya.bhatnagar158@nmims.in"], # HR
    "D": ["deepa_legal@example.com", "dev_legal@example.com","priya.bhatnagar58@nmims.in"], # Legal
    "E": ["mkrish1411@gmail.com","palak.gada136@nmims.edu.in"],  # Misc
    "ADMIN": ["work.atharva98@gmail.com","aditpunamiya28@gmail.com","priya23704@gmail.com"],
}


GMAIL_USER = "priya23704@gmail.com"
GMAIL_APP_PASSWORD = "sbbm mbkv tllr adyy" 

def send_email(role, subject, body, attachments=None):
    if role == "ALL":
        recipients = [email for members in ROLE_MEMBERS.values() for email in members]
    else:
        recipients = ROLE_MEMBERS.get(role.upper(), [])

    if not recipients:
        print(f"[WARN] No recipients for role {role}")
        return

    # Email message setup
    msg = MIMEMultipart()
    msg['From'] = GMAIL_USER
    msg['To'] = ", ".join(recipients)
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    # Attach files if provided
    if attachments:
        for file_path in attachments:
            if os.path.exists(file_path):
                part = MIMEBase('application', 'octet-stream')
                with open(file_path, 'rb') as f:
                    part.set_payload(f.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(file_path)}')
                msg.attach(part)
            else:
                print(f"[WARN] Attachment {file_path} not found")

    # Send email
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
            server.sendmail(GMAIL_USER, recipients, msg.as_string())
        print(f"[SUCCESS] Email sent to role {role}: {', '.join(recipients)}")
    except Exception as e:
        print(f"[ERROR] Failed to send email: {e}")

if __name__ == "__main__":
    print("=== Role-based Email System ===")
    role = input("Enter role to send email to (A, B, C, D, E, ADMIN, or ALL): ").strip().upper()
    subject = input("Enter email subject: ")
    body = input("Enter email body: ")
    attachments_input = input("Enter attachment file paths separated by commas (or leave empty): ")
    attachments = [f.strip() for f in attachments_input.split(",")] if attachments_input else []

    send_email(role, subject, body, attachments)
