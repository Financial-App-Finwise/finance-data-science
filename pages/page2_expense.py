from navigation import make_sidebar
import pandas as pd 
import numpy as np
import streamlit as st 
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import calendar 
from data.data_handling import *
from data.dv_overview import *
from data.dv_transactiontype import *
from api_config import *
from style.theme import *
import datetime

make_sidebar()

# Get current month and year
current_month = datetime.datetime.now().strftime('%B')  # Full name of the current month
current_year = datetime.datetime.now().year

# Expense 
st.title("My Personal Finance - Expense")

show_transaction_type_pattern_over_time(df, 'Expense', error_rgb_color)

# Filter income transactions
expense_transactions = create_transaction_type_summary_df(df, 'Expense')

# -------------------------------------------------------------------------
# TOP 5 CATEGORY in OVER THE TIME SERIES
st.markdown(f"#### Top 5 expense categories over time series")
show_top_5_categories_over_the_time_series(expense_transactions, 'Expense', error_rgb_colors)

# -------------------------------------------------------------------------
# TOP 5 CATEGORY in A SPECIFIC YEAR
title_top_5_ctg_in_year = st.empty()

selected_year_time_series = datetime.datetime.now().year

title_top_5_ctg_in_year.markdown(f"#### Top 5 expense categories in {selected_year_time_series}")

selected_year_time_series = st.selectbox(
    "Select Year:",
    options=expense_transactions["year"].unique(),
)
title_top_5_ctg_in_year.markdown(f"#### Top 5 expense categories in {selected_year_time_series}")

show_top_5_categories_donut_chart(expense_transactions, selected_year_time_series, 'Expense', error_rgb_colors)

# -------------------------------------------------------------------------
# TOP 5 CATEGORY of A SPECIFIC MONTH in A SPECIFIC YEAR
title_top_5_ctg_m_y = st.empty()
selected_month_name = datetime.datetime.now().strftime('%B')
selected_year = datetime.datetime.now().year
title_top_5_ctg_m_y.markdown(f"#### Top 5 expense categories of {selected_month_name} in {selected_year}")
col1, col2 = st.columns(2)
with col1: 
    selected_month_name = st.selectbox(
    "Select a month",
    list(month_map.keys()), 
    index=list(month_map.keys()).index(current_month)
)
    
with col2: 
    selected_year = st.selectbox(
        "Select year:",
        expense_transactions["year"].unique(),
        index=list(expense_transactions["year"].unique()).index(current_year)
    )
    
title_top_5_ctg_m_y.markdown(f"#### Top 5 expense categories of {selected_month_name} in {selected_year}")
selected_month_number = month_map[selected_month_name]
show_top_5_categories_of_the_month(expense_transactions, selected_year, selected_month_number, 'Expense', error_rgb_colors)

# -------------------------------------------------------------------------
# Comparison of A SPECIFIC CATEGORY between YEAR1 and YEAR2
title_cprs_ctg_y1_y2 = st.empty()

col1, col2, col3 = st.columns(3)
with col1: 
    selected_category_year = st.selectbox(
        "Select a category:",
        expense_transactions["category"].unique(),
    )
    
# Create select boxes in each column
with col2:
    unique_years = expense_transactions["year"].unique()
    if len(unique_years) > 0:  # Check if the sequence is not empty
        max_year = np.max(unique_years)  # Use np.max to handle empty arrays
        filtered_first_years = [year for year in unique_years if year < max_year]
        selected_first_year = st.selectbox(
            "Select first year:",
            filtered_first_years,
            key="first_year" 
        )
    else:
        st.warning("No years found in the dataset.")  
        selected_first_year = None 

with col3:
    # Filter years based on the first selected year
    if selected_first_year is not None:  # Check if selected_first_year is not None
        filtered_second_years = [year for year in expense_transactions["year"].unique() if year > selected_first_year]
    else:
        filtered_second_years = []  # Set an empty list if selected_first_year is None

    selected_second_year = st.selectbox(
        "Select second year:",
        filtered_second_years,
        key="second_year"  # Assign a unique key to the second selectbox
    )
    
# Update the title dynamically based on selected category and years
if selected_category_year is not None and selected_first_year is not None and selected_second_year is not None:
    title_cprs_ctg_y1_y2.markdown(f"#### Comparison of {selected_category_year} between {selected_first_year} and {selected_second_year}")
else:
    title_cprs_ctg_y1_y2.empty()

if selected_first_year is not None and selected_second_year is not None:
    compare_category_between_years(expense_transactions, selected_category_year, np.int32(selected_first_year), np.int32(selected_second_year))
else:
    title_cprs_ctg_y1_y2.markdown(f"#### Comparison of A SPECIFIC CATEGORY between YEAR1 and YEAR2")
    st.warning("You don't have enough data for this insight.")