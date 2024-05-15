import streamlit as st
from supabase import create_client, Client
import os

# Initialize Supabase client
url = os.environ["SUPABASE_URL"]
key = os.environ["SUPABASE_KEY"]

# Initialize the Supabase client
supabase = create_client(
    supabase_url=url,
    supabase_key=key,
)

# Define the login function
def login():
    # Get the user's email address
    email = st.text_input("Email address")

    # Send the user a magic link
    supabase.auth.send_magic_link_email(email)

    # Display a message to the user
    st.write("A magic link has been sent to your email address. Please click on the link to log in.")

# Display the login button
if st.button("Login"):
    login()
