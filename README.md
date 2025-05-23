# 📨 Google Sheet Auto Mailer (Cron-Based Python App)

This Python project reads a Google Sheets spreadsheet, sends personalized emails to listed contacts, and logs the status back to the sheet. It's designed to run automatically every 10 minutes via a scheduled cron job.

---

## 📁 Project Structure

```bash
.
├── .env                    # Stores sensitive environment variables
├── .gitignore             # Ignores secrets, logs, virtual env, etc.
├── LICENSE                # MIT License file
├── README.md              # You're reading it
├── requirements.txt       # Python packages required
├── send_email_from_google_excel.py  # Main script
├── api_docs/              # Google API credentials (ignored in git)
├── log/                   # Cron log output
│   └── cronlog.txt
├── venv/                  # Python virtual environment (ignored in git)
```

---



## 🛠 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/muratkutlutuna/my_python_project.git
cd my_python_project
```

---

### 2. Create and Activate a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
# For Windows use: venv\Scripts\activate
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Add Environment Variables

Create a `.env` file in the root directory:

```bash
touch .env
```

Add the following content (replace values accordingly):

```env
MY_EMAIL=your_email@gmail.com
MY_PASSWORD=your_email_app_password
JSON_PATH=/full/path/to/api_docs/your_google_api_credentials.json
SLACK_BOT_TOKEN=xoxb-xxx-your-token-here
SLACK_CHANNEL=#automation-logs
```

💡 Tip: Use `absolute paths` for things like `JSON_PATH`.

---

### 5. Add Your Google API Credentials

- Visit the [Google Cloud Console](https://console.cloud.google.com/)
- Enable the **Google Sheets API** and **Google Drive API**
- Create a service account and download the `.json` key
- Save the file to `api_docs/` and update your `.env` accordingly

---



## 🕰 Cron Job Setup

🛑 Important:

- Use **absolute paths** for Python and your script.
- Make sure the script is executable:  
  ```bash
  chmod +x send_email_from_google_excel.py
  ```
- Ensure the `log/` folder exists:
  ```bash
  mkdir -p log
  ```

To run the script automatically every 10 minutes:

1. Open your crontab:

```bash
crontab -e
```

2. Add the following line (change paths if needed):

```bash
*/10 * * * * /Users/muratkutlutuna/Documents/python_projects/my_python_project/venv/bin/python /Users/muratkutlutuna/Documents/python_projects/my_python_project/send_email_from_google_excel.py >> /Users/muratkutlutuna/Documents/python_projects/my_python_project/log/cronlog.txt 2>&1
```

---



## 🧪 Testing

Run the script manually to make sure it works:

```bash
source venv/bin/activate
python send_email_from_google_excel.py
```

Check:

- Console output
- Emails received
- Google Sheet updated
- `log/cronlog.txt` for cron output

---



## 🧠 Troubleshooting

- **Script doesn’t run via cron?**  
  - Log environment: `env > /tmp/env.output` inside your cron command to debug
  - Check cron logs: `grep CRON /var/log/system.log` (macOS)
- **Missing dependencies?**  
  Reinstall:
  ```bash
  pip install -r requirements.txt
  ```

- **Invalid credentials or access denied?**
  - Double-check service account email is shared with the Google Sheet.
  - Verify `.env` paths.

---



## ✅ Features

- Sends emails only if not already sent
- Updates Google Sheet with timestamp and status
- Posts success/failure messages to Slack
- Logs everything to a local file

---



## 📜 License

This project is licensed under the [MIT License](LICENSE).

---



## 🤝 Contributing

Pull requests are welcome. For major changes, open an issue first to discuss what you'd like to change.


---