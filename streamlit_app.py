import streamlit as st
import os
import requests
from supabase import create_client, Client

# Fetch Supabase URL and key from environment variables
supabase_url = os.getenv('SUPABASE_URL')
supabase_key = os.getenv('SUPABASE_KEY')

# Initialize Supabase client
supabase_client: Client = create_client(supabase_url, supabase_key)

def create_user(email, password):
    endpoint = f'{supabase_url}/auth/v1/signup'
    data = {
        'email': email,
        'password': password
    }
    response = requests.post(endpoint, json=data)
    return response.json()

def login_user(email, password):
    endpoint = f'{supabase_url}/auth/v1/token'
    data = {
        'email': email,
        'password': password
    }
    response = requests.post(endpoint, json=data)
    return response.json()

def main():
    # Streamlit app
    st.title('User Authentication')
    
    # Signup section
    st.header('Signup')
    signup_email = st.text_input('Signup Email')
    signup_password = st.text_input('Signup Password', type='password')
    
    if st.button('Signup'):
        signup_response = create_user(signup_email, signup_password)
        st.write(signup_response)
    
    # Login section
    st.header('Login')
    login_email = st.text_input('Login Email')
    login_password = st.text_input('Login Password', type='password')
    
    if st.button('Login'):
        login_response = login_user(login_email, login_password)
        st.write(login_response)

if __name__ == '__main__':
    main()
