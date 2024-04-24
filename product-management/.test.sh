#Create
curl -X POST "http://localhost:8001/products/" \
    -H "Content-Type: application/json" \
    -u test_admin:adminpassword \
    -d '{"name": "Product 1", "description": "Description of Product 1", "price": 19.99}'

#Get Product
curl -X GET "http://localhost:8001/products/Product%201/"

#Update Product
curl -X PUT "http://localhost:8001/products/Product%202/" \
    -H "Content-Type: application/json" \
    -u test_admin:adminpassword \
    -d '{"name": "Product 2", "description": "Updated Description", "price": 29.99}'
b
#Delete Product
curl -X DELETE "http://localhost:8001/products/Product%202/" \
    -u test_admin:adminpassword

#Get all Products
curl -X GET "http://localhost:8001/products/"
