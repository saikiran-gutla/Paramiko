"""
https://developers.google.com/sheets/api
//"client_email": "sw-catalog@sw-catalog.iam.gserviceaccount.com",
"""
import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)

# create client to talk to sheets
client = gspread.authorize(credentials)

# contains all the data in a sheet
sheet = client.open('temp sw catlog').sheet1  # sheet1 is the first sheet in the spreadsheet
# print(sheet.get_all_records())
print(sheet.row_values(3))
# print(sheet.col_values(3))

# find row,col by name
cell = sheet.find('Java')
print(cell.row)
print(cell.col)
print(cell.value)

# sheet.update_cell(3, 1, 'Google Chrome')

# Imserting data
data_insert = ["random", 'bandom']
sheet.insert_row(data_insert, 53)

# print(data)
