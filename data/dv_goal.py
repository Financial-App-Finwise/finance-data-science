import streamlit as st
import requests
import pandas as pd
from api_config import *
from datetime import datetime
from data.dv_transactiontype import *

def calculate_total_contribution_this_month(transaction_goal_df):
    # Convert 'created_at' column to datetime format
    transaction_goal_df['created_at'] = pd.to_datetime(transaction_goal_df['created_at'])
    
    # Extracting current month and year
    current_month = datetime.now().month
    current_year = datetime.now().year

    # Filter transactions for the current month and year
    current_month_transactions = transaction_goal_df[
        (transaction_goal_df['created_at'].dt.month == current_month) &
        (transaction_goal_df['created_at'].dt.year == current_year)
    ]

    # Calculate the total contribution amount for the current month
    total_contribution_this_month = current_month_transactions['ContributionAmount'].sum()

    return total_contribution_this_month

def count_num_goal(goal_filtered_df): 
    num_goals = goal_filtered_df['id'].nunique()
    return num_goals

def calculate_total_contribution(goal_filtered_df):
    # Calculate the total contribution
    total_contribution = goal_filtered_df['currentSave'].sum()
    return total_contribution

def calculate_total_goal_amount(goal_filtered_df): 
    total_goal_amount  = goal_filtered_df['amount'].sum()
    return total_goal_amount

def calculate_total_contribution_this_month(transaction_goal_df):
    # Get current month and year
    current_month = get_current_month()
    current_year = get_current_year()
    
    # Filter transactions for the current month and year
    current_month_transactions = transaction_goal_df[
        (transaction_goal_df['created_at'].dt.month == current_month) &
        (transaction_goal_df['created_at'].dt.year == current_year)
    ]
    
    # Calculate the total contribution for the current month
    total_contribution_this_month = current_month_transactions['ContributionAmount'].sum()
    
    return total_contribution_this_month

def plot_amount_of_money(goal_filtered_df, rgb_color):

    # Make a copy of the DataFrame
    goal_filtered_df_copy = goal_filtered_df.copy()

    # Create a new column by combining 'name' and 'id'
    goal_filtered_df_copy['name_id_combined'] = goal_filtered_df_copy['name'] + ' (' + goal_filtered_df_copy['id'].astype(str) + ')'

    # Create a figure
    fig = go.Figure()

    # Add a trace for the amount of money for each goal (area chart)
    fig.add_trace(go.Scatter(
        x=goal_filtered_df_copy['name_id_combined'],
        y=goal_filtered_df_copy['amount'],
        fill='tozeroy',  # Fill area below the curve
        mode='lines',  # Lines mode without markers
        name='Amount of Money',
        line=dict(color=rgb_color, width=2),
    ))

    # Add a trace for the currentSave values (area chart)
    fig.add_trace(go.Scatter(
        x=goal_filtered_df_copy['name_id_combined'],
        y=goal_filtered_df_copy['currentSave'],
        fill='tozeroy',  # Fill area below the curve
        mode='lines',  # Lines mode without markers
        name='Current Save',
        line=dict(color='green', width=2),  # Change color if needed
    ))

    # Update layout
    fig.update_layout(
        xaxis_title='Goal',
        yaxis_title='Amount of Money / Current Save',
        xaxis_tickangle=-45,  # Rotate x-axis labels for better readability
    )

    # Render the chart
    st.plotly_chart(fig, use_container_width=True)
    
    
def plot_contribution_over_months(transaction_goal_df, selected_goal_id, user_contributed_color):
    # Filter transactions for the selected goal
    goal_transactions = transaction_goal_df[transaction_goal_df['goalID'] == selected_goal_id]

    # Check if there are no transactions for the selected goal
    if goal_transactions.empty:
        st.warning("No data available for the selected goal.")
        return

    # Group transactions by month and sum the contribution amount
    monthly_contributions = goal_transactions.groupby('month')['ContributionAmount'].sum().reset_index()

    # Create a line chart
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=monthly_contributions['month'], y=monthly_contributions['ContributionAmount'], mode='lines+markers', line=dict(color=user_contributed_color), hovertemplate='$%{y:.2f}'))
    fig.update_layout(
        xaxis_title='Month',
        yaxis_title='Contribution Amount',
        xaxis=dict(tickmode='linear'),
    )
    st.plotly_chart(fig, use_container_width=True)
    
