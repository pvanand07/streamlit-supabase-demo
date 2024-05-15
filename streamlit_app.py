import streamlit as st
import os
import requests
from supabase import create_client, Client
from urllib.parse import urlencode

# Fetch Supabase URL and key from environment variables
supabase_url = os.getenv('SUPABASE_URL')
supabase_key = os.getenv('SUPABASE_KEY')

# Initialize Supabase client
supabase_client: Client = create_client(supabase_url, supabase_key)

def create_user(email, password):
    endpoint = f'{supabase_url}/auth/v1/signup'
    headers = {
        'apikey': supabase_key,
        'Content-Type': 'application/json'
    }
    data = {
        'email': email,
        'password': password
    }
    response = requests.post(endpoint, headers=headers, json=data)
    return response.json()

def login_user(email, password):
    endpoint = f'{supabase_url}/auth/v1/token'
    headers = {
        'apikey': supabase_key,
        'Content-Type': 'application/json'
    }
    data = {
        'email': email,
        'password': password
    }
    response = requests.post(endpoint, headers=headers, json=data)
    return response.json()

def get_google_auth_url():
    params = {
        'provider': 'google',
        'redirect_to': 'http://localhost:8501'  # Redirect back to your Streamlit app
    }
    query_string = urlencode(params)
    return f'{supabase_url}/auth/v1/authorize?{query_string}'

def exchange_code_for_token(code):
    endpoint = f'{supabase_url}/auth/v1/token?grant_type=authorization_code'
    headers = {
        'Content-Type': 'application/json',
        'apikey': supabase_key
    }
    data = {
        'code': code,
        'redirect_uri': 'http://localhost:8501'
    }
    response = requests.post(endpoint, headers=headers, json=data)
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
    
    # Google OAuth section
    st.header('Google OAuth')
    if st.button('Login with Google'):
        auth_url = get_google_auth_url()
        st.write(f"[Click here to authenticate with Google]({auth_url})")
    
    # Handling the OAuth response
    if 'code' in st.experimental_get_query_params():
        code = st.experimental_get_query_params()['code'][0]
        token_response = exchange_code_for_token(code)
        st.write(token_response)

if __name__ == '__main__':
    main()
