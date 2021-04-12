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

    scores = {}
    for i in range(4):
        scores.setdefault(sheet_instance.cell(row=1, col=i+2).value, sheet_instance.cell(row=2, col=i+2).value)
    sortedScores = dict(reversed(sorted(scores.items(), key=lambda item: item[1])))

    content = "Current team scores:\n"
    counter = 1
    for teamScore in sortedScores.items():
        content += f"{counter}. {teamScore[0]}: {teamScore[1]}\n"
        counter += 1

    requests.post(secret.WEBHOOK_URL, {"content": content})
