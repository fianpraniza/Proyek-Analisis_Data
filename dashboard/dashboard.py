import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from datetime import datetime

# Set up page configuration
st.set_page_config(
    page_title="E-commerce Analysis Dashboard",
    page_icon="🛍️",
    layout="wide"
)

# Function to load data
@st.cache_data
def load_data():

    datetime_cols = ["order_approved_at", "order_delivered_carrier_date", "order_delivered_customer_date", "order_estimated_delivery_date", "order_purchase_timestamp", "shipping_limit_date"]
    df = pd.read_csv("allData.csv")
    df.sort_values(by="order_approved_at", inplace=True)
    df.reset_index(inplace=True)
    df['order_approved_at'] = pd.to_datetime(df['order_approved_at'])

    min_date = df["order_approved_at"].min()
    max_date = df["order_approved_at"].max()
    return df

# Load data
try:
    df = load_data()

    # Header
    st.title("📊 E-commerce Analysis Dashboard")
    st.markdown("---")

    # Sidebar filters
    st.sidebar.header("Filters")
    
    # Date range filter
    date_range = st.sidebar.date_input(
        "Select Date Range",
        [df['order_approved_at'].min(), df['order_approved_at'].max()]
    )

    # Filter data berdasarkan date range
    mask = (df['order_approved_at'].dt.date >= date_range[0]) & (df['order_approved_at'].dt.date <= date_range[1])
    filtered_df = df.loc[mask]

    # Layout dengan 2 kolom
    col1, col2 = st.columns(2)

    with col1:
        # Top Products by Sales
        st.subheader("Top 10 Most Sold Products")
        top_products = filtered_df.groupby('product_category_name')['product_id'].count().sort_values(ascending=False).head(10)
        
        fig_top_products = px.bar(
            x=top_products.values,
            y=top_products.index,
            orientation='h',
            title="Top 10 Products by Sales Volume",
            labels={'x': 'Total Quantity Sold', 'y': 'Product Name'}
        )
        st.plotly_chart(fig_top_products, use_container_width=True)

    with col2:
        df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'], errors='coerce')
        # Sales Trend Over Time
        monthly_sales = df.groupby(pd.Grouper(key='order_purchase_timestamp', freq='M')).agg({
             'order_item_id': 'count',  # Menghitung jumlah item terjual
             'price': 'sum'  # Menghitung total harga
        }).reset_index()
        
        st.subheader("Monthly Sales Trend")

        plt.figure(figsize=(10, 5))
        plt.plot(monthly_sales['order_purchase_timestamp'].dt.strftime('%Y-%m'), monthly_sales['price'], marker='o', color='b', linestyle='-')
        plt.xlabel('Bulan')
        plt.ylabel('Total Penjualan')
        plt.title('Tren Penjualan Bulanan')
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.tight_layout()

# Menampilkan grafik di Streamlit
        st.pyplot(plt)

except Exception as e:
    st.error(f"Error loading data: {str(e)}")
    st.info("Please make sure your dataset contains the required columns: 'order_approved_at', 'product_id', 'order_item_id', and 'price'")