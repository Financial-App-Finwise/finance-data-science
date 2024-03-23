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
    
def fetch_all_data_from_api(api_url, token=''):
    # Set up headers with Authorization token
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    # Initialize a list to store all data
    all_data = []
    
    # Make initial request to the API
    response = requests.get(api_url, headers=headers)
    
    if response.status_code == 200:
        # Extract the initial page of data
        data = response.json()
        all_data.extend(data['data'])
        
        # Check if there are additional pages
        while data['links']['next'] is not None:
            # Make a request to the next page
            response = requests.get(data['links']['next'], headers=headers)
            data = response.json()
            all_data.extend(data['data'])
        
        return all_data
    else:
        st.error(f"Failed to fetch data. Status code: {response.status_code}")
        return None


def convert_json_to_df(api_url, token): 
    api_data = fetch_all_data_from_api(api_url, token)
    
    api_df = pd.DataFrame(api_data)
    return api_df

    
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

def get_category_name(row): 
    category_data = row['category']
    if category_data['parentCategory'] is None: 
        return category_data['name']
    else: 
        category_name = get_parent_category_name(category_data['parentCategory'])
        return category_name
    # pass
    # return None

def get_subcategory_name(row):
    category_data = row['category']
    if category_data['parentCategory'] != None: 
         return category_data['name']
    return None

def get_parent_category_name(category_data_id): 
    category_name = category_df[category_df['id'] == category_data_id]['name']
    return category_name


# preprocess transaction df 
def preprocess_df(transaction_df):
    transaction_df['amount'] = transaction_df['amount'].astype(float)
    transaction_df['date'] = pd.to_datetime(transaction_df['date'])
    
    new_transaction_df = pd.DataFrame({
        'transaction_type': transaction_df['isIncome'].apply(lambda x: 'Income' if x == 1 else 'Expense'),
        'transaction_amount': transaction_df['amount'],
        'transaction_date': transaction_df['date'],
        'transaction_note': transaction_df['note'],
        'category': transaction_df.apply(get_category_name, axis = 1),  # You might want to map categoryID to actual category names
        'subcategory': transaction_df.apply(get_subcategory_name, axis=1),  # Assuming expenseType represents subcategory
        'day': transaction_df['date'].dt.day,
        'month': transaction_df['date'].dt.month,
        'year': transaction_df['date'].dt.year
    })
    
    return new_transaction_df

def preprocess_goal_df(goal_df): 
    
    goal_filtered_df = goal_df[['id', 'name', 'amount', 'currentSave', 'remainingSave', 'setDate', 
             'startDate', 'endDate', 'monthlyContribution', 'transactionCount']]
    
    goal_filtered_df['startDate'] = pd.to_datetime(goal_filtered_df['startDate'])
    goal_filtered_df['endDate'] = pd.to_datetime(goal_filtered_df['endDate'])
    goal_filtered_df['name_id'] = goal_filtered_df['name'] + '_' + goal_filtered_df['id'].astype(str)

    return goal_filtered_df

def preprocess_goal_transaction_df(transaction_goal_df): 
    transaction_goal_df['created_at'] = pd.to_datetime(transaction_goal_df['created_at'])
    transaction_goal_df['updated_at'] = pd.to_datetime(transaction_goal_df['updated_at'])
    transaction_goal_df['date'] = transaction_goal_df['created_at'].dt.date
    transaction_goal_df['month'] = transaction_goal_df['created_at'].dt.month
    transaction_goal_df['year'] = transaction_goal_df['created_at'].dt.year
    
    return transaction_goal_df

category_df = None
transaction_df = None
goal_api_df = None
expense_df = None
income_df = None
preprocess_transaction_df = None
