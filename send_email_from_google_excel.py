#!/Users/muratkutlutuna/Documents/python_projects/my_python_project/venv/bin/python
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


load_dotenv(dotenv_path="/Users/muratkutlutuna/Documents/python_projects/my_python_project/.env")
password = os.getenv("MY_PASSWORD")
email = os.getenv("MY_EMAIL")
json_path = os.getenv("JSON_PATH")
slack_token = os.getenv("SLACK_BOT_TOKEN")
slack_channel = os.getenv("SLACK_CHANNEL")  # e.g., "#automation-logs"
slack_client = WebClient(token=slack_token)

def send_slack_message(message):
    try:
        slack_client.chat_postMessage(channel=slack_channel, text=message)
    except SlackApiError as e:
        print(f"Slack error: {e.response['error']}")

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(json_path, scope)
client = gspread.authorize(creds)

# Open the sheet
sheet = client.open("İletişim bilgileri (Yanıtlar)").sheet1

# Get headers
headers = sheet.row_values(1)

# Add "Sent Timestamp" if missing
if "Sent Timestamp" not in headers:
    headers.append("Sent Timestamp")
    sheet.update("1:1", [headers])  # Update only header row

# Re-fetch updated headers to get correct column indexes
headers = sheet.row_values(1)

# Get column indexes (+1 because gspread is 1-indexed)
sent_col_idx = headers.index("Email Sent?") + 1
timestamp_col_idx = headers.index("Sent Timestamp") + 1

# Fetch all form responses as list of dicts
data = sheet.get_all_records()

def send_email(to_email, subject, body):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = email
    msg["To"] = to_email

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(email, password)
        server.sendmail(email, to_email, msg.as_string())

subject = "Thanks for filling the form!"

# Loop through each row
for i, row in enumerate(data):
    name = row.get("Name, Surname")
    recipient_email = row.get("email address")
    email_sent_flag = row.get("Email Sent?")
    sent_timestamp = row.get("Sent Timestamp")
    sheet_row_index = i + 2  # +2 because data starts from row 2 in the sheet

    if not email_sent_flag or email_sent_flag.strip().lower() != "yes":
        # Send email
        body = f"""Dear {name},

Thanks for filling out the form!

Best regards,
Murat Kutlu"""
        try:
            send_email(recipient_email, subject, body)
            timestamp_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"✅ Email sent to {name} ({recipient_email}) at {timestamp_now}")
            # Update the sheet with "Yes" and timestamp
            sheet.update_cell(sheet_row_index, sent_col_idx, "Yes")
            sheet.update_cell(sheet_row_index, timestamp_col_idx, timestamp_now)
            send_slack_message(f"✅ Email sent to {row['email address']} at {timestamp_now}")
        except Exception as e:
            print(f"❌ Failed to send email to {name} ({recipient_email}): {e}")
            send_slack_message(f"❌ Failed to send email to {row['email address']}: {str(e)}")
    else:
        if sent_timestamp:
            print(f"ℹ️ Already sent to {name} at {recipient_email} on {sent_timestamp}")
        else:
            print(f"⚠️ Already sent to {name} at {recipient_email}, but no timestamp recorded.")