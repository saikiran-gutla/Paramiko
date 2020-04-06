"""
https://developers.google.com/sheets/api
//"client_email": "sw-catalog@sw-catalog.iam.gserviceaccount.com",
"""
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

scope = ['https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)

# create client to talk to sheets
client = gspread.authorize(credentials)


# contains all the data in a sheet
# sheet = client.open('temp sw catlog').sheet1  # sheet1 is the first sheet in the spreadsheet
# url_name = []
# for i in range(3, len(sheet.get_all_records()) - 3):
#     row_data = sheet.row_values(i)
#     if len(row_data) > 1 or row_data[1] != 'NA':
#         url_name.append({row_data[0]: [{'url': row_data[1], 'latest_version': row_data[4]}]})
# for i in url_name:
#     print(i)

def get_content(url):
    html = urlopen(url)
    soup = BeautifulSoup(html, 'lxml')
    return soup


def get_content_html(url):
    html = urlopen(url)
    soup = BeautifulSoup(html.text, "html.parser")
    return soup


def clean_data(data):
    str_cells = str(data)
    clean = re.compile('<.*?>')
    data = (re.sub(clean, '', str_cells))
    return data


# Google Chrome
# google_chrome_url = url_name[0]['Google Chrome'][0]['url']
def getChromVersions(chrome_url):
    content = get_content(chrome_url)
    table_rows = content.find_all('tr')
    chrome_versions = {}
    for row in table_rows:
        data = row.find_all('td')
        if len(data) > 0:
            os = clean_data(data[0]).replace(" ", "_")
            ver = clean_data(data[1])
            print(os, ver)
            chrome_versions[os] = ver
    return chrome_versions


# JAVA
def getJavaVersion(java_url):
    content = get_content(java_url)
    table = content.find('table', class_='innerPgSignpost')
    for li in table.find_all('li'):
        ver = li.get_text()
        if "ga" in ver.lower():
            l_ver = ver.split()[1]
            a_ver = l_ver.split('u')
            build_ver_number = (a_ver[0]) + '.0.' + (a_ver[1])
            break
    return build_ver_number


# ADOBE ACROBAT READER NOT DONE
# adobe_reader_url = 'https://en.wikipedia.org/wiki/Adobe_Acrobat'
# content = get_content_html(adobe_reader_url)
# # print(f"Content : {content}")
# table = content.find('table', class_='infobox vevent')
# for tr in content.findAll('tr'):
#     for td in tr.findAll('td'):
#         data = td.get_text()
#         print(data)

# I-TUNES
itunes_url = 'https://www.theiphonewiki.com/wiki/ITunes'
content = get_content_html(itunes_url)
table = content.findAll('table', class_='wikitable')
li = []
for tab in table:
    for tr in tab.findAll('tr'):
        version = len(tr)
        li.append(td.text for td in tr.find_all('td'))
            # print(td.text)
print(li)