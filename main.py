import requests
import secret
from oauth2client.service_account import ServiceAccountCredentials
import gspread

SCOPES = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']


if __name__ == "__main__":
    creds = ServiceAccountCredentials.from_json_keyfile_name('clan-cup.json', SCOPES)
    client = gspread.authorize(creds)
    sheet = client.open(secret.SHEET_NAME)
    sheet_instance = sheet.get_worksheet(secret.SHEET_INDEX)

    content = "Current team scores:\n"

    for i in range(4):
        content += f"{sheet_instance.cell(row=1,col=i+2).value}: {sheet_instance.cell(row=2,col=i+2).value}\n"

    requests.post(secret.WEBHOOK_URL, {"content": content})
