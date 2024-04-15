#Create Order
curl -X POST "http://localhost:8002/orders/" \
-H "Content-Type: application/json" \
-d '{"user_id": "user123", "product_id": "product123", "quantity": 2, "status": "pending"}'


curl -X GET "http://localhost:8002/orders/{order_id}/"

curl -X PUT "http://localhost:8002/orders/{order_id}/" \
-H "Content-Type: application/json" \
-d '{"user_id": "user123", "product_id": "product123", "quantity": 3, "status": "shipped"}'

curl -X GET "http://localhost:8002/orders/"


