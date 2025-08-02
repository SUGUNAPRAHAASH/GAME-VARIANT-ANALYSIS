import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timedelta
import time
import sys
import os

# Add error handling for imports
try:
    import streamlit as st
    import pandas as pd
    import plotly.express as px
    import plotly.graph_objects as go
    import numpy as np
    from datetime import datetime, timedelta
    import time
except ImportError as e:
    st.error(f"Import error: {e}")
    st.stop()

# Page configuration
st.set_page_config(
    page_title="Data Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for beautiful styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.5rem 2rem;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    
    .chart-container {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.title("🎛️ Dashboard Controls")
    st.markdown("---")
    
    # Date range selector
    st.subheader("📅 Date Range")
    start_date = st.date_input(
        "Start Date",
        value=datetime.now() - timedelta(days=30),
        max_value=datetime.now()
    )
    end_date = st.date_input(
        "End Date",
        value=datetime.now(),
        max_value=datetime.now()
    )
    
    # Filter options
    st.subheader("🔍 Filters")
    category_filter = st.multiselect(
        "Category",
        ["Technology", "Finance", "Healthcare", "Education", "Retail"],
        default=["Technology", "Finance"]
    )
    
    # Chart type selector
    st.subheader("📈 Chart Type")
    chart_type = st.selectbox(
        "Select Chart Type",
        ["Line Chart", "Bar Chart", "Pie Chart", "Scatter Plot", "Area Chart"]
    )
    
    # Color theme
    st.subheader("🎨 Theme")
    color_theme = st.selectbox(
        "Color Theme",
        ["Default", "Dark", "Light", "Colorful"]
    )

# Main content
st.markdown('<h1 class="main-header">📊 Data Analytics Dashboard</h1>', unsafe_allow_html=True)

# Generate sample data
@st.cache_data
def generate_sample_data():
    np.random.seed(42)
    dates = pd.date_range(start=start_date, end=end_date, freq='D')
    
    data = {
        'Date': dates,
        'Sales': np.random.normal(1000, 200, len(dates)),
        'Revenue': np.random.normal(50000, 10000, len(dates)),
        'Customers': np.random.normal(150, 30, len(dates)),
        'Category': np.random.choice(category_filter, len(dates)),
        'Region': np.random.choice(['North', 'South', 'East', 'West'], len(dates))
    }
    
    return pd.DataFrame(data)

# Load data
df = generate_sample_data()

# Key metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="metric-card">
        <h3>💰 Total Revenue</h3>
        <h2>${:,.0f}</h2>
    </div>
    """.format(df['Revenue'].sum()), unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="metric-card">
        <h3>📈 Total Sales</h3>
        <h2>{:,.0f}</h2>
    </div>
    """.format(df['Sales'].sum()), unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="metric-card">
        <h3>👥 Total Customers</h3>
        <h2>{:,.0f}</h2>
    </div>
    """.format(df['Customers'].sum()), unsafe_allow_html=True)

with col4:
    avg_revenue = df['Revenue'].mean()
    st.markdown("""
    <div class="metric-card">
        <h3>📊 Avg Revenue</h3>
        <h2>${:,.0f}</h2>
    </div>
    """.format(avg_revenue), unsafe_allow_html=True)

# Charts section
st.markdown("---")
st.subheader("📈 Data Visualization")

# Create charts based on selection
if chart_type == "Line Chart":
    fig = px.line(df, x='Date', y='Revenue', 
                   title='Revenue Over Time',
                   color='Category')
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)

elif chart_type == "Bar Chart":
    fig = px.bar(df.groupby('Category')['Revenue'].sum().reset_index(),
                  x='Category', y='Revenue',
                  title='Revenue by Category')
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)

elif chart_type == "Pie Chart":
    fig = px.pie(df.groupby('Category')['Revenue'].sum().reset_index(),
                  values='Revenue', names='Category',
                  title='Revenue Distribution by Category')
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)

elif chart_type == "Scatter Plot":
    fig = px.scatter(df, x='Sales', y='Revenue', 
                     color='Category', size='Customers',
                     title='Sales vs Revenue')
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)

elif chart_type == "Area Chart":
    fig = px.area(df, x='Date', y='Revenue', 
                   color='Category',
                   title='Revenue Area Chart')
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)

# Data table
st.markdown("---")
st.subheader("📋 Raw Data")

# Add search functionality
search_term = st.text_input("🔍 Search data...")

if search_term:
    filtered_df = df[df.apply(lambda x: x.astype(str).str.contains(search_term, case=False).any(), axis=1)]
else:
    filtered_df = df

# Display data with pagination
page_size = st.selectbox("Rows per page:", [10, 25, 50, 100])
total_rows = len(filtered_df)
total_pages = (total_rows + page_size - 1) // page_size

if total_pages > 1:
    page = st.selectbox("Page:", range(1, total_pages + 1))
    start_idx = (page - 1) * page_size
    end_idx = min(start_idx + page_size, total_rows)
    display_df = filtered_df.iloc[start_idx:end_idx]
else:
    display_df = filtered_df

st.dataframe(display_df, use_container_width=True)

# Download functionality
st.markdown("---")
col1, col2 = st.columns(2)

with col1:
    csv = df.to_csv(index=False)
    st.download_button(
        label="📥 Download CSV",
        data=csv,
        file_name=f"dashboard_data_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )

with col2:
    if st.button("🔄 Refresh Data"):
        st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 1rem;'>
    <p>📊 Data Analytics Dashboard | Built with Streamlit</p>
    <p>Last updated: {}</p>
</div>
""".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")), unsafe_allow_html=True) 