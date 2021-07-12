import hashlib
import sys
from datetime import time
import requests
import base64
from passlib.totp import TOTP
import pyotp

url = "https://dps-challenge.netlify.app/.netlify/functions/api/challenge"
totp = pyotp.TOTP(base64.b32encode("akki.sulochana@gmail.comDPSCHALLENGE".encode()).decode(), digits=10,
 digest=hashlib.sha512).now()


print("Current OTP:", totp)
headers = {'Authorization': "Basic/"+totp,
           'Content-Type': "application/json"}
payload = {'email':'akki.sulochana@gmail.com',
        'github':'https://github.com/Sulochanaakki/Book_finder',
        'url':'https://digitalproductschool.io/',
        'notes': 'deployed through  heroku'}


retries = 1
success = False
while not success:
    try:
        response = requests.post(url, headers=headers, data=payload, verify=False)
        success = True
        print(response)
    except Exception as e:
        wait = retries * 30;
        print("error! waitng %s secs and re trying..." % wait)
        sys.stdout.flush()
        time.sleep(wait)
        retries += 1