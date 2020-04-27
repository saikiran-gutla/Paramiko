"""
https://developers.google.com/sheets/api
//"client_email": "reportportal@reportportal-275110.iam.gserviceaccount.com",
"""
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Saving data to google sheets script goes here
scope = ['https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('ReportPortal-credentials.json', scope)
# create client to talk to sheets
client = gspread.authorize(credentials)
# contains all the data in a sheet
sheet = client.open('Report Portal Results').sheet1


def save_to_sheet(report_portal_sheet_data):
    sheet.delete_rows(2, len(report_portal_sheet_data) + 2)
    row_number = 2
    for test_case in report_portal_sheet_data:
        sheet.insert_row(test_case, row_number)
        row_number += 1
    return True
