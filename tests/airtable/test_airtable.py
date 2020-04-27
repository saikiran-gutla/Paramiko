import json
import requests
import pytest
from fuzzywuzzy import process


@pytest.mark.xfail(run=False)
def test_airtable_practice():
    get_headers = {
        'Authorization': 'Bearer keyq6E1toJDkJN4RM',
    }

    # get an array of donors
    get_url = 'https://api.airtable.com/v0/appihfkpqStNh6j9v/Test%20Cases%20copy?maxRecords=100&view=Full%20View'
    donors_response = requests.get(get_url, headers=get_headers)
    donors_data = donors_response.json()
    donors_list = []
    print(donors_data)
    print(len(donors_data['records']))
    for i in range(0, 2):
        donors_response = requests.get(get_url, headers=get_headers)
        donors_data = donors_response.json()
        for j in donors_data['records']:
            if j['fields']['Test Name'] not in donors_list:
                donors_list.append(j['fields']['Test Name'])
            print(j)
    print(len(donors_list))

    # POST URL(CREATES A RECORD)
    post_headers = {
        'Authorization': 'Bearer keyq6E1toJDkJN4RM',
        'Content-Type': 'application/json'
    }
    post_url = 'https://api.airtable.com/v0/appihfkpqStNh6j9v/Test%20Cases%20copy/'
    data = {
        "fields": {
            "Test Name": 're',
            "Notes": 'hello ',

        }
    }

    print(data)

    post_airtable_request = requests.post(post_url, headers=post_headers, json=data)
    status = post_airtable_request.status_code
    if status == 200:
        print("Data Inserted Successfully to Air table")
    else:
        print("Failed Inserting Data to Air table")
    pytest.xfail('Script is under development Stage')

