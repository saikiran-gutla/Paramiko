import requests
import json

if __name__ == '__main__':
    wekbook_url = 'https://hooks.slack.com/services/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'

    data = {
        'text': 'Hey.. Dude.. I just sent you this message from my AutoBot',
        'username': 'Saikiran Gutla',
        'icon_emoji': ':robot_face:'
    }

    response = requests.post(wekbook_url, data=json.dumps(
        data), headers={'Content-Type': 'application/json'})

    print('Response: ' + str(response.text))
    print('Response code: ' + str(response.status_code))
