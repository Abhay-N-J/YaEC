import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import st_pages as stp
import requests

stp.hide_pages(["manager"])

st.title('Register')

user_type = st.selectbox('User Type', ['Customer', 'Freelancer'])

username = st.text_input('Username')
password = st.text_input('Password', type='password')
email = st.text_input("Email")

first_name = st.text_input('First Name')
last_name = st.text_input('Last Name')
phone_number = st.text_input('Phone Number')
location = st.text_input('Location')

if st.button('Register'):
    data = {
        "user": username,
        "email": email,  
        "passwd": password  
    }

    # Make the HTTP POST request
    response = requests.post("http://user-service:8000/register/", json=data)
    response_json = response.json()

    if "error" in response_json:
        st.error(f'Registration failed: {response_json["error"]}')
    else:
        st.success('Registration Successful!')
        switch_page("login")
