import streamlit as st
import pandas as pd
import requests
from streamlit_extras.switch_page_button import switch_page
import st_pages as stp

stp.hide_pages(["register","manager","main"])

# services=["yaec-product-management-1","yaec-order-management-1","yaec-user-management-1","yaec-review-management-1"]

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

    action = st.selectbox('Select Action', ['Product User View','Add Product', 'Update Product', 'Delete Product'])

    if action == 'Add Product':
        add_product()
    elif action == 'Edit Product':
        edit_product()
    elif action == 'Product User View':
        product_user_view()
    elif action == 'Delete Product':
        delete_product()

def add_product():
    st.header('Add Product')
    product_name = st.text_input('Product Name')
    product_desc = st.text_input('Product Desciption')
    price = st.number_input('Price', step=0.01)

    if st.button('Add'):
        data = {
            "name": product_name,
            "description": product_desc,
            "price": price
        }

        # Make the HTTP POST request
        response = requests.post("http://yaec-product-management-1:8000/products/",
                                 headers={"Content-Type": "application/json"},
                                 auth=(st.session_state.user, st.session_state.token),
                                 json=data)
        response_json = response.json()
        
        if "error" in response_json:
            st.error(f'Failed to add product. Error: {response_json["error"]}')
        else:
            st.success("Product Added Successfully !!!")

def edit_product():
    st.header('Edit Product')
    response = requests.get("http://yaec-product-management-1:8000/products/")
    response_json = response.json()
    products_df = pd.DataFrame(response_json)

    product_id = st.selectbox('Select Product Name to Edit', products_df['name'].tolist())
    new_product_name = st.text_input('Product Name', value=products_df.loc[products_df['name'] == product_id, 'name'].iloc[0])
    new_product_desc = st.text_input('Product Description', value=products_df.loc[products_df['name'] == product_id, 'description'].iloc[0])
    new_price = st.number_input('Price', value=products_df.loc[products_df['name'] == product_id, 'price'].iloc[0], step=0.01)

    if st.button('Update'):
        data = {
                "name": new_product_name,
                "description": new_product_desc,
                "price": new_price
            }

        # Make HTTP PUT request to update product
        update_response = requests.put(f"http://yaec-product-management-1:8000/products/{product_id}/",
                                        headers={"Content-Type": "application/json"},
                                        auth=(st.session_state.user, st.session_state.token),
                                        json=data)
        update_response_json = update_response.json()

        if "error" in update_response_json:
            st.error(f'Failed to Update product. Error: {update_response_json["error"]}')
        else:
            st.success(f'Product with ID {product_id} updated successfully!')

def delete_product():
    st.header('Delete Product')
    response = requests.get("http://yaec-product-management-1:8000/products/")
    response_json = response.json()
    products_df = pd.DataFrame(response_json)

    product_id = st.selectbox('Select Product Name to Edit', products_df['name'].tolist())

    if st.button('Delete'):
        delete_response = requests.delete(f"http://yaec-product-management-1:8000/products/{product_id}/",
                                              auth=(st.session_state.user, st.session_state.token))
        delete_response_json = delete_response.json()

        if "error" in delete_response_json:
            st.error(f'Failed to Delete product. Error: {delete_response_json["error"]}')
        else:
            st.success(f'Product with ID {product_id} deleted successfully!')

def product_user_view():
    st.title('Product User View')
    st.subheader('## Products')

    response = requests.get("http://yaec-product-management-1:8000/products/")
    response_json = response.json()

    if "error" not in response_json:
        # Create a DataFrame from the products
        products_df = pd.DataFrame(response_json)
        st.dataframe(products_df)
    else:
        st.error(f'Failed to show all products. Error: {response_json["error"]}')    
    
def order_management():
    st.title('Order Management')
    action = st.selectbox('Select Action', ['Order History','Create Order', 'Update Order', 'Delete Order'])

    if action == 'Order History':
        order_history()
    elif action == 'Create Order':
        create_order()
    elif action == 'Update Order':
        update_order()
    elif action == 'Delete Order':
        delete_order()
    
def order_history():
    st.header('Order History')
    st.subheader('## Orders')

    response = requests.get("http://yaec-order-management-1:8000/orders/",
                            auth=(st.session_state.user, st.session_state.token))
    response_json = response.json()

    if "error" not in response_json:
        filtered_orders_df = pd.DataFrame(response_json)
        orders_df = filtered_orders_df[filtered_orders_df['user_id'] == st.session_state.user]
        st.dataframe(orders_df)
    else:
        st.error(f'Failed to show all orders. Error: {response_json["error"]}')

def create_order():
    st.header('Create Order')

    response = requests.get("http://yaec-product-management-1:8000/products/")
    response_json = response.json()
    product_names = set(review['product_name'] for review in response_json)

    product_id = st.selectbox("Select Product:", sorted(product_names))
    # product_id = st.text_input('Product ID')

    quantity = st.number_input('Quantity', min_value=1, value=1,step=1)
    status = st.selectbox('Status', ['pending', 'processing', 'shipped'])

    if st.button('Create'):
        data = {
            "user_id": st.session_state.user,
            "product_id": product_id,
            "quantity": quantity,
            "status": status
        }

        # Make the HTTP POST request
        response = requests.post("http://yaec-order-management-1:8000/orders/",
                                 headers={"Content-Type": "application/json"},
                                 auth=(st.session_state.user, st.session_state.token),
                                 json=data)
        response_json = response.json()
        
        if "error" in response_json:
            st.error(f'Failed to Create Order. Error: {response_json["error"]}')
        else:
            st.success("Order Created Successfully !!!")

