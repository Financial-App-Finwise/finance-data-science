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
    if transaction_df.empty:
        print("Warning: Input DataFrame is empty. Initializing with zeros.")
        df = pd.DataFrame(columns=['transaction_type', 'transaction_amount', 'transaction_date', 
                                    'transaction_note', 'category', 'subcategory', 'day', 'month', 'year'],
                          dtype={'transaction_amount': float, 'day': int, 'month': int, 'year': int})
        # Fill numerical columns with zeros
        df['transaction_amount'] = 0
        df['day'] = 0
        df['month'] = 0
        df['year'] = 0
        print(df)
        return df
    
    try:
        # Convert 'amount' column to float
        transaction_df['amount'] = transaction_df['amount'].astype(float)
        
        # Convert 'date' column to datetime
        transaction_df['date'] = pd.to_datetime(transaction_df['date'])
        
        # Create new DataFrame with processed columns
        new_transaction_df = pd.DataFrame({
            'transaction_type': transaction_df['isIncome'].apply(lambda x: 'Income' if x == 1 else 'Expense'),
            'transaction_amount': transaction_df['amount'],
            'transaction_date': transaction_df['date'],
            'transaction_note': transaction_df['note'],
            # Assuming get_category_name and get_subcategory_name functions are defined elsewhere
            'category': transaction_df.apply(get_category_name, axis=1),  # You might want to map categoryID to actual category names
            'subcategory': transaction_df.apply(get_subcategory_name, axis=1),  # Assuming expenseType represents subcategory
            'day': transaction_df['date'].dt.day,
            'month': transaction_df['date'].dt.month,
            'year': transaction_df['date'].dt.year
        })
        
    except KeyError as e:
        return None
    
    except Exception as e:
        return None
    
    return new_transaction_df

def preprocess_goal_df(goal_df): 
    if goal_df.empty:
        print("Warning: Input DataFrame is empty. Initializing with default values.")
        # Create an empty DataFrame with desired columns
        goal_filtered_df = pd.DataFrame(columns=['id', 'name', 'amount', 'currentSave', 'remainingSave', 
                                                  'setDate', 'startDate', 'endDate', 'monthlyContribution', 
                                                  'transactionCount', 'name_id'],
                                        dtype={'amount': float, 'currentSave': float, 'remainingSave': float,
                                               'monthlyContribution': float, 'transactionCount': int})
        # Fill numerical columns with zeros
        goal_filtered_df['amount'] = 0.0
        goal_filtered_df['currentSave'] = 0.0
        goal_filtered_df['remainingSave'] = 0.0
        goal_filtered_df['monthlyContribution'] = 0.0
        goal_filtered_df['transactionCount'] = 0
        return goal_filtered_df
    
    try:
        # Filter and select desired columns
        goal_filtered_df = goal_df[['id', 'name', 'amount', 'currentSave', 'remainingSave', 'setDate', 
                                    'startDate', 'endDate', 'monthlyContribution', 'transactionCount']]
        
        # Convert 'startDate' and 'endDate' columns to datetime
        goal_filtered_df['startDate'] = pd.to_datetime(goal_filtered_df['startDate'])
        goal_filtered_df['endDate'] = pd.to_datetime(goal_filtered_df['endDate'])
        
        # Concatenate 'name' and 'id' columns to create 'name_id'
        goal_filtered_df['name_id'] = goal_filtered_df['name'] + '_' + goal_filtered_df['id'].astype(str)
        
    except KeyError as e:
        return None
    
    except Exception as e:
        return None
    
    return goal_filtered_df

def preprocess_goal_transaction_df(transaction_goal_df): 
    if transaction_goal_df.empty:
        # Assign default values to each column
        transaction_goal_df['created_at'] = pd.to_datetime(None)
        transaction_goal_df['updated_at'] = pd.to_datetime(None)
        transaction_goal_df['date'] = None
        transaction_goal_df['month'] = 0
        transaction_goal_df['year'] = 0
        return transaction_goal_df
    
    try:
        # Convert 'created_at' and 'updated_at' columns to datetime
        transaction_goal_df['created_at'] = pd.to_datetime(transaction_goal_df['created_at'])
        transaction_goal_df['updated_at'] = pd.to_datetime(transaction_goal_df['updated_at'])
        
        # Extract date, month, and year from 'created_at' column
        transaction_goal_df['date'] = transaction_goal_df['created_at'].dt.date
        transaction_goal_df['month'] = transaction_goal_df['created_at'].dt.month
        transaction_goal_df['year'] = transaction_goal_df['created_at'].dt.year
        
    except KeyError as e:
        return None
    
    except Exception as e:
        return None
    
    return transaction_goal_df

category_df = None
transaction_df = None
goal_api_df = None
expense_df = None
income_df = None
preprocess_transaction_df = None
