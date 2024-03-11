import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score, classification_report, mean_absolute_percentage_error
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import MinMaxScaler

from data.data_handling import *

def encode_categorical_variables(df, columns):
    """
    Encode categorical variables using LabelEncoder.
    """
    encoded_df = df.copy()  # Create a copy of the original DataFrame

    label_encoder = LabelEncoder()  # Initialize LabelEncoder

    for col in columns:
        encoded_df[col + '_encoded'] = label_encoder.fit_transform(encoded_df[col])  # Add new encoded column to DataFrame

    return encoded_df

def scale_feature(df, column_name, feature_range=(-1, 1)):
    """
    Scale a specified feature in the DataFrame using MinMaxScaler.
    """
    scaled_df = df.copy()  # Create a copy of the original DataFrame

    scaler = MinMaxScaler(feature_range=feature_range)  # Initialize MinMaxScaler

    # Reshape the feature array
    feature_values = df[column_name].values.reshape(-1, 1)

    # Scale the feature using MinMaxScaler
    scaled_feature = scaler.fit_transform(feature_values)

    # Add new column with scaled values to DataFrame
    scaled_df[column_name + '_scaled'] = scaled_feature

    return scaled_df

def train_and_predict(X_train, y_train, new_data):
    # Initialize RandomForestRegressor model
    random_model = RandomForestRegressor()

    # Model Training
    random_model.fit(X_train, y_train)

    # Make predictions on new data
    y_pred = random_model.predict(new_data)
    st.write(f'This is y_pred {y_pred}')
    return y_pred

def preprocess_and_predict_with_year(df, new_data):
    categorical_columns = ['category', 'month', 'year']
    column_to_scale = 'transaction_amount'
    
    # Label Encoding
    label_encoder = LabelEncoder()
    for col in categorical_columns:
        df[col + '_encoded'] = label_encoder.fit_transform(df[col])
    
    # Scale Encoding
    feature_range=(-1, 1)
    scaler = MinMaxScaler(feature_range=feature_range)
    feature_values = df[column_to_scale].values.reshape(-1, 1)
    scaled_feature = scaler.fit_transform(feature_values)
    df[column_to_scale + '_scaled'] = scaled_feature
    
    X_train = df[['category_encoded', 'month_encoded', 'year_encoded']]  # Features
    y_train = df['transaction_amount_scaled']
    
    random_model = RandomForestRegressor()
    random_model.fit(X_train, y_train)
     # Extract values from new data
    selected_category = new_data.at[0, 'category']
    selected_month = new_data.at[0, 'month']
    selected_year = new_data.at[0, 'year']
    st.write(new_data)
    st.write(df[df['category'] == selected_category]['category_encoded'].iloc[0])
    
    selected_category_encoded = df[df['category'] == selected_category]['category_encoded'].iloc[0]
    selected_month_encoded = df[df['month'] == selected_month]['month_encoded'].iloc[0]
    selected_year_encoded = df[df['year'] == selected_year]['year_encoded'].iloc[0]

    # Create a DataFrame with the encoded values
    new_data_encoded = pd.DataFrame({
        'category_encoded': [selected_category_encoded],
        'month_encoded': [selected_month_encoded],
        'year_encoded': [selected_year_encoded]
    })
    
    st.write(new_data)
    predicted_amount = random_model.predict(new_data_encoded)
    predicted_amount_original = scaler.inverse_transform(predicted_amount.reshape(-1, 1))
    
    # actual_transaction_amount = df[(df['category'] == selected_category) & 
    #                                (df['month'] == selected_month) & 
    #                                (df['year'] == selected_year)]['transaction_amount'].iloc[0]
    
    actual_transaction_amount = 0
    
    return predicted_amount_original, actual_transaction_amount


def preprocess_and_predict(df, new_data):
    categorical_columns = ['category', 'month']
    column_to_scale = 'transaction_amount'
    
    # Label Encoding
    label_encoder = LabelEncoder()
    for col in categorical_columns:
        df[col + '_encoded'] = label_encoder.fit_transform(df[col])
    
    # Scale Encoding
    feature_range=(-1, 1)
    scaler = MinMaxScaler(feature_range=feature_range)
    feature_values = df[column_to_scale].values.reshape(-1, 1)
    scaled_feature = scaler.fit_transform(feature_values)
    df[column_to_scale + '_scaled'] = scaled_feature
    
    X_train = df[['category_encoded', 'month_encoded']]  # Features
    y_train = df['transaction_amount_scaled']
    
    random_model = RandomForestRegressor()
    random_model.fit(X_train, y_train)
     # Extract values from new data
    selected_category = new_data.at[0, 'category']
    selected_month = new_data.at[0, 'month']
    
    # Retrieve the encoded values for the selected category and month
    selected_category_encoded = df[df['category'] == selected_category]['category_encoded'].iloc[0]
    selected_month_row = df[df['month'] == selected_month]
    
    if not selected_month_row.empty:
        selected_month_encoded = selected_month_row['month_encoded'].iloc[0]
    else:
        # Handle case where selected month does not exist in the DataFrame
        # You can assign a default value or raise an exception based on your requirement
        selected_month_encoded = -1  # Placeholder value
    
    # Create a DataFrame with the encoded values
    new_data_encoded = pd.DataFrame({
        'category_encoded': [selected_category_encoded],
        'month_encoded': [selected_month_encoded]
    })
    
    st.write(new_data)
    predicted_amount = random_model.predict(new_data_encoded)
    predicted_amount_original = scaler.inverse_transform(predicted_amount.reshape(-1, 1))
    
    actual_transaction_amount = 0
    
    return predicted_amount_original, actual_transaction_amount

