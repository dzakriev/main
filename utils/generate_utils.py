import random
from datetime import datetime
from dateutil.relativedelta import relativedelta
from faker import Faker


fake = Faker(["ru_RU"])
# Faker.seed(42)

def generate_user(id=None, loyalty_status="Base"):
    return {
        'id': id,
        'first_name': fake.first_name(),
        'last_name': fake.last_name(),
        'email': fake.ascii_email(),
        'phone': fake.phone_number(),
        'registration_date': fake.date_time_between(),
        'loyalty_status': loyalty_status
    }

def generate_product(id=None, category_id=None):
    return {
        'id': id,
        'name': fake.word(),
        'description': fake.sentence(nb_words=10),
        'category_id': category_id or random.randint(1, 100),
        'price': random.randint(100, 10000),
        'stock_quantity': random.randint(1, 500),
        'creation_date': fake.date_time_between(start_date=datetime(2023, 1, 1))
    }

def generate_order(id=None, user_id=0, total_amount=0, status_id=0, delivered=False):
    month_ago = datetime.now() - relativedelta(months=1)
    week_later = datetime.now() + relativedelta(weeks=1)
    if delivered:
        creation_date = fake.date_time_between(start_date=month_ago, end_date=datetime.now())
        delivery_date = fake.date_time_between(start_date=creation_date, end_date=creation_date+relativedelta(weeks=1))
    else:
        creation_date = fake.date_time_between(start_date=month_ago, end_date=datetime.now())
        delivery_date = fake.date_time_between(start_date=datetime.now(), end_date=week_later)

    return {
        'id': id,
        'user_id': user_id,
        'creation_date': creation_date,
        # 'creation_date': fake.date_time_between(start_date=datetime(2024, 1, 1)).isoformat(),
        'total_amount': total_amount,
        'status': status_id,
        'delivery_date': delivery_date
    }

def generate_order_details(id=None, order_id=0, product_id=0, quantity=0, price_per_unit=0, total_price=0):
    return {
        'id': id,
        'order_id': order_id,
        'product_id': product_id,
        'quantity': quantity,
        'price_per_unit': price_per_unit,
        'total_price': total_price,
    }

def generate_product_category(id=None, parent_id=None):
    return {
        'id': id,
        'name': fake.word(),
        'parent_category_id': parent_id
    }

def generate_status(id=None, name=''):
    return {
        'id': id,
        'name': name
    }