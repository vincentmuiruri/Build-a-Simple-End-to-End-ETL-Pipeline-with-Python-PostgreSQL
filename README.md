# Fake API Project

An ETL pipeline that pulls product and user data from [Fake Store API](https://fakestoreapi.com/),
loads it into PostgreSQL, and visualizes it with a Streamlit dashboard.

## How it works

1. **Extract** ([etl/extract.py](etl/extract.py)) — fetches products and users from the Fake Store API.
2. **Transform** ([etl/transform.py](etl/transform.py)) — cleans and reshapes the raw JSON into flat tables.
3. **Load** ([etl/load.py](etl/load.py)) — truncates and reloads the `etl.products` and `etl.users` tables in PostgreSQL.
4. **Visualize** ([visual.py](visual.py)) — a Streamlit dashboard for exploring the loaded data.

## Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure the database connection

Copy `.env.example` to `.env` and fill in your PostgreSQL credentials:

```bash
cp .env.example .env
```

`.env` is git-ignored, so your credentials never get committed.

### 3. Prepare the database

The loader expects an `etl` schema with `products` and `users` tables already created in your
PostgreSQL database — it truncates and re-inserts into those tables rather than creating them.

## Usage

Run the ETL pipeline to fetch fresh data and load it into PostgreSQL:

```bash
python main.py
```

Launch the dashboard to explore the data:

```bash
streamlit run visual.py
```

## Project structure

```
etl/
  extract.py    # Pull data from the Fake Store API
  transform.py  # Clean and reshape the data
  load.py       # Load data into PostgreSQL
main.py         # Runs the ETL pipeline end to end
visual.py       # Streamlit dashboard
```
