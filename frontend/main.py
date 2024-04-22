import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import st_pages as stp

st.title('Home')

stp.hide_pages(["manager"])

st.subheader("Login :")
if st.button('Login'):
    st.write('Redirecting to Login page...')
    switch_page("login")

st.subheader("Register :")
if st.button('Register'):
    st.write('Redirecting to Login page...')
    switch_page("register")