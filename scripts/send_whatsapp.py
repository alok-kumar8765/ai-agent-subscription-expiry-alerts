import requests

def send_whatsapp(number, message):
    token = open("config/whatsapp_token.txt").read().strip()
    phone_id = "YOUR_WHATSAPP_NUMBER_ID"

    url = f"https://graph.facebook.com/v19.0/{phone_id}/messages"

    payload = {
        "messaging_product": "whatsapp",
        "to": number,
        "type": "text",
        "text": {"body": message}
    }

    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    return requests.post(url, json=payload, headers=headers).text
