import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

host = os.environ["DB_HOST"]
port = os.environ["DB_PORT"]
user = os.environ["DB_USER"]
password = os.environ["DB_PASSWORD"]
db_name = os.environ["DB_NAME"]

# Create a connection to the PostgreSQL database
engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db_name}')

# Function to load data into PostgreSQL
def load_to_postgres(df, table_name, schema="etl"):
    # engine.begin() wraps the truncate and the insert in one transaction,
    # so a failed load won't leave you with an empty table
    with engine.begin() as conn:
        conn.execute(text(f"TRUNCATE TABLE {schema}.{table_name}"))
        df.to_sql(table_name, conn, schema=schema, if_exists="append", index=False)

    print(f"Data loaded into PostgreSQL table '{schema}.{table_name}' successfully.")