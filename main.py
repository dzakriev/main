from utils.db_utils import init_db, get_one_record_by_id, print_all_records
from utils.generate import insert_order_with_details, insert_constants
from sqlmodel import SQLModel

def init():
    init_db()
    insert_constants()

ORDERS_AMOUNT = 10

def main():
    init()

    for _ in range(ORDERS_AMOUNT):
        insert_order_with_details()
        print("Order inserted")

    print_all_records()

if __name__ == "__main__":
    main()
