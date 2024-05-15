import streamlit as st
from supabase import create_client, Client
import os

# Initialize Supabase client
url = os.environ["SUPABASE_URL"]
key = os.environ["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

# Streamlit UI
st.title("Supabase Magic Link Authentication")

if 'auth_state' not in st.session_state:
    st.session_state.auth_state = None

if st.session_state.auth_state:
    st.success("You are logged in!")
    st.write("Welcome!")
    # Add your authenticated app logic here
else:
    email = st.text_input("Enter your email address")
    if st.button("Send Magic Link"):
        try:
            result = supabase.auth.sign_in(email=email)
            st.success("Magic link sent! Please check your email.")
        except Exception as e:
            st.error(f"Error sending magic link: {e}")

    # Check for authentication token in URL
    token = st.experimental_get_query_params().get("access_token", [None])[0]
    if token:
        try:
            user = supabase.auth.api.get_user(token)
            st.session_state.auth_state = user
            st.experimental_rerun()
        except Exception as e:
            st.error(f"Error verifying token: {e}")

