import gspread
from google.oauth2.service_account import Credentials
from ai_agent import ai_generate_message
from send_sms_msg91 import send_sms
from send_email import send_email
from send_whatsapp import send_whatsapp
from datetime import datetime

def run_automation():
    creds = Credentials.from_service_account_file(
        "config/creds.json",
        scopes=["https://www.googleapis.com/auth/spreadsheets"]
    )
    client = gspread.authorize(creds)

    sheet = client.open_by_key("YOUR_SHEET_ID").sheet1
    rows = sheet.get_all_records()

    today = datetime.today().date()

    for row in rows:
        name = row["User Name"]
        email = row["Email"]
        phone = str(row["Phone"])
        wa = str(row["WhatsApp Number"])
        sub = row["Subscription Name"]
        expiry = datetime.strptime(row["Expiry Date"], "%Y-%m-%d").date()
        notify_days = int(row["Notify Before"])

        delta = (expiry - today).days

        if delta in [notify_days, 7, 3, 1, 0]:
            prompt = f"Create a friendly reminder message: {name}'s subscription {sub} expires in {delta} days."
            message = ai_generate_message(prompt)

            send_sms(phone, message)
            send_email(email, "Subscription Expiry Alert", message)
            send_whatsapp(wa, message)

if __name__ == "__main__":
    run_automation()
