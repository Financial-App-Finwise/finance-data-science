import streamlit as st
from time import sleep
from navigation import make_sidebar
import requests
import api_config

make_sidebar()
st.session_state.logged_in = True
# st.success("Logged in successfully!")
# sleep(0.5)
token = st.query_params['token']

# -----------------------------------------------------------------------------------
import data.preprocessed_data_v2 as pre

pre.category_df = pre.get_df(api_config.categories_api_url, token)
pre.transaction_df = pre.convert_json_to_df(api_config.transaction_api_url, token)
pre.goal_api_df = pre.convert_json_to_df(api_config.goal_api_url, token)
pre.expense_df, income_df = pre.get_expense_income_df(pre.category_df)
pre.preprocess_transaction_df = pre.transaction_df.copy()
pre.preprocess_transaction_df = pre.preprocess_df(pre.preprocess_transaction_df)

# ---------------------------------------------------------------------------------
import data.data_handling as handler
handler.df = handler.handle_missing_values(pre.preprocess_transaction_df)
handler.df = handler.handle_duplicates(handler.df)

# Sort column
sort_columns = ['year', 'month', 'day']
df = handler.sort_dataframe(handler.df, sort_columns)

st.switch_page("pages/page1_overview.py")