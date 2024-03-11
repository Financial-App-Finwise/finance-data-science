import pandas as pd 
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
import calendar 
import streamlit as st 

def plot_pattern_over_time(df, x_column_name, y_column_name, title, rgb_color):
    df['month_year'] = df['year'].astype(str) + '-' + df['month'].astype(str)
    
    fig = px.line(df, x=df['month_year'], y=y_column_name, 
                  title=f'{title} Pattern Over Time Series', markers=True, 
                  labels={
                      'month_year': "Time Series",
                      y_column_name: "Amount"
                  },
                  color_discrete_sequence=[rgb_color],
                  
                )  # Change line color to blue
    
    fig.update_layout( 
        margin=dict(l=0, r=0, t=50, b=0),  # Adjust margin to fit the chart
    )
    
    st.plotly_chart(fig, use_container_width=True)
     
def show_transaction_type_pattern_over_time(df, transaction_type):
    # Filter transactions by transaction type
    transactions = df[df['transaction_type'] == transaction_type]

    # Extract year and month from the transaction date
    transactions['year'] = pd.to_datetime(transactions['transaction_date']).dt.year
    transactions['month'] = pd.to_datetime(transactions['transaction_date']).dt.month

    # Group by year and month, and aggregate total amount spent
    transaction_summary_time = transactions.groupby(['year', 'month']).agg(
        total_amount=('transaction_amount', 'sum')
    ).reset_index()

    # Create line plot
    fig = px.line(transaction_summary_time, x='month', y='total_amount', color='year',
                  title=f'{transaction_type} Pattern over Time', markers=True)
    st.write(fig)

def get_truncated_total_amount(monthly_summary_pivot, data_type):
    # Find the highest year in the DataFrame
    highest_year = monthly_summary_pivot['year'].max()

    # Filter the DataFrame to include only rows where the year matches the highest year
    highest_year_data = monthly_summary_pivot[monthly_summary_pivot['year'] == highest_year]

    # Find the highest month among the rows with the highest year
    highest_month = highest_year_data['month'].max()

    # Retrieve the total_balance value corresponding to the highest year and highest month
    total_amount_highest_year_month = round(highest_year_data[highest_year_data['month'] == highest_month][data_type].values[0], 2)

    return total_amount_highest_year_month

def compare_total_balance_percentage(monthly_summary_pivot, data_type):
    # Sort the dataframe by month
    monthly_summary_pivot.sort_values(by='month', inplace=True)
    
    # Get the current month index
    current_month_index = monthly_summary_pivot['month'].idxmax()
    
    # Get the total_balance for this month
    current_total_balance = monthly_summary_pivot.iloc[current_month_index][data_type]
    
    # Get the total_balance for last month
    last_month_index = current_month_index - 1 if current_month_index > 0 else len(monthly_summary_pivot) - 1
    last_total_balance = monthly_summary_pivot.iloc[last_month_index][data_type]
    
    # Calculate the percentage change
    percentage_change = round(((current_total_balance - last_total_balance) / last_total_balance) * 100, 2)
    
    return percentage_change

def filter_last_x_months(monthly_summary_pivot, last_x_month):
    last_x_months_data = monthly_summary_pivot.tail(last_x_month)
    
    return last_x_months_data

def create_income_expense_bar_chart(monthly_summary_pivot, selected_range):
    # Mapping the selected ranges to their corresponding integer values
    range_mapping = {
        "Last Month": 1,
        "Last 3 Months": 3,
        "Last 6 Months": 6,
        "Last 9 Months": 9,
        "Last Year": 12,
    }

    # Retrieve the number of months to filter
    last_x_month = range_mapping[selected_range]
    
    # Filter the data based on the selected range
    last_x_months_data = filter_last_x_months(monthly_summary_pivot, last_x_month)

    # Create a bar chart using Plotly
    fig = go.Figure(data=[
        go.Bar(name='Income', x=last_x_months_data['year'].astype(str) + '-' + last_x_months_data['month'].astype(str), y=last_x_months_data['Income'], marker_color='rgb(10, 189, 227)'),
        go.Bar(name='Expense', x=last_x_months_data['year'].astype(str) + '-' + last_x_months_data['month'].astype(str), y=last_x_months_data['Expense'], marker_color='rgb(238, 83, 83)')
    ])

    # Update the layout
    fig.update_layout(
        barmode='group',
        title='Comparison of Income and Expense',
        legend=dict(title='Type'),
        autosize=True,  # Set autosize to make the chart responsive
        margin=dict(l=0, r=0, t=50, b=0),  # Adjust margin to fit the chart
    )

    # Render the chart using Streamlit
    st.plotly_chart(fig, use_container_width=True)
    
