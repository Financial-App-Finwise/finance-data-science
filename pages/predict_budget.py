from navigation import make_sidebar
import streamlit as st
import pandas as pd 
import numpy as np 
import pickle
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from data.data_handling import *
from data.budget_prediction import *

expense_transactions_df = filter_transactions_df(df, 'Expense')

unique_years = expense_transactions_df["year"].unique()
additional_years = np.arange(unique_years.max() + 1, unique_years.max() + 6)
selectable_years = np.concatenate((unique_years, additional_years))

# get data from query paremter
selected_category = st.query_params['category'].replace("'", "")
selected_month_name = st.query_params['month']

selected_month_number = month_map[selected_month_name]

# new_data = [selected_category, selected_month_number, selected_year]
new_testing_data = pd.DataFrame({
    'category': [selected_category],
    'month': [selected_month_number]
})
# Call preprocess_and_predict function
predicted_amount_original, actual_result = preprocess_and_predict(expense_transactions_df, new_testing_data)
st.write(predicted_amount_original[0][0])

import requests
from api_config import *

requests.post("https://finwise-api-test.up.railway.app/api/predictions", 
              json={"predicted_budget": predicted_amount_original[0][0]}, 
              headers = {"Authorization": f"Bearer {token}"})
