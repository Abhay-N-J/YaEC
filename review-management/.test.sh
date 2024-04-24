#Create Review
curl -X POST "http://localhost:8003/reviews/" \
-H "Content-Type: application/json" \
-d '{"user_name": "example_user", "product_name": "example_product", "rating": 4, "comment": "Nice product"}'

#Get specific review
curl -X GET "http://localhost:8003/reviews/{user_name}/{product_name}/"


#Update
curl -X PUT "http://localhost:8003/reviews/{user_name}/{product_name}/" \
-H "Content-Type: application/json" \
-d '{"user_id": "user123", "product_id": "product123", "rating": 5, "comment": "Great product!"}'

#Delete
curl -X DELETE "http://localhost:8003/reviews/{user_name}/{product_name}/"
