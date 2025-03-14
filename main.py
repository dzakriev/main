from utils.db_utils import init_db, print_all_records
from utils.generate import insert_order_with_details, insert_constants

def init():
    init_db()
    insert_constants()

ORDERS_AMOUNT = 500

def main():
    init()

    for _ in range(ORDERS_AMOUNT):
        insert_order_with_details()
        print("Order inserted")

    print_all_records()

if __name__ == "__main__":
    main()
