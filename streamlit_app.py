from urllib.parse import parse_qsl

import streamlit as st
import os

from streamlit_url_fragment import get_fragment
from supabase import create_client, Client

def main():
    supabase = get_supabase(
        url=os.environ["SUPABASE_URL"],
        key=os.environ["SUPABASE_KEY"],
    )

    if supabase.auth.get_session():
        # Provide the token from .auth to .postgres
        supabase.auth.session().persist_session()
        token = supabase.auth.get_session().access_token
        supabase.postgrest.auth(token=token)
        
        if st.button("Sign out"):
            supabase.auth.sign_out()
            st.experimental_rerun()

        # We are logged in, let's show our profile
        show_profile(supabase)
    elif login_with_url_fragment(supabase):
        pass  # We got the correct authentication key through #access_token=...
        # This happens when responding to invites, magic links, signup etc.
    elif handle_password_recovery(supabase):
        pass  # We went through the password reset process and should have been logged in
    else:
        if login_form(supabase):
            st.experimental_rerun()

def login_form(supabase: Client):
    email = st.text_input("E-mail")
    password = st.text_input("Password", type="password")
    st.write("Leave password empty to log in with a magic link")

    if st.button("Log in"):
        result = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password or None,
        })
        if result['status_code'] == 200:
            return True
        else:
            st.write("Error", result)

    elif st.button("Sign up"):
        if not password:
            st.error("You need to provide a password to sign up")
        result = supabase.auth.sign_up({
            "email": email,
            "password": password,
        })
        if result['status_code'] == 200:
            st.write("The confirmation link was sent to your e-mail")
        else:
            st.write("Error", result)

    elif st.button("Reset password"):
        result = supabase.auth.reset_password_for_email(email)
        if result['status_code'] == 200:
            st.write("The password reset link was sent to your e-mail")
        else:
            st.write("Error", result)

def login_with_url_fragment(supabase: Client):
    """Handle account activation and magic link login"""
    params = dict(parse_qsl(url_fragment.removeprefix('#')))
    if params.get('type') in ('invite', 'signup', 'magiclink'):
        # We've got redirected here from an invite or a magic link, we should have all the right tokens in params.
        supabase.auth.sign_in_with_token(params.get('refresh_token'))
        return True

def handle_password_recovery(supabase: Client):
    params = dict(parse_qsl(url_fragment.removeprefix('#')))
    if params.get('type') == 'recovery':
        # We've got redirected here from a password reset link
        password = st.text_input("New password")
        if st.button("Save"):
            result = supabase.auth.update_user({
                'access_token': params.get('access_token'),
                'password': password,
            })
            if result['status_code'] == 200:
                reset_fragment()  # Make sure we won't try to reset password again
                supabase.auth.sign_in_with_password({
                    "email": result['email'],
                    "password": password,
                })
            else:
                st.write("Error:", result)
        return True

def show_profile(supabase: Client):
    st.write(f"Hello, {supabase.auth.current_user['email']}!")
    user_id = supabase.auth.current_user['id']
    profiles = supabase.from_('user_profile').select('id', 'bio').eq('id', user_id).execute()
    bio = st.text_area("Say something about yourself:", value=profiles['data'][0]['bio'] if profiles['data'] else '')
    supabase.from_('user_profile').upsert({'bio': bio, 'id': user_id}).execute()

@st.cache(allow_output_mutation=True)
def get_supabase(url, key) -> Client:
    return create_client(url, key)

def reset_fragment():
    params = st.experimental_get_query_params()
    r = params.get('_r', [0])
    try:
        r = int(r[0])
    except (ValueError, TypeError):
        r = 0
    params['_r'] = r + 1
    st.experimental_set_query_params(**params)
    st.experimental_rerun()

# Some preparation before running the main() function
url_fragment = get_fragment()
if url_fragment is None:
    st.spinner("Loading components...")
    st.stop()

main()
