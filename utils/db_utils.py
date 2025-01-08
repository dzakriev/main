from sqlalchemy import func
from sqlmodel import Session, SQLModel, select, create_engine
from utils.models import create_tables, User, Product, ProductCategory, Order, OrderDetails, Status
from typing import List
from datetime import datetime


def get_engine():
    return create_engine("postgresql://admin:admin@postgres:5432/orders")

engine = get_engine()


def init_db():
    create_tables()

def insert_records(records):
    with(Session(engine)) as session:
        for record in records:
            session.add(record)
        session.commit()

def insert_record(record: SQLModel):
    with(Session(engine)) as session:
        session.add(record)
        session.commit()
        return record.id

def get_one_record_id(table: SQLModel):
    with Session(engine) as session:
        statement = select(table).order_by(func.random())
        record = session.exec(statement).first()
        return record.id

def get_one_record(table: SQLModel):
    with Session(engine) as session:
        statement = select(table).order_by(func.random())
        record = session.exec(statement).first()
        return record
    
def get_one_record_by_id(table: SQLModel, id: int):
    with Session(engine) as session:
        statement = select(table).where(table.id == id)
        record = session.exec(statement).first()
        return record

def get_records(table: SQLModel, limit=1):
    with Session(engine) as session:
        statement = select(table).order_by(func.random()).limit(limit)
        records = session.exec(statement).all()
        return records
    
def get_all_records(table: SQLModel, limit=1):
    with Session(engine) as session:
        statement = select(table)
        records = session.exec(statement).all()
        return records

def print_all_records():
    models: List[SQLModel] = [User, Product, ProductCategory, Order, OrderDetails, Status]
    for model in models:
        print(model.__name__, ":")
        for record in get_all_records(model):
            print(convert_datetime(record))
        print("\n\n\n")


def convert_datetime(data):
    if isinstance(data, SQLModel):
        return {key: convert_datetime(value) for key, value in data}
    elif isinstance(data, datetime):
        return data.isoformat()
    else:
        return data