def get_contributed_amount(selected_goal_id, goal_filtered_df, transaction_goal_df):
    # Get the start date and end date
    start_date = goal_filtered_df[goal_filtered_df['id'] == selected_goal_id]['startDate'].values[0]
    end_date = goal_filtered_df[goal_filtered_df['id'] == selected_goal_id]['endDate'].values[0]

    # Generate the date range
    def generate_month_year_range(start_date, end_date):
        month_year_range = []
        current_date = pd.Timestamp(start_date)
        end_date = pd.Timestamp(end_date)
        while current_date <= end_date:
            month_year_range.append(current_date.strftime('%Y-%m'))
            current_date += pd.offsets.MonthBegin(1)
        return month_year_range

    month_year_range = generate_month_year_range(start_date, end_date)

    # Merge the transaction and goal data
    merged_df = pd.merge(transaction_goal_df, goal_filtered_df, left_on='goalID', right_on='id', how='left')

    # Filter and process the merged DataFrame
    new_merged_df = merged_df[['id_x', 'transactionID', 'goalID', 'ContributionAmount', 'date', 'startDate', 'endDate', 'transactionCount']]
    new_merged_df = new_merged_df.rename(columns={'id_x': 'id', 'date': 'trans_date'})
    new_merged_df['trans_date'] = pd.to_datetime(new_merged_df['trans_date'])
    new_merged_df['trans_month'] = new_merged_df['trans_date'].dt.month
    new_merged_df['trans_year'] = new_merged_df['trans_date'].dt.year
    new_merged_df['trans_year_month'] = new_merged_df.apply(lambda row: datetime.datetime(row['trans_year'], row['trans_month'], 1).strftime('%Y-%m'), axis=1)

    # Group by year, month, and goalID and sum the ContributionAmount
    monthly_sum = new_merged_df.groupby(['trans_year', 'trans_month', 'goalID'])[['ContributionAmount']].sum().reset_index()
    monthly_sum['trans_year_month'] = monthly_sum['trans_year'].astype(str) + '-' + monthly_sum['trans_month'].astype(str).str.zfill(2)
    monthly_sum.drop(columns=['trans_year', 'trans_month'], inplace=True)

    # Create a DataFrame to store the results
    monthly_contribution_for_selected_goal = goal_filtered_df[goal_filtered_df['id'] == selected_goal_id]['monthlyContribution'].values[0]
    data = {'month_year': month_year_range, 'amount': monthly_contribution_for_selected_goal}
    df = pd.DataFrame(data)

    # Iterate over each value in the 'month_year' column and calculate the contributed amount
    contributed_amounts = []
    for value in df['month_year']:
        has_contributed_amount = monthly_sum[(monthly_sum['trans_year_month'] == value) & (monthly_sum['goalID'] == selected_goal_id)]
        contributed_amount = has_contributed_amount['ContributionAmount'].iloc[0] if not has_contributed_amount.empty else 0
        contributed_amounts.append(contributed_amount)

    # Add the contributed amounts as a new column to the DataFrame
    df['hasContributedAmount'] = contributed_amounts

    return df


def plot_amount_over_time(contributed_amount_df, progress_color, expected_color):
    # Create a Plotly figure
    fig = go.Figure()

    # Add a line trace for 'amount' column
    fig.add_trace(go.Scatter(x=contributed_amount_df['month_year'], y=contributed_amount_df['amount'], mode='lines+markers', name='Total Amount', line=dict(color=expected_color), hovertemplate='$%{y:.2f}'))

    # Add a line trace for 'hasContributedAmount' column
    fig.add_trace(go.Scatter(x=contributed_amount_df['month_year'], y=contributed_amount_df['hasContributedAmount'], mode='lines+markers', name='Contributed Amount', line=dict(color=progress_color), hovertemplate='$%{y:.2f}'))

    # Update layout
    fig.update_layout(
        xaxis_title='Month',
        yaxis_title='Amount'
    )
    
    fig.update_xaxes(
        tickformat='%Y-%m'
    )

    # Render the chart using Plotly
    st.plotly_chart(fig, use_container_width=True)