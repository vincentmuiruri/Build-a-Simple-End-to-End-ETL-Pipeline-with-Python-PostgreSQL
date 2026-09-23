import pandas as pd
import requests

# Base URL for the Fake Store API
BASE_URL = "https://fakestoreapi.com"

# Extract product data from the Fake Store API
def extract_product():
    url = f'{BASE_URL}/products'
    response = requests.get(url)
    response.raise_for_status()

    data = response.json()
    product_df = pd.DataFrame(data)

    return product_df

# Extract user data from the Fake Store API
def extract_users():
    url = f'{BASE_URL}/users'
    response = requests.get(url)
    response.raise_for_status()

    data = response.json()
    user_df = pd.DataFrame(data)

    return user_df