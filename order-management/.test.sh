#Create Order
curl -X POST "http://localhost:8002/orders/" \
-H "Content-Type: application/json" \
-u user:pass \
-d '{"user_id": "user123", "product_id": "product123", "quantity": 2, "status": "pending"}'

#Get specific order
curl -X GET "http://localhost:8002/orders/{order_id}/" \
-u user:pass \

#Update order
curl -X PUT "http://localhost:8002/orders/{order_id}/" \
-H "Content-Type: application/json" \
-u user:pass \
-d '{"user_id": "user123", "product_id": "product123", "quantity": 3, "status": "shipped"}'

#Get all orders
curl -X GET "http://localhost:8002/orders/"

#Delete order
curl -X DELETE "http://localhost:8002/orders/{order_id}/" \
-H "Content-Type: application/json" \
-u user:pass \


