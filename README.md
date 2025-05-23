# My Python Project

This project automates sending emails from a Google Excel file using a Python script scheduled with `cron`.

---

## Setup & Environment

### 1. Clone the repository

```bash
git clone https://github.com/muratkutlutuna/my_python_project.git
cd my_python_project
```

### 2. Create and activate a Python virtual environment
```bash
python3 -m venv venv
source venv/bin/activate    # On macOS/Linux
# For Windows use: venv\Scripts\activate
```
### 3. Install dependencies
```bash
pip install -r requirements.txt
```
> Make sure your requirements.txt includes all necessary packages your script uses (e.g., google-api-python-client, pandas, etc.).

### 4. Environment variables

-If your script needs environment variables (like Google API credentials), create a .env file in the root and add the required keys.

```bash
# Example .env content:
GOOGLE_API_KEY=your_api_key_here
OTHER_SECRET=your_secret_here
```
## Cron Job Setup

> To automate running the script every 10 minutes and log output, add this line to your crontab:
```bash
*/10 * * * * /Users/muratkutlutuna/Documents/python_projects/my_python_project/venv/bin/python /Users/muratkutlutuna/Documents/python_projects/my_python_project/send_email_from_google_excel.py >> /Users/muratkutlutuna/Documents/python_projects/my_python_project/log/cronlog.txt 2>&1
```
### How to edit your crontab:
```bash
crontab -e
```
> This opens your cron table in an editor. Paste the line above at the end of the file and save.

## Important Notes

- Ensure the log/ directory exists, or create it so the log file can be written:
```bash
mkdir -p /Users/muratkutlutuna/Documents/python_projects/my_python_project/log
```
- Use absolute paths for both the Python interpreter and your script in the crontab to avoid environment/path issues.
- Check *cronlog.txt* periodically to see any errors or output from the script.

## Troubleshooting
- If the cron job does not run, check:
    - That the Python path is correct (`/Users/muratkutlutuna/Documents/python_projects/my_python_project/venv/bin/python`)
    - The script has executable permissions.
    - Cron logs for errors (`/var/log/syslog` or `/var/log/cron.log` depending on your system).

## License

This project is licensed under the [MIT License](LICENSE).