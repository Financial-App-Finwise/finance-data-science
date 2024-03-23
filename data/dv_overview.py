import pandas as pd 
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
import calendar 
import streamlit as st
import datetime 

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
        hovermode="y"
    )
    
    fig.update_xaxes(
        tickformat='%Y-%m'
    )
    
    st.plotly_chart(fig, use_container_width=True)
     
def show_transaction_type_pattern_over_time(df, transaction_type, rgb_color):
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
                  title=f'{transaction_type} Pattern over Time', markers=True, 
                  color_discrete_sequence=[rgb_color],
                  )
    st.plotly_chart(fig, use_container_width=True)
    
def get_current_month_and_year():
    # Get the current date
    current_date = datetime.datetime.now()
    # Extract the year and month from the current date
    current_year = current_date.year
    current_month = current_date.month
    return current_year, current_month

def get_truncated_total_amount(monthly_summary_pivot, data_type):
    # Get the current year and month
    current_year, current_month = get_current_month_and_year()

    # Filter the DataFrame to include only rows where the year matches the current year
    current_year_data = monthly_summary_pivot[monthly_summary_pivot['year'] == current_year]

    # Retrieve the total_balance value corresponding to the current year and month
    total_amount_current_year_month = round(current_year_data[current_year_data['month'] == current_month][data_type].values[0], 2)

    return total_amount_current_year_month

def compare_total_balance_percentage(monthly_summary_pivot, data_type):
    # Get the current year and month
    current_year, current_month = get_current_month_and_year()

    # Filter the DataFrame to include only rows where the year matches the current year
    current_year_data = monthly_summary_pivot[monthly_summary_pivot['year'] == current_year]

    # Retrieve the total_balance value corresponding to the current year and month
    total_amount_current_year_month = round(current_year_data[current_year_data['month'] == current_month][data_type].values[0], 2)

    # Retrieve the total_balance value for the previous month
    previous_month = current_month - 1 if current_month > 1 else 12
    previous_year = current_year if current_month > 1 else current_year - 1
    previous_month_data = monthly_summary_pivot[(monthly_summary_pivot['year'] == previous_year) & (monthly_summary_pivot['month'] == previous_month)]
    
    if previous_month_data.empty:
        return "No data availabe"
    
    total_amount_previous_month = round(previous_month_data[data_type].values[0], 2)

    # Calculate the percentage change
    percentage_change = round(((total_amount_current_year_month - total_amount_previous_month) / abs(total_amount_previous_month)) * 100, 2)

    return f"{percentage_change}% vs last month"

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
    last_x_month = range_mapping.get(selected_range, 0)  # Default to 0 if selected range is not found

    # Filter the data based on the selected range
    last_x_months_data = filter_last_x_months(monthly_summary_pivot, last_x_month)
    
    if last_x_months_data.empty:
        st.write("No data available for the selected range.")
        return

    # Format the 'y' values with a dollar sign
    last_x_months_data['Income'] = last_x_months_data['Income'].apply(lambda x: f"${x:.2f}")
    last_x_months_data['Expense'] = last_x_months_data['Expense'].apply(lambda x: f"${x:.2f}")

    # Create a bar chart using Plotly
    fig = go.Figure(data=[
        go.Bar(name='Income', x=last_x_months_data['year'].astype(str) + '-' + last_x_months_data['month'].astype(str), y=last_x_months_data['Income'], marker_color='rgb(10, 189, 227)', hoverinfo='y', text=last_x_months_data['Income'], textposition='outside'),
        go.Bar(name='Expense', x=last_x_months_data['year'].astype(str) + '-' + last_x_months_data['month'].astype(str), y=last_x_months_data['Expense'], marker_color='rgb(238, 83, 83)', hoverinfo='y', text=last_x_months_data['Expense'], textposition='outside')
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
    
