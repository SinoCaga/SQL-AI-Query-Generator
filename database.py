from sqlalchemy import create_engine, text
import pandas as pd

engine = create_engine("sqlite:///sample.db")

def initialize_database():

    sample_data = pd.DataFrame({
        "id": [1, 2, 3],
        "name": ["Sino", "Alex", "Jordan"],
        "created_at": ["2023-01-15", "2022-06-10", "2023-09-21"]
    })

    sample_data.to_sql("users", engine, if_exists="replace", index=False)

def execute_query(query):

    with engine.connect() as connection:
        result = connection.execute(text(query))

        rows = [dict(row._mapping) for row in result]

    return rows