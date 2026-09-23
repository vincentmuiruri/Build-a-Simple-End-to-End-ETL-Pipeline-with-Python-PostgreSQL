import os

import pandas as pd
import plotly.express as px
import streamlit as st
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

HOST = os.environ["DB_HOST"]
PORT = os.environ["DB_PORT"]
USER = os.environ["DB_USER"]
PASSWORD = os.environ["DB_PASSWORD"]
DB_NAME = os.environ["DB_NAME"]

CATEGORY_COLORS = [
    "#2a78d6", "#eb6834", "#1baf7a", "#eda100",
    "#e87ba4", "#008300", "#4a3aa7", "#e34948",
]
SEQUENTIAL_BLUE = "#2a78d6"

st.set_page_config(page_title="Fake Store Data", layout="wide")


@st.cache_resource
def get_engine():
    return create_engine(f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}")


@st.cache_data(ttl=300)
def load_data():
    engine = get_engine()
    products = pd.read_sql("SELECT * FROM etl.products", engine)
    users = pd.read_sql("SELECT * FROM etl.users", engine)
    
    return products, users


products, users = load_data()

st.title("Fake Store Data Dashboard")

tab_products, tab_users = st.tabs(["Products", "Users"])

with tab_products:
    st.subheader("Products")

    categories = sorted(products["product_category"].unique())
    selected = st.multiselect("Filter by category", categories, default=categories)
    filtered = products[products["product_category"].isin(selected)]

    col1, col2, col3 = st.columns(3)
    col1.metric("Total products", len(filtered))
    col2.metric(
        "Average price",
        f"${filtered['product_price'].mean():.2f}" if len(filtered) else "$0.00",
    )
    col3.metric("Categories", filtered["product_category"].nunique())

    col_a, col_b = st.columns(2)

    with col_a:
        counts = filtered["product_category"].value_counts().reset_index()
        counts.columns = ["product_category", "count"]
        fig = px.bar(
            counts,
            x="product_category",
            y="count",
            color="product_category",
            color_discrete_sequence=CATEGORY_COLORS,
            title="Products by category",
            labels={"product_category": "Category", "count": "Products"},
        )
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        avg_price = filtered.groupby("product_category", as_index=False)["product_price"].mean()
        fig2 = px.bar(
            avg_price,
            x="product_category",
            y="product_price",
            color="product_category",
            color_discrete_sequence=CATEGORY_COLORS,
            title="Average price by category",
            labels={"product_category": "Category", "product_price": "Avg price ($)"},
        )
        fig2.update_layout(showlegend=False)
        st.plotly_chart(fig2, use_container_width=True)

    fig3 = px.histogram(
        filtered,
        x="product_price",
        nbins=20,
        color_discrete_sequence=[SEQUENTIAL_BLUE],
        title="Price distribution",
        labels={"product_price": "Price ($)"},
    )
    st.plotly_chart(fig3, use_container_width=True)

    st.dataframe(filtered, use_container_width=True)

with tab_users:
    st.subheader("Users")
    st.metric("Total users", len(users))

    city_counts = users["city"].value_counts().reset_index()
    city_counts.columns = ["city", "count"]
    fig4 = px.bar(
        city_counts,
        x="city",
        y="count",
        color_discrete_sequence=[SEQUENTIAL_BLUE],
        title="Users by city",
        labels={"city": "City", "count": "Users"},
    )
    st.plotly_chart(fig4, use_container_width=True)

    st.dataframe(users, use_container_width=True)
