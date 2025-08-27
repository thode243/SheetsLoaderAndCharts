import os
import json
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

# Load credentials from environment
creds_json = os.environ["GOOGLE_CREDENTIALS"]
creds_dict = json.loads(creds_json)

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)

# Open by URL
SPREADSHEET_URL = "https://docs.google.com/spreadsheets/d/1JJ5nIJpCfX1lNHCiL3kmRXqEYeIFT2sQuXYbzNaia8U/edit"  # your full sheet URL
spreadsheet = client.open_by_url(SPREADSHEET_URL)

# Print sheet names
print("✅ Sheets found:", [ws.title for ws in spreadsheet.worksheets()])

# Example: load first sheet
ws = spreadsheet.sheet1
data = ws.get_all_records()
df = pd.DataFrame(data)

print("🔹 First 5 rows:")
print(df.head())
