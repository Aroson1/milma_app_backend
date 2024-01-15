import requests
import json
 
def login(email: str, password: str):
   body = {
       "email": email,
       "password": password
   }
   response = requests.post(url="http://127.0.0.1:1234/email-login", json=body)
   print(json.loads(response.text)["user_id"])
   return json.loads(response.text)["token"]
 
token = login("abc@abc.com", "password")
 
def ping(token: str):
   headers = {
       'authorization': token
   }
   response = requests.post(url="http://127.0.0.1:1234/ping", headers=headers)
   return(response.text)
 
print(ping(token))