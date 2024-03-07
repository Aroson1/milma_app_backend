from pydantic import BaseModel

class Products(BaseModel):
    title: str
    description: str
    price: int
    available: bool
    rating: int
    categories: list
    imageurl: str
    expectedtime: int

class Users(BaseModel):
    username: str
    email: str
    hostelno: str
    phoneno: int
    # profile_picture: str
    # is_active: bool
    last_login: str
    

class CurrentOrders(BaseModel):
    rollno: str
    items: list
    quantity: list
    total_price: int
    order_date: str
    status_enum: int
    
    