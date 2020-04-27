import requests
from requests.auth import HTTPDigestAuth
import os
"""Grabs the organizations using datalayer exposed via the axtestsvc REST interface using the
provided dictionary values.

Returns:

    dict: Org mapping of id to org name

"""
org_id = 19040
url = f"https://console.stg.automox-dev.com/api/orgs/self?o={str(org_id)}"
# url = f"https://console.stg.automox-dev.com/api/orgs/self?o={str(org_id)}&api_key=4983a718-cfe4-400d-af53-1c9b7e04e836"
HEADERS = {'Content-Type': 'application/json'}
data = {
    'Username': 'mark@patchsimple.com',
    'Password': 'markmark'
}

# resp = requests.get(url, headers=HEADERS,auth=HTTPDigestAuth('mark@patchsimple.com','markmark') , verify=False)
# print(resp.text)
text = os.getenv('NAME')
print(text)