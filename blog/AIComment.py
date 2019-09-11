import requests


def check_comment(comment):
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=6bUmcFPdStzkUHBq1dUpBg8t&client_secret=RTfGLhYQeTtcG4T6rEb20g4y9DA7PmYd'
    headers = {'Content-Type': 'application/json; charset=UTF-8'}

    response = requests.post(host, headers=headers)
    content = response.json()
    access_token = content["access_token"]

    url = f"https://aip.baidubce.com/rest/2.0/antispam/v2/spam?access_token={access_token}"
    data = {
        "content": comment
    }
    header = {"Content-Type": "application/x-www-form-urlencoded"}

    res = requests.post(url, data=data, headers=header)
    return res.json()["result"]["spam"]
