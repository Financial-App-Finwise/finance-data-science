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
from data.dv_goal import *
from api_config import *
from style.theme import *
import altair as alt

make_sidebar()

# -----------------------------------------------------------------
# DATA SECTION
goal_filtered_df = preprocess_goal_df(goal_api_df)

transaction_goal_df = convert_json_to_df(transaction_goal_api_url, token)
transaction_goal_df = preprocess_goal_transaction_df(transaction_goal_df)

num_goals = count_num_goal(goal_filtered_df)
total_amount = calculate_total_goal_amount(goal_filtered_df)
total_contribution = calculate_total_contribution(goal_filtered_df)
total_contribution_this_month = calculate_total_contribution_this_month(transaction_goal_df)
# -----------------------------------------------------------------

# -----------------------------------------------------------------
# Top Content
st.title("My Smart Goal Overview")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Goal", f'{num_goals}')
col2.metric("Total Amount", f'${total_amount}')
col3.metric("Total Contribution", f'${total_contribution}')
col4.metric("This Month's Contribution", f'${total_contribution_this_month}')

# End of Top Content
# -----------------------------------------------------------------

# -----------------------------------------------------------------
# Amount of Money and Current Save for Each Goal
plot_amount_of_money(goal_filtered_df, success_rgb_color)
# -----------------------------------------------------------------

# -----------------------------------------------------------------
# USER CONTRIBUTION PATTERN FOR SELECTED GOAL
title_contribution_amount_over_months_for_selected_goal = st.empty()
selected_goal_name = goal_filtered_df['name_id'].values[0]
selected_goal_id = goal_filtered_df[goal_filtered_df['name_id'] == selected_goal_name]['id'].values[0]
selected_goal_name = st.selectbox(
    "Select Name:",
    options=goal_filtered_df["name_id"].unique()
)
title_contribution_amount_over_months_for_selected_goal.markdown(f"#### Your Contribution Pattern for {selected_goal_name}")
selected_goal_id = goal_filtered_df[goal_filtered_df['name_id'] == selected_goal_name]['id'].values[0]

plot_contribution_over_months(transaction_goal_df, selected_goal_id, success_rgb_color)
# -----------------------------------------------------------------

# -----------------------------------------------------------------
# COMPARISON BETWEEN USER CONTRIBUTION & EXPECTED AMOUNT
# CA_VS_EA = contributed amount vs expected amount

# Generate unique keys for the selectbox widgets
selectbox_key = "_selectbox_ca_vs_ea"
title_contributed_amount_vs_expected_amount = st.empty()
selected_goal_name_ca_vs_ea = goal_filtered_df['name_id'].values[0]
selected_goal_id_ca_vs_ea = goal_filtered_df[goal_filtered_df['name_id'] == selected_goal_name_ca_vs_ea]['id'].values[0]
selected_goal_name_ca_vs_ea = st.selectbox(
    "Select Name:",
    options=goal_filtered_df["name_id"].unique(),
    key=selectbox_key
)
title_contributed_amount_vs_expected_amount.markdown(f"#### Your Contributed Amount vs Expected Contributed Amount for {selected_goal_name_ca_vs_ea}")
selected_goal_id_ca_vs_ea = goal_filtered_df[goal_filtered_df['name_id'] == selected_goal_name_ca_vs_ea]['id'].values[0]
contributed_amount_df = get_contributed_amount(selected_goal_id_ca_vs_ea, goal_filtered_df, transaction_goal_df)
plot_amount_over_time(contributed_amount_df, success_rgb_color, gray_rgb_color)
# -----------------------------------------------------------------

