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


for row in data:
    body = f"""Dear {row["Name, Surname"]},

Thanks for you to filling the form!

Best regards,
Murat Kutlu"""
    send_email(row["email address"],subject,body)  # Adjust these keys according to your form


