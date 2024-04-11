import streamlit as st
import pandas as pd
import requests

services=["yaec-main-product-management-1","yaec-main-order-management-1","yaec-main-user-management-1","yaec-main-review-management-1"]

def fetch_data(service):
    response = requests.get(f"http://{service}:8000/")
    if response.status_code == 200:
        print(response)
        return response.json()
    else:
        return None

services_dict = {
    "Product Management": "yaec-main-product-management-1",
    "Order Management": "yaec-main-order-management-1",
    "User Management": "yaec-main-user-management-1",
    "Review Management": "yaec-main-review-management-1"
}

def register():
    st.title('Register')

    user_type = st.selectbox('User Type', ['Customer', 'Freelancer'])

    username = st.text_input('Username')
    password = st.text_input('Password', type='password')

    first_name = st.text_input('First Name')
    last_name = st.text_input('Last Name')
    phone_number = st.text_input('Phone Number')
    location = st.text_input('Location')

    if st.button('Register'):
        st.success('Registration Successful!')

    
def login():
    st.title('Login')

    username = st.text_input('Username')
    password = st.text_input('Password', type='password')

    if st.button('Login'):
        if username == "your_username" and password == "your_password":
            st.success('Login Successful!')
        else:
            st.error('Invalid username or password')

def home():
    st.title('Home')
        
    if st.button('Login'):
        st.write('Redirecting to Login page...')

    if st.button('Register'):
        st.write('Redirecting to Register page...')

def manage_profile():
    st.title('User Profile Management')

    user_data = {
        'username': 'JohnDoe',
        'password': 'Password',
        'email': 'johndoe@example.com',
        'first_name': 'John',
        'last_name': 'Doe',
        'phone_number': '+1234567890',
        'location': 'New York, USA'
    }

    st.write(f"Username: {user_data['username']}")
    st.write(f"Email: {user_data['email']}")
    st.write(f"First Name: {user_data['first_name']}")
    st.write(f"Last Name: {user_data['last_name']}")
    st.write(f"Phone Number: {user_data['phone_number']}")
    st.write(f"Location: {user_data['location']}")

    st.write('---')

    st.subheader('Update Profile')
    new_username = st.text_input('New Username', value=user_data['username'])
    new_password = st.text_input('New Password')
    new_email = st.text_input('New Email', value=user_data['email'])
    new_first_name = st.text_input('New First Name', value=user_data['first_name'])
    new_last_name = st.text_input('New Last Name', value=user_data['last_name'])
    new_phone_number = st.text_input('New Phone Number', value=user_data['phone_number'])
    new_location = st.text_input('New Location', value=user_data['location'])

    if st.button('Update Profile'):
        updated_data = {
            'username' : new_username,
            'password' : new_password,
            'email': new_email,
            'first_name': new_first_name,
            'last_name': new_last_name,
            'phone_number': new_phone_number,
            'location': new_location
        }
        st.success('Profile updated successfully!')


products_data = {
    'Product ID': [101, 102, 103],
    'Product Name': ['Product A', 'Product B', 'Product C'],
    'Price': [10.99, 20.49, 15.99],
    'Stock': [100, 50, 75]
}
products_df = pd.DataFrame(products_data)



orders_data = {
    'Order ID': [1, 2, 3],
    'Product ID': [101, 102, 103],
    'Quantity': [2, 1, 3],
    'Status': ['Shipped', 'Processing', 'Delivered']
}
orders_df = pd.DataFrame(orders_data)


# OPTIONAL
reviews_data = {
    'Product ID': [101, 102, 103],
    'User': ['User1', 'User2', 'User3'],
    'Rating': [4.5, 3.8, 5.0],
    'Review': ['Great product!', 'Good quality.', 'Highly recommend.']
}
reviews_df = pd.DataFrame(reviews_data)


def product_management():
    st.title('Product Management')

    action = st.sidebar.selectbox('Select Action', ['Add Product', 'Edit Product', 'Delete Product'])

    if action == 'Add Product':
        add_product()
    elif action == 'Edit Product':
        edit_product()
    elif action == 'Delete Product':
        delete_product()

def add_product():
    st.header('Add Product')
    product_name = st.text_input('Product Name')
    price = st.number_input('Price', step=0.01)
    stock = st.number_input('Stock', step=1)

    if st.button('Add'):
        st.success(f'Product "{product_name}" added successfully!')

def edit_product():
    st.header('Edit Product')
    product_id = st.selectbox('Select Product ID to Edit', products_df['Product ID'].tolist())
    product_name = st.text_input('Product Name', value=products_df.loc[products_df['Product ID'] == product_id, 'Product Name'].iloc[0])
    price = st.number_input('Price', value=products_df.loc[products_df['Product ID'] == product_id, 'Price'].iloc[0], step=0.01)
    stock = st.number_input('Stock', value=products_df.loc[products_df['Product ID'] == product_id, 'Stock'].iloc[0], step=1)

    if st.button('Update'):
        st.success(f'Product with ID {product_id} updated successfully!')

def delete_product():
    st.header('Delete Product')
    product_id = st.selectbox('Select Product ID to Delete', products_df['Product ID'].tolist())

    if st.button('Delete'):
        st.success(f'Product with ID {product_id} deleted successfully!')

def product_user_view():
    st.title('Product User View')

    search_term = st.text_input('Search Products')

    filtered_products = products_df[products_df['Product Name'].str.contains(search_term, case=False)]

    st.write('## Products')
    st.table(filtered_products)
    
def order_management():
    st.subheader('Order Management')
    action = st.sidebar.selectbox('Select Action', ['View Order History', 'Track Orders', 'Manage Orders'])

    if action == 'View Order History':
        view_order_history()
    elif action == 'Track Orders':
        track_orders()
    elif action == 'Manage Orders':
        manage_orders()
    
def view_order_history():
    st.header('Order History')
    st.table(orders_df)

def track_orders():
    st.header('Track Orders')
    order_id = st.text_input('Enter Order ID')

    if st.button('Track'):
        st.write(f'Tracking order with ID {order_id}')
        #should fetch order status and display that

def manage_orders():
    st.header('Manage Orders')
    order_id = st.selectbox('Select Order ID to Manage', orders_df['Order ID'].tolist())
    new_status = st.selectbox('New Status', ['Shipped', 'Processing', 'Delivered'])

    if st.button('Update Status'):
        st.success(f'Order with ID {order_id} updated to {new_status}')

def review_management():
    st.title('Review Management')

    product_id = st.selectbox('Select Product ID', products_df['Product ID'].tolist())
    user_review = st.text_area('Write Your Review')
    user_rating = st.slider('Rating', 0.0, 5.0, 0.0)

    if st.button('Submit Review'):
        st.success('Review submitted successfully!')

def manager():
    st.sidebar.title('Navigation')
    page = st.sidebar.radio('Go to', ['Profile Management','Product Management', 'Product User View', 'Order Management', 'Review Management'])

    if page == 'Profile Management':
        manage_profile()
    elif page == 'Product Management':
        product_management()
    elif page == 'Product User View':
        product_user_view()
    elif page == 'Order Management':
        order_management()
    elif page == 'Review Management':
        review_management()


def main():
    manager()

if __name__ == "__main__":
    main()
