import pandas as pd 
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import calendar 
import streamlit as st 
from data.preprocessed_data_v2 import *

@st.cache_data
def load_data(path: str): 
    data = pd.read_csv(path)
    
    return data

def cleaned_data(df): 
    if 'transaction_date' in df.columns: 
        df['transaction_date'] = pd.to_datetime(df['transaction_date'])
        
    return df
    
def handle_missing_values(df): 
    # Fill missing values in numeric columns with the mean
    numeric_cols = df.select_dtypes(include='number').columns
    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())

    # Fill missing values in categorical columns with the mode
    categorical_cols = df.select_dtypes(include='object').columns
    df[categorical_cols] = df[categorical_cols].fillna(df[categorical_cols].mode().iloc[0])
    
    return df

def handle_duplicates(df):
    # Count the number of duplicated rows
    num_duplicated_rows = df.duplicated().sum()
    # print(num_duplicated_rows)

    if num_duplicated_rows > 0:
        # Remove duplicated rows
        df.drop_duplicates(inplace=True)
        print(f"Removed {num_duplicated_rows} duplicated row(s).")
    else:
        print("No duplicated rows found.")

    return df

def add_date_columns(df, date_column):
    """
    This function adds new columns for day, month, and year based on a given date column.
    """
    try:
        # Convert the date column to datetime format
        df[date_column] = pd.to_datetime(df[date_column])

        # Add new columns for day, month, and year
        df['day'] = df[date_column].dt.day
        df['month'] = df[date_column].dt.month
        df['year'] = df[date_column].dt.year

    except ValueError as e:
        print(f"Error: {e}. Failed to convert '{date_column}' to datetime.")

    return df

def sort_dataframe(df, columns):
    """
    This function sorts a DataFrame by the specified columns in ascending order.
    """
    try:
        df.sort_values(by=columns, ascending=True, inplace=True)
        df.reset_index(drop=True, inplace=True)
        print("DataFrame sorted successfully.")
    except KeyError as e:
        print(f"Error: {e}. One or more columns specified for sorting do not exist.")

    return df

def convert_to_month_name(month):
    """
    This function converts numeric month values to their respective month names.
    """
    month_names = {
        1: 'January',
        2: 'February',
        3: 'March',
        4: 'April',
        5: 'May',
        6: 'June',
        7: 'July',
        8: 'August',
        9: 'September',
        10: 'October',
        11: 'November',
        12: 'December'
    }

    return month_names.get(month, 'Invalid Month')

def generate_monthly_summary_pivot(df):
    """
    This function generates a monthly summary pivot table from the input DataFrame.
    """
    # Group by year, month, and transaction_type, calculate total_amount
    monthly_summary_pivot = df.groupby(['year', 'month', 'transaction_type']) \
        .agg(total_amount=('transaction_amount', 'sum')) \
        .pivot_table(index=['year', 'month'], columns='transaction_type', values='total_amount', fill_value=0) \
        .reset_index()

    # Rename 'transaction_type' column to 'id'
    monthly_summary_pivot.rename(columns={'transaction_type': 'id'}, inplace=True)

    # Calculate total balance for each month
    monthly_summary_pivot['net_balance'] = monthly_summary_pivot['Income'] - monthly_summary_pivot['Expense']

    # Calculate cumulative total balance starting from the first month
    monthly_summary_pivot['total_balance'] = monthly_summary_pivot['net_balance'].cumsum()

    return monthly_summary_pivot


# --------------------------------------------------------------------------------
# Create Table for each transaction Type
def create_transaction_type_summary_df(df, transaction_type): 
    # Filter transactions by transaction_type
    transaction_type_transactions = df[df['transaction_type'] == transaction_type]

    # Check if there are any transactions of the specified transaction_type
    if transaction_type_transactions.empty:
        print(f"No transactions found for transaction type '{transaction_type}'.")
        return None

    # Group by month and category, then aggregate total amount and count
    monthly_transaction_type_summary = transaction_type_transactions.groupby(['year', 'month', 'category']).agg(
        total_amount=('transaction_amount', 'sum'),
    ).reset_index()
    
    return monthly_transaction_type_summary 

def filter_transactions_df(df, transaction_type):
    
    filtered_df = df[df['transaction_type'] == transaction_type]
    return filtered_df

month_map = {
    'January': 1,
    'February': 2,
    'March': 3,
    'April': 4,
    'May': 5,
    'June': 6,
    'July': 7,
    'August': 8,
    'September': 9,
    'October': 10,
    'November': 11,
    'December': 12
}

# df = load_data("transactions_v2.csv")
# df = cleaned_data(preprocess_df)
df = handle_missing_values(preprocess_transaction_df)
df = handle_duplicates(df)
# df = add_date_columns(preprocess_df, "transaction_date")

# Sort column
sort_columns = ['year', 'month', 'day']
df = sort_dataframe(df, sort_columns)


