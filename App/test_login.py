import requests
import json
 
def login(email: str, password: str):
   body = {
       "email": email,
       "password": password
   }
   response = requests.post(url="http://127.0.0.1:1234/email-login", json=body)
   return json.loads(response.text)["token"]
 
token = login("abc@abc.com", "password")
print(token)