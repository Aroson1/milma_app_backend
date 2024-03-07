import requests
import json

def items(title: str, discription: str):
    body = {
        
        "title": title,
        "description": discription,
        "price": 30,
        "rating": 4,
    }
    response = requests.post(url="http://127.0.0.1:3000/product", json=body)
    return response.json()

def login(email: str, username: str):
    body = {
        "username": username,
        "email": email,
        "last_login": "2021-10-10 10:10:10.10+00:00",
    }
    response = requests.post(url="http://127.0.0.1:3000/user", json=body)
    return response.json()

def postOrder(username: str, item_name: str, quantity: int, total_price: int, order_date: str):
    body = {
        "username": username,
        "item_name": item_name,
        "quantity": quantity,
        "total_price": total_price,
        "order_date": order_date,
    }
    response = requests.post(url="http://127.0.0.1:3000/order", json=body)
    return response.json()

# token = login("abc@abc.com", "alex")
# print(token)

# token = items("Maggie", "Noodle it is")
# print(token)

token = postOrder("alex", "Maggie", 2, 60, "2021-10-10 10:10:10.10+00:00")
print(token)
