import streamlit as st
import requests
import pandas as pd
from api_config import *

def fetch_data_from_api(api_url, token=''):
    # Set up headers with Authorization token
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    # Make a request to the API
    response = requests.get(api_url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Failed to fetch data. Status code: {response.status_code}")
        return None
        
def get_df(api_url, token): 
    
    api_data = fetch_data_from_api(api_url, token)
    
    api_df = pd.DataFrame(api_data['data'])
    
    return api_df

# filter expense and income df 
def get_expense_income_df(category_df): 
    
    expense_category_df = category_df[category_df['isIncome'] == 0].copy()
    income_category_df = category_df[category_df['isIncome'] == 1].copy()
    
    expense_category_df.drop(['isIncome', 'isOnboarding', 'created_at', 'updated_at', 'userID'], axis=1, inplace=True)
    income_category_df.drop(['isIncome', 'isOnboarding', 'created_at', 'updated_at', 'userID'], axis=1, inplace=True)
    
    return expense_category_df, income_category_df

# preprocess transaction df 
def preprocess_df(transaction_df, expense_category_df, income_category_df): 
     
    transaction_df['amount'] = transaction_df['amount'].astype(float)
    transaction_df['date'] = pd.to_datetime(transaction_df['date'])
    
    new_transaction_df = pd.DataFrame({
        'transaction_type': transaction_df['isIncome'].apply(lambda x: 'Income' if x == 1 else 'Expense'),
        'transaction_amount': transaction_df['amount'],
        'transaction_date': transaction_df['date'],
        'transaction_note': transaction_df['note'],
        'category': transaction_df['categoryID'],  # You might want to map categoryID to actual category names
        'subcategory': transaction_df['expenseType'],  # Assuming expenseType represents subcategory
        'day': transaction_df['date'].dt.day,
        'month': transaction_df['date'].dt.month,
        'year': transaction_df['date'].dt.year
    })
    
    for index, row in new_transaction_df.iterrows():
        if row['transaction_type'] == 'Income':
            category_row: pd.DataFrame = income_category_df[income_category_df['id'] == row['category']]
            if (len(category_row) != 0):
                if category_row['level'].iloc[0] == 1:
                    parentID = category_row['parentID'].iloc[0]
                    new_transaction_df.at[index, 'category'] = income_category_df[income_category_df['id'] == parentID]['name'].iloc[0]
                    new_transaction_df.at[index, 'subcategory'] = category_row['name'].iloc[0]
                else:
                    new_transaction_df.at[index, 'category'] = category_row['name'].iloc[0]
                    new_transaction_df.at[index, 'subcategory'] = category_row['parentID'].iloc[0]
        else:
            category_row = expense_category_df[expense_category_df['id'] == row['category']]
            if category_row['level'].iloc[0] == 1:
                parentID = category_row['parentID'].iloc[0]
                new_transaction_df.at[index, 'category'] = expense_category_df[expense_category_df['id'] == parentID]['name'].iloc[0]
                new_transaction_df.at[index, 'subcategory'] = category_row['name'].iloc[0]
            else:
                new_transaction_df.at[index, 'category'] = category_row['name'].iloc[0]
                new_transaction_df.at[index, 'subcategory'] = category_row['parentID'].iloc[0]
    
    return new_transaction_df

category_df = None
transaction_df = None
expense_df = None
income_df = None
preprocess_transaction_df = None