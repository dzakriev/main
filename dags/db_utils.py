import os
from typing import List
import psycopg2
from pydantic import BaseModel, ValidationError

def fetch_all_rows(model: BaseModel) -> List[BaseModel]:
    print("Started fetching model: ", model.__name__)
    url = os.environ.get("DATABASE_URL", "postgresql://airflow:airflow@postgres_target:5432/orders")
    conn = psycopg2.connect(url)
    cursor = conn.cursor()

    print("ok")
    query = f"SELECT * FROM \"{model.__name__.lower()}\";"
    print("ok")

    cursor.execute(query)
    rows = cursor.fetchall()

    column_names = [desc[0] for desc in cursor.description]

    cursor.close()
    conn.close()

    result = []
    for row in rows:
        row_dict = dict(zip(column_names, row))

        try:
            result.append(model(**row_dict))
        except ValidationError as e:
            print(f"Validation error for record {row_dict.items()}: {e}")

        

    return result
