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
