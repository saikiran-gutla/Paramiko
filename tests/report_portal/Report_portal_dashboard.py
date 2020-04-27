import requests

from tests.report_portal.report_portal_sheet import save_to_sheet

project = 'STG'
launches_url = 'http://10.0.0.170:8080/api/v1/' + project + '/launch'
bearer_token = '101721a2-78a6-4cbe-87e2-fbe9849dd2c7'
params = {
    'Authorization': 'bearer ' + bearer_token,
    'Accept': 'application/json'
}
try:
    response = requests.get(url=launches_url, headers=params)
    data = response.json()
except ConnectionError:
    print(f"VPN is not connected")

report_portal_sheet_data = []
for launch in data['content']:
    statistics_executions = launch['statistics']['executions']
    statistics_defects = launch['statistics']['defects']
    print(
        f"Launch Name : {launch['name']} \t Status : {launch['status']} \t Total Statistics : {statistics_executions['total']}"
        f"\tPassed : {statistics_executions['passed']} \t Failed : {statistics_executions['failed']} \t"
        f"Skipped : {statistics_executions['skipped']},Product Bug : {statistics_defects['product_bug']['total']} \t"
        f"Automation Bug : {statistics_defects['automation_bug']['total']} \t "
        f"System Issue : {statistics_defects['system_issue']['total']} \t "
        f"To Investigate {statistics_defects['to_investigate']['total']} \t"
        f"No Defects : {statistics_defects['no_defect']['total']}")
    report_portal_sheet_data.append([launch['name'], statistics_executions['total'], statistics_executions['passed'],
                                     statistics_executions['failed'], statistics_executions['skipped'],
                                     statistics_defects['product_bug']['total'],
                                     statistics_defects['automation_bug']['total'],
                                     statistics_defects['system_issue']['total'],
                                     statistics_defects['to_investigate']['total'],
                                     statistics_defects['no_defect']['total'],
                                     launch['status']])
status = save_to_sheet(report_portal_sheet_data)
if status:
    print(f'Data written to Document Successfully')
