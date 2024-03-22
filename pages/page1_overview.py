from navigation import make_sidebar
import requests
import streamlit as st
import pandas as pd 
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timedelta
from data.data_handling import *
from data.dv_overview import *
from data.dv_transactiontype import *
from api_config import *
from style.theme import *
import altair as alt

make_sidebar()

# -----------------------------------------------------------------
# DATA SECTION
# Generate monthly summary pivot table
monthly_summary_pivot = generate_monthly_summary_pivot(df)
income_transactions = create_transaction_type_summary_df(df, 'Income')

total_balance = get_truncated_total_amount(monthly_summary_pivot, 'total_balance')
total_income = get_truncated_total_amount(monthly_summary_pivot, 'Income')
total_expense = get_truncated_total_amount(monthly_summary_pivot, 'Expense')

total_balance_percentage_comparison = compare_total_balance_percentage(monthly_summary_pivot, 'total_balance')
total_income_percentage_comparison = compare_total_balance_percentage(monthly_summary_pivot, 'Income')
total_expense_percentage_comparison = compare_total_balance_percentage(monthly_summary_pivot, 'Expense')

# Range mapping
range_mapping = {
    "Last 6 Months": 6,
    "Last 9 Months": 9,
    "Last Year": 12,
}
# -----------------------------------------------------------------

# -----------------------------------------------------------------
# Top Content
st.title("My Personal Finance Overview")
col1, col2, col3 = st.columns(3)
col1.metric("Balance", f'${total_balance}', f"{total_balance_percentage_comparison}")
col2.metric("Income", f'${total_income}', f"{total_income_percentage_comparison}")
col3.metric("Expense", f'${total_expense}', f"{total_expense_percentage_comparison}")

# End of Top Content
# -----------------------------------------------------------------


# -----------------------------------------------------------------
# My Cashflow Bar Chart
col1, col2 = st.columns([3, 1])

# Apply CSS styling for center alignment
col1.markdown(
    "<div style='display: flex; align-items: center; height: 100%;'>"
    "<h3>My Cashflow</h3>"
    "</div>",
    unsafe_allow_html=True
)

# Show the select box in the second column
with col2:
    selected_range = st.selectbox('Select Time Range', list(range_mapping.keys()))

create_income_expense_bar_chart(monthly_summary_pivot, selected_range)

# End of My Cashflow Bar Chart
# -----------------------------------------------------------------

# -----------------------------------------------------------------
# Income Pattern and Pie chart
plot_pattern_over_time(monthly_summary_pivot, 'year', 'total_balance', 'Total Balance', primary_rgb_color)
plot_pattern_over_time(monthly_summary_pivot, 'year', 'Expense', 'Total Expense', error_rgb_color)
plot_pattern_over_time(monthly_summary_pivot, 'year', 'Income', 'Total Income', success_rgb_color)
