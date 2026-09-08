from sqlalchemy import create_engine

host = "localhost"
port = "5432"
user = "postgres"
password = "postgres"
db_name = "fake_store_db"

# Function to load data into PostgreSQL
def load_to_postgres(df, table_name):
    # Create a connection to the PostgreSQL database
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db_name}')

    # Load the DataFrame into the specified table in PostgreSQL
    df.to_sql(table_name, engine, if_exists='replace', index=False)


    print(f"Data loaded into PostgreSQL table '{table_name}' successfully.")