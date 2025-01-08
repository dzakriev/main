from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel, create_engine

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    first_name: str
    last_name: str
    email: str
    phone: str
    registration_date: datetime
    loyalty_status: str

class Product(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: str
    category_id: int
    price: int
    stock_quantity: int
    creation_date: datetime

class Order(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int
    creation_date: datetime
    total_amount: int
    status: int
    delivery_date: datetime

class OrderDetails(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    order_id: Optional[int]
    product_id: int
    quantity: int
    price_per_unit: int
    total_price: int

class ProductCategory(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    parent_category_id: Optional[int]

class Status(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str


def create_tables():
    engine = create_engine("postgresql://admin:admin@postgres/orders")
    SQLModel.metadata.create_all(engine)