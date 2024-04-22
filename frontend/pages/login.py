import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import st_pages as stp
import requests

stp.hide_pages(["manager"])

st.title('Login')

username = st.text_input('Username')
password = st.text_input('Password', type='password')


if st.button('Login'):
    data = {
        "user": username,
        "passwd": password,   
    }

    # Make the HTTP POST request
    response = requests.post("http://user-service:8000/login/", json=data)
    response_json = response.json()

    if "error" in response_json:
        st.error(f'Login failed: {response_json["error"]}')
    else:
        st.success('Login Successful!')
        st.session_state.token = response_json["token"]
        st.session_state.user = username
        switch_page("manager") 
