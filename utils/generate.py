from utils.models import Status, User, Product, Order, OrderDetails, ProductCategory
import utils.generate_utils as generate_utils
import random
from typing import Tuple, List
from utils.db_utils import insert_records, insert_record, get_one_record, get_one_record_id, get_records



USERS_COUNT = 50
PRODUCTS_COUNT = 100
CATEGORIES_COUNT = 10
PARENTLESS_CATEGORY_CHANCE = 0.3
LOYALTY_STATUSES = ["Base","Silver", "Gold", "Platinum", "Diamond"]
ORDER_STATUSES = ['New', 'Pending', 'Completed', 'Cancelled']
MAX_PRODUCTS_IN_ORDER = 5
MAX_PRODUCT_COUNT = 10

def generate_constants():
    validate = Status.model_validate
    generate = generate_utils.generate_status
    order_statuses = [validate(generate(name=name)) for name in ORDER_STATUSES]

    validate = User.model_validate
    generate = generate_utils.generate_user
    users = [validate(generate(loyalty_status=random.choice(LOYALTY_STATUSES))) for _ in range(USERS_COUNT)]
    
    validate = Product.model_validate
    generate = generate_utils.generate_product
    products = [validate(generate()) for _ in range(PRODUCTS_COUNT)]

    validate = ProductCategory.model_validate
    generate = generate_utils.generate_product_category
    categories = []
    categories.append(validate(generate(parent_id=None)))
    for i in range(1, CATEGORIES_COUNT-1):
        parent_id = None if random.random() < PARENTLESS_CATEGORY_CHANCE else random.randint(0, i-1)
        categories.append(validate(generate(parent_id=parent_id)))

    return users, products, categories, order_statuses

def insert_constants():
    users, products, categories, order_statuses = generate_constants()
    insert_records(users)
    insert_records(products)
    insert_records(categories)
    insert_records(order_statuses)

def generate_order() -> Tuple[Order, List[OrderDetails]]:
    total_amount = 0
    products_count = random.randint(1, MAX_PRODUCTS_IN_ORDER)
    products_in_order = get_records(Product, products_count)


    products_quantity = {}
    for product in products_in_order:
        products_quantity[product.id] = random.randint(1, MAX_PRODUCT_COUNT)
        total_amount += product.price * products_quantity[product.id]

    user_id = get_one_record_id(User)
    status_id = get_one_record_id(Status)
    delivered = random.random() < 0.5

    validate = Order.model_validate
    generate = generate_utils.generate_order
    order = validate(generate(user_id=user_id, status_id=status_id, total_amount=total_amount, delivered=delivered))

    validate = OrderDetails.model_validate
    generate = generate_utils.generate_order_details
    order_details = []

    for product in products_in_order:
        quantity = products_quantity[product.id]
        total_price=product.price * quantity

        order_detail = validate(generate(order_id=None, product_id=product.id, quantity=quantity, price_per_unit=product.price, total_price=total_price))
        order_details.append(order_detail)

    return order, order_details


def insert_order_with_details():
    order, order_details = generate_order()
    order_id = insert_record(order)

    for detail in order_details:
        detail.order_id = order_id
    
    insert_records(order_details)
    