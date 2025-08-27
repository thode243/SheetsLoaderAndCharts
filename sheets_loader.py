import os
import json
import gspread
from google.oauth2.service_account import Credentials

# --- Load Google credentials ---
creds_info = None

# Use service account file path from env
service_account_file = os.environ.get("GOOGLE_CREDENTIALS_PATH", "service_account.json")
if os.path.exists(service_account_file):
    with open(service_account_file) as f:
        creds_info = json.load(f)
else:
    raise RuntimeError("❌ No GOOGLE_CREDENTIALS_PATH file found")

# --- Authenticate with Google Sheets ---
creds = Credentials.from_service_account_info(
    creds_info,
    scopes=[
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
)
gc = gspread.authorize(creds)

# --- Get sheet ID only for loader ---
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
