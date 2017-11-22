import requests

MY_ENVIRONMENT_NAME_ACCESS_TOKEN = '''eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbnZJZCI6IjFjNWUyODE1LWYxMGQtNDk1Zi1hOGM5LTEzODg5MTE2ZTBlOSIsImlkIjoiZDM2YTI0Y2UtMGJkOC00NTFkLTg1NGUtZjJiOWQ2YzdlMDJjIiwiZG9tYWluIjoiZmx1dGVzeXN0ZW1zLmNvbSIsImNyZWF0ZWRBdCI6IlwiMjAxNy0xMS0yMVQxNjozMjozOS4zNjVaXCIiLCJuYmYiOjE1MTEyODI5NjEsImF1ZCI6ImZsdXRlIiwiaXNzIjoiZmx1dGVzeXN0ZW1zIiwic3ViIjoiZmx1dGVtYWlsIiwianRpIjoiU1BBUktQT1NULUZMVVRFU1lTVEVNU0NPTSJ9.b-DvyVRLWVwfHu1_SJwGDwMzbqtTMyed6JEia7DvNBDm0n6bQI3OOBzP_C4_zrIfMFvTplS4kwExyOPA2qCtIWgPZyy6arHdWH9bqxl1rins2M_lmvNZj2M0anZONGYcXcVTckHT7M7KLf_afr8Lgi4JjclEuae3m1nRJMnt5fAo5VHnL21k85kPHYKsMOHaAtj9ABPox_4ET_698P6P7gg5JQX2Q1QKPefdLy0tAENEjG7sv6h0GpwEch0xXPc1riRCYyLxhPurDJtYHoCUD-X4BIr_2UgMYCsh2RnKCwrNkmQ7ISL04mtIzvsL5d5KTzPapQPPCkE-Z3pqDcPm3A'''

r = requests.post('https://api.flutemail.com/v1/email', json={
    "access_token": MY_ENVIRONMENT_NAME_ACCESS_TOKEN,
    "subject": "test email subject",
    "text": "test email content",
    "to": [
        {
            "email": "you@example.com",
        }
    ],
    "from": {
        "name": "Flute",
        "email": "flute_test_sender@flutemail.io"
    }
})