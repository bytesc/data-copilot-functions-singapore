import json

import requests
import os

url = "https://www.onemap.gov.sg/api/auth/post/getToken"

with open("./agent/tools/map/utils/onemap_email.txt", "r") as email_file:
    email = email_file.read().strip()

with open("./agent/tools/map/utils/onemap_password.txt", "r") as password_file:
    password = password_file.read().strip()

payload = {
    "email": email,
    "password": password
}

response = requests.request("POST", url, json=payload)

AUTH = json.loads(response.text)["access_token"]

print(AUTH)
print(response.text)
