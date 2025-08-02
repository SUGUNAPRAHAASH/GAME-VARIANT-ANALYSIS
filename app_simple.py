import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Page configuration
st.set_page_config(
    page_title="Simple Data Dashboard",
    page_icon="📊",
    layout="wide"
)

# Main content
st.title("📊 Simple Data Analytics Dashboard")
st.markdown("---")

# Generate sample data
@st.cache_data
def generate_sample_data():
    np.random.seed(42)
    dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='D')
    
    data = {
        'Date': dates,
        'Sales': np.random.normal(1000, 200, len(dates)),
        'Revenue': np.random.normal(50000, 10000, len(dates)),
        'Customers': np.random.normal(150, 30, len(dates))
    }
    
    return pd.DataFrame(data)

# Load data
df = generate_sample_data()

# Key metrics
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("💰 Total Revenue", f"${df['Revenue'].sum():,.0f}")

with col2:
    st.metric("📈 Total Sales", f"{df['Sales'].sum():,.0f}")

with col3:
    st.metric("👥 Total Customers", f"{df['Customers'].sum():,.0f}")

# Simple chart
st.subheader("📈 Revenue Over Time")
st.line_chart(df.set_index('Date')['Revenue'])

# Data table
st.subheader("📋 Raw Data")
st.dataframe(df.head(10), use_container_width=True)

# Footer
st.markdown("---")
st.markdown(f"*Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*") 