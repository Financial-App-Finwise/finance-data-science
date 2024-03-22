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

# ---------------------------------------------
import data.preprocessed_data_v2 as pre
from data.preprocessed_data_v2 import *

pre.category_df = get_df(api_config.categories_api_url, token)
pre.transaction_df = get_df(api_config.transaction_api_url, token)
pre.expense_df, income_df = get_expense_income_df(pre.category_df)

pre.preprocess_transaction_df = pre.transaction_df.copy()
pre.preprocess_transaction_df = preprocess_df(pre.preprocess_transaction_df)

st.switch_page("pages/page1_overview.py")