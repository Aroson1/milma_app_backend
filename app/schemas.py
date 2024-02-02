from pydantic import BaseModel

class Products(BaseModel):
    title: str
    description:str
    price: int
    available: bool = True
    rating: int

class Users(BaseModel):
    username: str
    email: str
    last_login: str
    # profile_picture: str
    # is_active: bool = True
    

class CurrentOrders(BaseModel):
    username: str
    item_name: str
    quantity: int
    total_price: int
    order_date: str
    is_active: bool = True
    
    