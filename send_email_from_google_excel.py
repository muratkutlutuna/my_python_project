import gspread
from oauth2client.service_account import ServiceAccountCredentials
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

load_dotenv()
password = os.getenv("MY_PASSWORD")
email = os.getenv("MY_EMAIL")
json_path = os.getenv("JSON_PATH")

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(json_path, scope)
client = gspread.authorize(creds)

sheet = client.open("İletişim bilgileri (Yanıtlar)").sheet1
data = sheet.get_all_records()

# Get number of columns to calculate the "Email Sent?" column index
header_row = sheet.row_values(1)
sent_column_index = len(header_row) + 1  # e.g. 6 if you had 5 columns

def send_email(to_email, subject, body):
    from_email = email
    app_password = password  # NOT your normal Gmail password

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = from_email
    msg["To"] = to_email

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(from_email, app_password)
        server.sendmail(from_email, to_email, msg.as_string())

subject = "Thanks for you to filling the form!"


for index, row in enumerate(data, start=2):
    name = row["Name, Surname"]
    recipient_email = row["email address"]
    email_sent_flag = row.get("Email Sent?")

    if email_sent_flag == "Yes":
        print(f"Skipping {name} ({recipient_email}) - already sent.")
        continue

    # Email content
    body = f"""Dear {name},

Thanks for you to filling the form!

Best regards,
Murat Kutlu"""
    # Send the email
    try:
        send_email(recipient_email, subject, body)
        print(f"Email sent to {name} at {recipient_email}.")

        # Mark the email as sent in the Google Sheet
        sheet.update_cell(index, sent_column_index, "Yes")

    except Exception as e:
        print(f"❌ Failed to send email to {name} ({recipient_email}): {e}")

