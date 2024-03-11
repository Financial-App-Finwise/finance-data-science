import pandas as pd 
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import calendar 
import streamlit as st 

def show_top_5_categories_donut_chart(df, year, transaction_type_str):
    # Filter expense transactions for the given year
    expense_transactions_year = df[(df['year'] == year)]

    # Sort the categories based on total amount spent in descending order
    expense_summary_sorted_year = expense_transactions_year.sort_values(by='total_amount', ascending=False)

    # Select the top 5 categories
    top_5_categories_year = expense_summary_sorted_year.head(5)
    
    # Create the donut chart
    fig = go.Figure(data=[go.Pie(labels=top_5_categories_year['category'], 
                                  values=top_5_categories_year['total_amount'], 
                                  hole=0.4,
                                  textinfo='label+percent'
                                  )])
    # Set layout options
    fig.update_layout(title=f'Top 5 {transaction_type_str} Categories in {year}',
                      showlegend=True)

    # Show the chart
    st.write(fig)
    
def show_top_5_categories_over_the_time_series(df, transaction_type_str):
    # Sort the transactions from high to low based on total amount
    transaction_sorted_descending = df.sort_values(by='total_amount', ascending=False)
    
    # find time series 
    unique_months = df['month'].unique()
    
    # Select the top 5 categories
    top_5_categories_month = transaction_sorted_descending.head(5)
    
    # Create the donut chart
    fig = go.Figure(data=[go.Pie(labels=top_5_categories_month['category'], 
                                  values=top_5_categories_month['total_amount'], 
                                  hole=0.4,
                                  textinfo='label+percent'
                                  )])
    # Set layout options
    fig.update_layout(title=f'Top 5 {transaction_type_str} Categories for the available months',
                      showlegend=True)

    # Show the chart
    st.write(fig)
    
def show_top_5_categories_of_the_month(df, year, month, transaction_type_str):
    # Filter expense transactions for the given year
    expense_transactions_year = df[(df['year'] == year) & (df['month'] == month)]

    # Sort the categories based on total amount spent in descending order
    expense_summary_sorted_year = expense_transactions_year.sort_values(by='total_amount', ascending=False)

    # Select the top 5 categories
    top_5_categories_year = expense_summary_sorted_year.head(5)
    
    # Convert month number to month name
    month_name = calendar.month_name[month]
    
    # Create the donut chart
    fig = go.Figure(data=[go.Pie(labels=top_5_categories_year['category'], 
                                  values=top_5_categories_year['total_amount'], 
                                  hole=0.4,
                                  textinfo='label+percent'
                                  )])
    # Set layout options
    fig.update_layout(title=f'Top 5 {transaction_type_str} Categories in {month_name}, {year}',
                      showlegend=False)

    # Show the chart
    st.write(fig)
    
def compare_category_between_years(df, category, year1, year2):
    # Filter the DataFrame for the two specific years and the given category
    df_year1 = df[(df['year'] == year1) & (df['category'] == category)]
    df_year2 = df[(df['year'] == year2) & (df['category'] == category)]

    # Calculate the total amount for the specific category for each year
    total_amount_year1 = df_year1['total_amount'].sum()
    total_amount_year2 = df_year2['total_amount'].sum()

    # Create the Plotly bar chart
    fig = go.Figure(data=[
        go.Bar(name=str(year1), x=[category], y=[total_amount_year1], text=str(year1)),
        go.Bar(name=str(year2), x=[category], y=[total_amount_year2], text=str(year2))
    ])

    # Set layout options
    fig.update_layout(barmode='group', title=f'Comparison of {category} between {year1} and {year2}',
                      xaxis_title='Category', yaxis_title='Total Amount')

    # Show the chart
    st.write(fig)
    
def compare_category_between_months(df, category, year, month1, month2):
    # Filter the DataFrame for the specific year and months, and the given category
    df_month1 = df[(df['year'] == year) & (df['month'] == month1) & (df['category'] == category)]
    df_month2 = df[(df['year'] == year) & (df['month'] == month2) & (df['category'] == category)]

    # Calculate the total amount for the specific category for each month
    total_amount_month1 = df_month1['total_amount'].sum()
    total_amount_month2 = df_month2['total_amount'].sum()

    # Create the Plotly bar chart
    fig = go.Figure(data=[
        go.Bar(name=str(month1), x=[str(month1)], y=[total_amount_month1]),
        go.Bar(name=str(month2), x=[str(month2)], y=[total_amount_month2])
    ])

    # Set layout options
    fig.update_layout(barmode='group', title=f'Comparison of {category} between {month1} and {month2} of {year}',
                      xaxis_title='Month', yaxis_title='Total Amount')

    # Show the chart
    st.write(fig)
    
    
def compare_total_expense_between_years(df, year1, year2):
    # Filter the DataFrame for the specific years
    df_year1 = df[df['year'] == year1]
    df_year2 = df[df['year'] == year2]
    

    
    