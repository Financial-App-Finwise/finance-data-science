import pandas as pd 
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
import calendar 
import streamlit as st 
import datetime


def show_top_5_categories_donut_chart(df, year, transaction_type_str, colors):
    
    if df.empty or df['total_amount'].sum() == 0:
        st.warning(f"No {transaction_type_str.lower()} data available.")
        return
    
    # Filter expense transactions for the given year
    expense_transactions_year = df[(df['year'] == year)]
    
    if expense_transactions_year.empty:
        st.write(f"No {transaction_type_str.lower()} data available for {year}.")
        return

    # Sort the categories based on total amount spent in descending order
    expense_summary_sorted_year = expense_transactions_year.sort_values(by='total_amount', ascending=False)

    # Select the top 5 categories
    top_5_categories_year = expense_summary_sorted_year.head(5)
    
    if top_5_categories_year.empty:
        st.write(f"Not enough data available for {transaction_type_str.lower()} categories in {year}.")
        return
    
    # Create the donut chart
    fig = go.Figure(data=[go.Pie(labels=top_5_categories_year['category'], 
                                  values=top_5_categories_year['total_amount'], 
                                  hole=0.4,
                                  textinfo='label+percent', 
                                  marker=dict(colors=colors)
                                  )])
    
    # Set layout options
    fig.update_layout(showlegend=True)
    config = {'displayModeBar': False}
    # Show the chart
    st.plotly_chart(fig, use_container_width=True, config=config)
    
def show_top_5_categories_over_the_time_series(df, transaction_type_str, colors):
    if df.empty or df['total_amount'].sum() == 0:
        st.warning(f"No {transaction_type_str.lower()} data available.")
        return
    
    # Sort the transactions from high to low based on total amount
    transaction_sorted_descending = df.sort_values(by='total_amount', ascending=False)
    
    # find time series 
    unique_months = df['month'].unique()
    
    # Select the top 5 categories
    top_5_categories_month = transaction_sorted_descending.head(5)
    
    if top_5_categories_month.empty:
        st.warning(f"No {transaction_type_str.lower()} data available for the selected time period.")
        return
    
    # Create the donut chart
    fig = go.Figure(data=[go.Pie(labels=top_5_categories_month['category'], 
                                  values=top_5_categories_month['total_amount'], 
                                  hole=0.4,
                                  textinfo='label+percent',
                                  marker=dict(colors=colors)
                                  )])
    # Set layout options
    fig.update_layout(showlegend=True)
    config = {'displayModeBar': False}

    # Show the chart
    st.plotly_chart(fig, use_container_width=True, config=config)
    
def show_top_5_categories_of_the_month(df, year, month, transaction_type_str, colors):
    
    # Filter expense transactions for the given year and month
    expense_transactions_month = df[(df['year'] == year) & (df['month'] == month)]

    # Check if there are any transactions available for the specified month and year
    if expense_transactions_month.empty:
        st.warning(f"No {transaction_type_str.lower()} data available for {calendar.month_name[month]}, {year}.")
        return

    # Sort the categories based on total amount spent in descending order
    expense_summary_sorted_month = expense_transactions_month.sort_values(by='total_amount', ascending=False)

    # Select the top 5 categories
    top_5_categories_month = expense_summary_sorted_month.head(5)
    
    # Create the donut chart
    fig = go.Figure(data=[go.Pie(labels=top_5_categories_month['category'], 
                                  values=top_5_categories_month['total_amount'], 
                                  hole=0.4,
                                  textinfo='label+percent', 
                                  marker=dict(colors=colors)
                                  )])
    # Set layout options
    fig.update_layout(showlegend=False)
    config = {'displayModeBar': False}

    # Show the chart
    st.plotly_chart(fig, use_container_width=True, config=config)
    
def compare_category_between_years(df, category, year1, year2):
    st.markdown(f"#### Comparison of {category} between {year1} and {year2}")
    
    # Filter the DataFrame for the two specific years and the given category
    df_year1 = df[(df['year'] == year1) & (df['category'] == category)]
    df_year2 = df[(df['year'] == year2) & (df['category'] == category)]
    
    if df_year1.empty or df_year2.empty:
        st.warning(f"No data available for the category {category} in {year1} or {year2}.")
        return

    # Calculate the total amount for the specific category for each year
    total_amount_year1 = df_year1['total_amount'].sum()
    total_amount_year2 = df_year2['total_amount'].sum()

    # Create the Plotly bar chart
    fig = go.Figure(data=[
        go.Bar(name=str(year1), x=[category], y=[total_amount_year1], text=str(year1)),
        go.Bar(name=str(year2), x=[category], y=[total_amount_year2], text=str(year2))
    ])

    # Set layout options
    fig.update_layout(barmode='group',
                      xaxis_title='Category', yaxis_title='Total Amount')
    config = {'displayModeBar': False}

    # Show the chart
    st.plotly_chart(fig, use_container_width=True, config=config)
    
def compare_category_between_months(df, category, year, month1, month2):
    st.markdown(f"#### Comparison of {category} between {month1} and {month2} of {year}")
    # Filter the DataFrame for the specific year and months, and the given category
    df_month1 = df[(df['year'] == year) & (df['month'] == month1) & (df['category'] == category)]
    df_month2 = df[(df['year'] == year) & (df['month'] == month2) & (df['category'] == category)]
    
    if df_month1.empty or df_month2.empty:
        st.warning(f"No data available for the category {category} in {month1} or {month2}.")
        return

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
    config = {'displayModeBar': False}

    # Show the chart
    st.plotly_chart(fig, use_container_width=True, config=config)
    
    
def compare_total_expense_between_years(df, year1, year2):
    # Filter the DataFrame for the specific years
    df_year1 = df[df['year'] == year1]
    df_year2 = df[df['year'] == year2]

def get_current_month():
    # Get the current date
    current_date = datetime.datetime.now()
    # Extract the month from the current date
    current_month = current_date.month
    return current_month

def get_current_year():
    # Get the current date
    current_date = datetime.datetime.now()
    # Extract the year from the current date
    current_year = current_date.year
    return current_year

    
    