def update_order():
    st.header('Edit Product')
    response = requests.get("http://yaec-order-management-1:8000/orders/",
                            auth=(st.session_state.user, st.session_state.token))
    response_json = response.json()
    filtered_orders_df = pd.DataFrame(response_json)
    orders_df = filtered_orders_df[filtered_orders_df['user_id'] == st.session_state.user]
    if orders_df.empty:
        st.error("No orders found for the current user.")
    else:
        order_id = st.selectbox('Select Order ID to Edit', orders_df['order_id'].tolist())
        product_id = orders_df.loc[orders_df['order_id'] == order_id, 'product_id'].iloc[0]
        new_quantity = st.number_input('Quantity', value=orders_df.loc[orders_df['order_id'] == order_id, 'quantity'].iloc[0], min_value=1,step=1)
        new_status = st.selectbox('Status', ['pending', 'processing', 'shipped'])

        if st.button('Update'):
            data = {
                "user_id": st.session_state.user,
                "product_id": product_id,
                "quantity": new_quantity,
                "status": new_status
            }

            # Make HTTP PUT request to update product
            update_response = requests.put(f"http://yaec-order-management-1:8000/orders/{order_id}/",
                                            headers={"Content-Type": "application/json"},
                                            auth=(st.session_state.user, st.session_state.token),
                                            json=data)
            update_response_json = update_response.json()

            if "error" in update_response_json:
                st.error(f'Failed to Update Order. Error: {update_response_json["error"]}')
            else:
                st.success(f'Order with ID {order_id} updated successfully!')

def delete_order():
    st.header('Delete Order')
    response = requests.get("http://yaec-order-management-1:8000/orders/",
                            auth=(st.session_state.user, st.session_state.token))
    response_json = response.json()
    filtered_orders_df = pd.DataFrame(response_json)
    orders_df = filtered_orders_df[filtered_orders_df['user_id'] == st.session_state.user]
    if orders_df.empty:
        st.error("No orders found for the current user.")
    else:
        order_id = st.selectbox('Select Order ID to Edit', orders_df['order_id'].tolist())

        if st.button('Delete'):
            delete_response = requests.delete(f"http://yaec-order-management-1:8000/orders/{order_id}/",
                                                auth=(st.session_state.user, st.session_state.token))
            delete_response_json = delete_response.json()

            if "error" in delete_response_json:
                st.error(f'Failed to Delete Order. Error: {delete_response_json["error"]}')
            else:
                st.success(f'Product with ID {order_id} deleted successfully!')

def review_management():
    st.title('Review Management')

    response = requests.get("http://yaec-product-management-1:8000/products/")
    response_json = response.json()
    
    st.subheader("Reviews:")
    product_names = set(review['product_name'] for review in response_json)
    selected_product = st.selectbox("Select Product:", sorted(product_names))
    st.write("---")
    
    st.write("Reviews:")
    for review in response_json:
        if review['product_name'] == selected_product:
            st.write(f"user_name: {review['user_name']}")
            st.write(f"rating: {review['rating']}")
            st.write(f"comment: {review['comment']}")
            st.write("---")
    user_reviews = [review for review in response_json if review['user_name'] == st.session_state.user and review['product_name'] == selected_product]
    if user_reviews:
        user_reviews = user_reviews[0]
        st.subheader("Update Review")
        new_rating = st.slider("Rating", value=int(user_reviews['rating']), min_value=1, max_value=5)
        new_comment = st.text_area("Comment", value=user_reviews['comment'])
        if st.button("Update Review"):
            data = {
                "user_name": st.session_state.user,
                "product_name": selected_product,
                "rating": new_rating,
                "comment": new_comment
            }
            response = requests.put("http://yaec-review-management-1:8000/reviews/{user_name}/{product_name}/",
                                     headers={"Content-Type": "application/json"},
                                     json=data) 
            if "error" in response_json:
                st.error(f'Failed to Update Review. Error: {response_json["error"]}')
            else:
                st.success("Review Updated Successfully !!")
    else:
        st.subheader("Create Review")
        new_rating = st.slider("Rating", min_value=1, max_value=5)
        new_comment = st.text_area("Comment")
        if st.button("Create Review"):
            data = {
                "user_name": st.session_state.user,
                "product_name": selected_product,
                "rating": new_rating,
                "comment": new_comment
            }
            response = requests.post("http://yaec-review-management-1:8000/reviews/",
                                     headers={"Content-Type": "application/json"},
                                     auth=(st.session_state.user, st.session_state.token),
                                     json=data) 
            if "error" in response_json:
                st.error(f'Failed to Create Review. Error: {response_json["error"]}')
            else:
                st.success("Review Created Successfully !!!")

st.sidebar.title('Navigation')
page = st.sidebar.selectbox('Go to', ['Product Management', 'Order Management', 'Review Management'])

# if page == 'Profile Management':
#     manage_profile()
if page == 'Product Management':
    product_management()
elif page == 'Order Management':
    order_management()
elif page == 'Review Management':
    review_management()

