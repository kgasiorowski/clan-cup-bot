import requests
import secret
from oauth2client.service_account import ServiceAccountCredentials
import gspread
from gspread.exceptions import APIError
import json
import time

SCOPES = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

def logScores(scores):
    loggedScores = []
    try:
        with open('logged-scores.json', 'r') as loggedScoresFile:
            loggedScores = json.load(loggedScoresFile)
    except Exception:
        pass  # We can just do nothing if the file doesn't exist. The next code will create it anyway

    loggedScores.append({time.time(): scores})

    with open('logged-scores.json', 'w+') as loggedScoresFile:
        json.dump(loggedScores, loggedScoresFile)


if __name__ == "__main__":
    creds = ServiceAccountCredentials.from_json_keyfile_name('clan-cup.json', SCOPES)
    client = gspread.authorize(creds)
    sheet = client.open(secret.SHEET_NAME)
    sheet_instance = None

    while sheet_instance is None:
        try:
            sheet_instance = sheet.get_worksheet(secret.SHEET_INDEX)
        except APIError:
            content = "Looks like the Google Sheets API is having problems. Retrying in 2 minutes."
            requests.post(secret.WEBHOOK_URL, {"content": content})
            time.sleep(120)

    scores = {}
    for i in range(4):
        scores.setdefault(sheet_instance.cell(row=1, col=i+2).value, sheet_instance.cell(row=2, col=i+2).value)
    sortedScores = dict(reversed(sorted(scores.items(), key=lambda item: item[1])))

    logScores(scores)

    content = "Current team scores:\n"
    counter = 1
    for teamScore in sortedScores.items():
        content += f"{counter}. {teamScore[0]}: {teamScore[1]}\n"
        counter += 1

    requests.post(secret.WEBHOOK_URL, {"content": content})
