from sqlalchemy import func
from sqlmodel import Session, SQLModel, select, create_engine
from models import create_tables


engine = create_engine("postgresql://admin:admin@localhost/orders")

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
    
def get_records(table: SQLModel, limit=1):
    with Session(engine) as session:
        statement = select(table).order_by(func.random()).limit(limit)
        records = session.exec(statement).all()
        return records
    