from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class User(BaseModel):
    id: Optional[int]
    first_name: str
    last_name: str
    email: str
    phone: str
    registration_date: datetime
    loyalty_status: str

class Product(BaseModel):
    id: Optional[int]
    name: str
    description: str
    category_id: int
    price: int
    stock_quantity: int
    creation_date: datetime

class Order(BaseModel):
    id: Optional[int]
    user_id: int
    creation_date: datetime
    total_amount: int
    status: int
    delivery_date: datetime

class OrderDetails(BaseModel):
    id: Optional[int]
    order_id: Optional[int]
    product_id: int
    quantity: int
    price_per_unit: int
    total_price: int

class ProductCategory(BaseModel):
    id: Optional[int]
    name: str
    parent_category_id: Optional[int]

class Status(BaseModel):
    id: Optional[int]
    name: str

def get_models():
    return [User, Product, ProductCategory, Order, OrderDetails, Status]
