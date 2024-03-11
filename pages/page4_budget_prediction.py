from navigation import make_sidebar
import streamlit as st
import pandas as pd 
import numpy as np 
import pickle
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from data.data_handling import *
from data.budget_prediction import *

make_sidebar()

expense_transactions_df = filter_transactions_df(df, 'Expense')

unique_years = expense_transactions_df["year"].unique()
additional_years = np.arange(unique_years.max() + 1, unique_years.max() + 6)
selectable_years = np.concatenate((unique_years, additional_years))

st.write(expense_transactions_df)
# Streamlit app
st.title('Budget Prediction App')

col1, col2 = st.columns(2)

with col1: 
    selected_category = st.selectbox(
        "Select a category:",
        expense_transactions_df["category"].unique(),
    )
    
with col2: 
    selected_month_name = st.selectbox(
    "Select a month",
    list(month_map.keys())
)
selected_month_number = month_map[selected_month_name]

# new_data = [selected_category, selected_month_number, selected_year]
new_testing_data = pd.DataFrame({
    'category': [selected_category],
    'month': [selected_month_number]
})
# Call preprocess_and_predict function
predicted_amount_original, actual_result = preprocess_and_predict(expense_transactions_df, new_testing_data)

# Display predicted amount
st.write(f"Predicted amount: {predicted_amount_original}")
# st.write(f"Actual amount: {actual_result}")







