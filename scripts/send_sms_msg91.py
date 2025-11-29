import requests

def send_sms(phone, message):
    auth = open("config/msg91_auth.txt").read().strip()
    url = "https://api.msg91.com/api/v5/flow/"

    payload = {
        "flow_id": "YOUR_FLOW_ID",
        "sender": "SENDERID",
        "recipients": [
            {"mobiles": phone, "msg": message}
        ]
    }

    headers = {"authkey": auth, "Content-Type": "application/json"}

    r = requests.post(url, json=payload, headers=headers)
    return r.text
