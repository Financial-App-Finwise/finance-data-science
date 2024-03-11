import streamlit as st
from time import sleep
from navigation import make_sidebar
import requests

make_sidebar()

st.title("Welcome to FinWise")

st.write("Please log in to continue (username `test`, password `test`).")

username = st.text_input("Username")
password = st.text_input("Password", type="password")

# if st.button("Log in", type="primary"):
#     data = {
#         "username": username,
#         "password": password
#     }
    
#     # Send a POST request to the login API endpoint
#     response = requests.post("https://finwise-api-test.up.railway.app/api/auth/login", json=data)
    
#     st.write(response.status_code)
    
#     # Check if the request was successful (status code 200)
#     if response.status_code == 200:
#         st.session_state.logged_in = True
#         st.success("Logged in successfully!")
#         sleep(0.5)
#         st.switch_page("pages/page1_overview.py")
#     else:
#         st.error("Incorrect username or password")
        
if st.button("Log in", type="primary"):
    if username == 'test' and password == 'test':
        st.session_state.logged_in = True
        st.success("Logged in successfully!")
        sleep(0.5)
        st.switch_page("pages/page1_overview.py")
    else:
        st.error("Incorrect username or password")