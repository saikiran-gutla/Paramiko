import requests
from requests.auth import HTTPDigestAuth
import os
import pytest
import json
import arrow

"""
Grabs the organizations using datalayer exposed via the axtestsvc REST interface using the4
provided dictionary values.

Returns:

    dict: Org mapping of id to org name

"""


@pytest.mark.testing
def test_check():
    org_id = os.getenv('ORG_ID')
    api_key = os.getenv('API_KEY')
    user_name = os.getenv('USER_NAME')
    password = os.getenv('PASSWORD')
    print(f'Org id : {org_id}')
    print(f'Api Key : {api_key}')
    url = f"https://console.stg.automox-dev.com/api/orgs/self?o={str(org_id)}&api_key={api_key}"
    headers = {'Content-Type': 'application/json'}
    resp = requests.get(url, headers=headers, auth=HTTPDigestAuth(user_name, password),
                        verify=False)
    print(resp.json())


@pytest.mark.create_policy
def test_create_policy():
    org_id = os.getenv('ORG_ID')
    api_key = os.getenv('API_KEY')
    user_name = os.getenv('USER_NAME')
    password = os.getenv('PASSWORD')
    policy_url = f"https://console.stg.automox-dev.com/api/policies?o={str(org_id)}&api_key={api_key}"
    config_dict = {'advanced_filter': [],
                   'auto_patch': True,
                   'auto_reboot': False,
                   'filter_type': "all",
                   'filters': [],
                   'include_optional': True,
                   'missed_patch_window': False,
                   'notify_reboot_user': False,
                   'notify_user': False,
                   'patch_rule': "all",
                   'severity_filter': []}
    policy_dict = {
        'name': "saikiran",
        'notes': "",
        'organization_id': org_id,
        'policy_type_name': "patch",
        'schedule_days': 254,
        'schedule_months': 8190,
        'schedule_time': str(get_time(5)),
        'schedule_weeks_of_month': 62,
        'server_groups': []
    }
    policy_dict.update({'configuration': config_dict})
    headers = {'Content-Type': 'application/json'}
    resp = requests.post(policy_url, headers=headers, auth=HTTPDigestAuth(user_name, password),
                         data=json.dumps(policy_dict),
                         verify=False)
    print(resp.json())


def get_time(minutes):
    arw = arrow.get(arrow.utcnow())
    arw = arw.shift(minutes=minutes)
    schedule_time = arw.to('US/Mountain').format('HH:mm')
    return schedule_time
