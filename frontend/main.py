import streamlit as st
import requests

services=["yaec-product-management-1","yaec-order-management-1","yaec-user-management-1","yaec-review-management-1"]

def fetch_data(service):
    response = requests.get(f"http://{service}:8000/")
    if response.status_code == 200:
        print(response)
        return response.json()
    else:
        return None

def main():
    st.title("FastAPI and Streamlit Integration")

    for service in services:
        data=fetch_data(service)
        st.write(data)

if __name__ == "__main__":
    main()
