import gspread
from oauth2client import service_account


def mark_attendance(attendance):
    attendance.insert(0, "Date")

    scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
             "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

    creds = service_account.ServiceAccountCredentials.from_json_keyfile_name('creds.json', scope)

    client = gspread.authorize(creds)

    sheet = client.open("Tutorial").sheet1

    data = sheet.get_all_records()

    col = len(data[0]) + 1

    row = 1
    for ipt in attendance:
        sheet.update_cell(row, col, ipt)
        row += 1

    print("Attendance Updated Sucessfully!")

