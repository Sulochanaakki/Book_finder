import httplib2
import hmac
import hashlib
import time
import struct
import json

root = "https://dps-challenge.netlify.app/.netlify/functions/api/challenge"
content_type = "application/json"
userid = "akki.sulochana@gmail.com"
name = "DPSCHALLENGE"
shared_secret = userid+name

timestep = 120
T0 = 0

def HOTP(K, C, digits=10):
    K_bytes = str.encode(K)
    C_bytes = struct.pack(">Q", C)
    hmac_sha512 = hmac.new(key = K_bytes, msg=C_bytes, digestmod=hashlib.sha512).hexdigest()
    return Truncate(hmac_sha512)[-digits:]

def Truncate(hmac_sha512):
    offset = int(hmac_sha512[-1], 16)
    binary = int(hmac_sha512[(offset *2):((offset*2)+8)], 16) & 0x7FFFFFFF
    return str(binary)

def TOTP(K, digits=10, timeref = 0, timestep = 120):
    C = int ( time.time() - timeref ) // timestep
    return HOTP(K, C, digits = digits)

data = {'email':'akki.sulochana@gmail.com',
        'github':'https://github.com/Sulochanaakki/Book_finder',
        'url':'https://digitalproductschool.io/',
        'notes': 'deployed through  heroku'}

password = TOTP(shared_secret, 10, T0, timestep).zfill(10)
#password_new = "Basic/" + password

h = httplib2.Http()
auth =h.add_credentials(userid, password)
header = {'Content-Type':'application/json',
               'username':userid,
               'Authorization':'Basic '+ password}
resp, content = h.request(root, "POST", headers=header, body = json.dumps(data))
print(resp)