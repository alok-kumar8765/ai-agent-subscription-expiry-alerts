# =========================
# 🔥 AI Subscription Expiry Reminder System (Google Sheets + MSG91 + WhatsApp + Email)
# =========================

<p>
AI-powered Subscription Expiry Reminder System with Google Sheets sync, Google Calendar event creation, SMS alerts via MSG91, WhatsApp notifications using WhatsApp Cloud API, and email alerts via Gmail API.
Fully automated using Python, OpenAI (with fallback to local Llama3), and cron jobs.
</p>

<b>Features include:</b>

-	✅ Auto-sync Excel → Google Sheets
-	✅ AI Agent for reminder message generation
-	✅ Multi-channel notifications (SMS, Email, WhatsApp)
-	✅ Google Calendar integration
-	✅ Daily cron-based automation
-	✅ OpenAI + Local AI (Ollama) fallback
-	✅ Ideal for subscription management, expiry alerts, and automated reminders

<p>Perfect for developers, startups, and businesses wanting an easy extensible subscription notification platform.</p>

---

# 🚀 FULL END-TO-END SOLUTION: Subscription Expiry Notification System

### =============================
### 1️⃣ SYSTEM FOLDER STRUCTURE
### =============================

``` graphql
subscription-notifier/
│
├── config/
│   ├── creds.json               # Google API credentials
│   ├── whatsapp_token.txt       # WhatsApp Cloud API Token
│   ├── msg91_auth.txt           # MSG91 Auth Key
│   ├── openai_key.txt           # OpenAI API Key (if available)
│
├── data/
│   └── master_sheet_backup.xlsx
│
├── scripts/
│   ├── sync_excel_to_sheets.py
│   ├── calendar_sync.gs         # Google Apps Script
│   ├── ai_agent.py
│   ├── send_sms_msg91.py
│   ├── send_whatsapp.py
│   ├── send_email.py
│   ├── automate.py              # master automation
│
├── local_ai/
│   ├── run_local_llama.py
│   ├── model/ (auto-downloaded)
│
└── README_SETUP.md
```
---

### ======================================
### 2️⃣ GOOGLE SHEET TEMPLATE (MASTER DATA)
### ======================================

<p>Create a Google Sheet with the following columns: </p>

```
A: User Name
B: Email
C: Phone
D: WhatsApp Number
E: Subscription Name
F: Start Date
G: Expiry Date
H: Notify Before (days)
I: Status (AUTO: Active/Expired)
```

---

### =============================================
### 3️⃣ SYNC EXCEL → GOOGLE SHEETS (Python Script)
### =============================================

<p>scripts/sync_excel_to_sheets.py</p>

``` Python
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

def sync_excel_to_google_sheet():
    excel_path = "data/master_sheet_backup.xlsx"
    sheet_id = "YOUR_GOOGLE_SHEET_ID"

    df = pd.read_excel(excel_path)

    creds = Credentials.from_service_account_file(
        "config/creds.json",
        scopes=["https://www.googleapis.com/auth/spreadsheets"]
    )
    client = gspread.authorize(creds)
    sheet = client.open_by_key(sheet_id).sheet1

    sheet.clear()
    sheet.update([df.columns.values.tolist()] + df.values.tolist())

if __name__ == "__main__":
    sync_excel_to_google_sheet()
	
```

---

## =============================
## 4️⃣ GOOGLE CALENDAR SYNC SCRIPT
## =============================

<p>Create scripts/calendar_sync.gs in Google Apps Script: </p>

```javascript
function syncCalendar() {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("Sheet1");
  const calendar = CalendarApp.getCalendarById("primary");

  const data = sheet.getRange(2, 1, sheet.getLastRow() - 1, 9).getValues();

  data.forEach(row => {
    const [name, email, phone, wa, sub, start, expiry] = row;

    if (!expiry) return;

    const title = sub + " Expiry Reminder";
    const desc = `User: ${name}\nEmail: ${email}\nPhone: ${phone}\nWhatsApp: ${wa}`;

    calendar.createAllDayEvent(title, new Date(expiry), { description: desc });
  });
}
```
	- Set trigger:
		- Triggers → Daily → Time-Driven → Every day at 8 AM
---

## ===========================================
## 5️⃣ AI AGENT (OpenAI + Fallback to Local Llama)
## =============================

<p>scripts/ai_agent.py </p>

```Python
import os
import openai
import requests
import subprocess

def ai_generate_message(text):
    try:
        key = open("config/openai_key.txt").read().strip()
        openai.api_key = key
        completion = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": text}]
        )
        return completion['choices'][0]['message']['content']
    except:
        print("⚠ Switching to local AI model (Llama).")
        result = subprocess.run(
            ["python", "local_ai/run_local_llama.py", text],
            capture_output=True, text=True
        )
        return result.stdout

```
---

## =============================
## 6️⃣ SMS via MSG91
## =============================

<p> scripts/send_sms_msg91.py</p>

