"""This file is used to fetch the report portal results data and writes that data to the google sheet specified"""
import time
import os
import gspread
import requests
from oauth2client.service_account import ServiceAccountCredentials
from AwsLoggers.aws_loggers import get_logger

bearer_token = os.getenv('BEARER_TOKEN')
project_name = os.getenv('PROJECT_NAME')
project_url = f"http://10.0.0.170:8080/api/v1/{project_name}"

params = {
    'Authorization': 'bearer ' + bearer_token,
    'Accept': 'application/json'
}
__my_logger = get_logger('Report Portal')


def test_report_portal():
    """
    This Method reads the report portal daily individual runs data and uploads it to the google sheet specified.
    The data uploaded to google sheets can be viewed in google data studio.
    Sheet Link : https://docs.google.com/spreadsheets/d/1bPMox4nDsVs4iP10c0iWgNPnP_4Qt6G_Qnic9Z2QaZ4/edit#gid=0
    Data Studio Link : https://datastudio.google.com/u/0/reporting/1-EJ7I-gx7dhnTb4ksxfWvsXR7OxYX3eG/page/bf3MB
    Returns:

    """
    url = f"{project_url}/launch/latest?page.page=1&page.size=500&filter.btw.start_time=0%3B1439%3B%2B0530&" \
          f"page.sort=start_time,number%2CDESC"
    response = requests.get(url=url, headers=params)
    resp = response.json()
    report_portal_sheet_data = []
    test_cases_data = []
    for launch in resp['content']:
        statistics_executions = launch['statistics']['executions']
        statistics_defects = launch['statistics']['defects']
        report_portal_sheet_data.append(
            [launch['name'], statistics_executions['total'], statistics_executions['passed'],
             statistics_executions['failed'], statistics_executions['skipped'],
             statistics_defects['product_bug']['total'],
             statistics_defects['automation_bug']['total'],
             statistics_defects['system_issue']['total'],
             statistics_defects['to_investigate']['total'],
             statistics_defects['no_defect']['total'],
             launch['status']])
        launch_id_url = f"{project_url}/item?page.page=1&page.size=50&page." \
                        "sort=start_time%2CASC&filter.eq.launch=" + launch['id'] + "&filter.size.path=0"
        response = requests.get(url=launch_id_url, headers=params)
        respo = response.json()
        launch_id = respo['content'][0]['launchId']
        parent_id = respo['content'][0]['id']
        all_tests = f"{project_url}/item?page.page=1&page.size=50" \
                    "&page.sort=start_time%2CASC&filter.eq.launch=" + str(launch_id) + "&filter.eq.parent=" + str(
            parent_id)
        response = requests.get(url=all_tests, headers=params)
        data = response.json()
        for name in data['content']:
            __my_logger.info(
                f"Final Test : {name['name']} and status : {name['status']} and Suit Name : {launch['name']}")
            test_cases_data.append([str(name['name']), str(launch['name']), str(name['status'])])

    save_to_sheet(test_cases_data)


def save_to_sheet(report_portal_sheet_data):
    """
    This method writes the provided data to the specified google spread sheet.
    Args:
        report_portal_sheet_data(list): Data to write to the google spread sheet

    Returns:

    """
    try:
        # Saving data to google sheets script goes here
        scope = ['https://www.googleapis.com/auth/drive']
        credentials = ServiceAccountCredentials.from_json_keyfile_name('ReportPortal-credentials.json', scope)
        # creating client to talk to sheets
        client = gspread.authorize(credentials)
        sheet = client.open('Report Portal Results Automated').worksheet('test_cases')
        sheet.clear()
        sheet.insert_row(['Test Case Name', 'Suit Name', 'Status'])
        row_number = 2
        for test_case in report_portal_sheet_data:
            sheet.insert_row(test_case, row_number)
            time.sleep(2)
            print(f'Adding Test Case to Sheet : {test_case}')
            row_number += 1
    except gspread.exceptions.APIError:
        __my_logger.error('Write requests per user per 100 seconds')
        raise gspread.exceptions.APIError
    except AttributeError:
        __my_logger.error('No sheet found with the sheet name provided')
        raise AttributeError
