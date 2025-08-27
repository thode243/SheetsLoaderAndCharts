import os
import requests
import pandas as pd
import gspread
import os
from time import sleep
from datetime import datetime, date
from datetime import time as dtime
import pytz
from oauth2client.service_account import ServiceAccountCredentials
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import logging
import sys
import uuid

# --- Load Google credentials ---
service_account_file = os.environ.get("GOOGLE_CREDENTIALS_PATH", "service_account.json")
if os.path.exists(service_account_file):
    with open(service_account_file) as f:
        content = f.read()
        print("JSON content:", content)  # Debug the JSON content
        try:
            creds_info = json.load(f)
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
            raise
else:
    raise RuntimeError(f"❌ No GOOGLE_CREDENTIALS_PATH file found at {service_account_file}")

# --- Authenticate with Google Sheets ---
creds = Credentials.from_service_account_info(
    creds_info,
    scopes=[
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
)
gc = gspread.authorize(creds)

# --- Get sheet ID for the new sheet ---
sheet_id = os.environ.get("SHEET_ID2")
if not sheet_id:
    raise RuntimeError("❌ SHEET_ID2 env variable not set")

# Open spreadsheet and first worksheet
sh = gc.open_by_key(sheet_id)
worksheet = sh.get_worksheet(0)
data = worksheet.get_all_values()

print(f"✅ Loaded {len(data)} rows from sheet '{worksheet.title}'")

# Example: just print first 5 rows
for row in data[:5]:
    print(row)