```Python
import requests

def send_sms(phone, message):
    auth = open("config/msg91_auth.txt").read().strip()
    url = "https://api.msg91.com/api/v5/flow/"

    payload = {
        "flow_id": "YOUR_FLOW_ID",
        "sender": "SENDERID",
        "recipients": [
            {"mobiles": phone, "msg": message}
        ]
    }

    headers = {"authkey": auth, "Content-Type": "application/json"}

    r = requests.post(url, json=payload, headers=headers)
    return r.text

```
---

## ================================
## 7️⃣ WhatsApp (Official Cloud API)
## ================================

<p>scripts/send_whatsapp.py</p>
```Python
import requests

def send_whatsapp(number, message):
    token = open("config/whatsapp_token.txt").read().strip()
    phone_id = "YOUR_WHATSAPP_NUMBER_ID"

    url = f"https://graph.facebook.com/v19.0/{phone_id}/messages"

    payload = {
        "messaging_product": "whatsapp",
        "to": number,
        "type": "text",
        "text": {"body": message}
    }

    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    return requests.post(url, json=payload, headers=headers).text

```
---

## =============================
## 8️⃣ Email (Using Gmail API)
## =============================

<p>scripts/send_email.py</p>
```Python
import smtplib
from email.mime.text import MIMEText

def send_email(to, subject, body):
    sender = "your@gmail.com"
    pwd = "YOUR_APP_PASSWORD"

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = to

    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login(sender, pwd)
    server.sendmail(sender, [to], msg.as_string())
    server.quit()
```
---

## =============================
## 9️⃣ MAIN AUTOMATION (Runs Daily)
## =============================

<p>scripts/automate.py</p>
```Python
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
```
---

## ===================================
## 🔟 LOCAL AI MODEL (Fallback Llama)
## ===================================

<p>local_ai/run_local_llama.py</p>
```Python
import sys
from ollama import Client

client = Client()

prompt = sys.argv[1]

resp = client.chat(model="llama3", messages=[{"role": "user", "content": prompt}])
print(resp['message']['content'])
```
---

## =============================
## 1️⃣1️⃣ CRON JOB / TASK SCHEDULER
## =============================

<p>Linux</p>
```nginx
crontab -e
```
<p>Add:</p>
```ruby
0 9 * * * /usr/bin/python3 /path/scripts/automate.py
```

### **Windows**

| Use Task Scheduler → Run daily at 9 AM.
---

# ✅ subscription-notifier/config/ — FULL EXPLANATION

### Below are the 4 required config files, their correct format, and how to generate them.

## 1️⃣ creds.json (Google API Credentials)

<p>This file is needed for:

✔ Reading Google Sheets
✔ Updating Google Sheets
✔ Using Google Calendar via Apps Script (optional)</p>

## How to Generate creds.json

* Go to Google Cloud Console:
	| https://console.cloud.google.com/
* Create a New Project → subscription-notifier

* Enable APIs:

	* Google Sheets API

	* Google Drive API

* Go to:
	| APIs & Services → Credentials → Create Credentials → Service Account

* After creating the service account:

	* Click “Keys”

	* Add Key → JSON

    * Download it

* Rename it to:
```pgsql
creds.json
```

* Put it here:
```pgsql
subscription-notifier/config/creds.json
```
---

### ✔ Example creds.json (Structure)
```json
{
  "type": "service_account",
  "project_id": "subscription-notifier",
  "private_key_id": "948ae8ac087c...",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhki...==\n-----END PRIVATE KEY-----\n",
  "client_email": "your-service-account@subscription-notifier.iam.gserviceaccount.com",
  "client_id": "1069383938383938",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/your-service-account"
}
```
<p>⚠ Do NOT edit this file manually.
Just download it from Google Cloud.</p>
---

# **2️⃣ whatsapp_token.txt (WhatsApp Cloud API Token)**

### This file stores your WhatsApp Cloud API token (Meta).

## How to Generate WhatsApp Token

*	Go to:
		| https://developers.facebook.com/apps/

*	Create App → Business → WhatsApp

*	Go to:
		* WhatsApp → API Settings

*	Copy:
		* 👉 Permanent Access Token
		* 👉 WhatsApp Business Phone Number ID

* 	Save only the token in this file:

## **✔ Example whatsapp_token.txt**
```
EAAI29VbF89OABAqZC2sZAa8ZAXFZB0BOb8I6...
```
---

# **3️⃣ msg91_auth.txt (MSG91 Auth Key)**

### For sending SMS in India without delays.

## How to Get the Auth Key:

1 . Go to MSG91 Dashboard:
	| https://control.msg91.com/

2 . Login → Tools → API Keys

3 . Click Generate Authkey
<p>Copy this key.</p>

## **✔ Example msg91_auth.txt**
```
378819AqvHns8M9NvBdjE2a041p
```
---

# **4️⃣ openai_key.txt (Optional — OpenAI Key)**

### This key is only used when you have free OpenAI quota.
### If it fails → your system automatically switches to local AI (Ollama + Llama).

## How to get OpenAI API Key:

	| https://platform.openai.com/api-keys

-	Click Create new secret key

## **✔ Example openai_key.txt**
```
sk-4KZGrewaZlE3PiSy0EwHA28Fjh7fZlnVpukBPQdX
```
---

