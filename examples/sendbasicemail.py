#!/Library/Frameworks/Python.framework/Versions/3.5/bin/python3
import requests

payload = {
        "access_token": MY_ENV_ACCESS_TOKEN,
        "environment": MY_ENV_NAME,
        "to": [
                {
                        "email": TEST_DEST
                }
        ],
        "subject": "rumi says",
        "text": "listen to the song of the reed flute"
}

response = requests.post("https://api.flutemail.com/v1/email", json=payload)

print(response.json())