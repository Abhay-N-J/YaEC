# Register 
curl -X POST "http://localhost:8000/register/" \
     -H "Content-Type: application/json" \
     -d '{"user": "test_user", "email": "test@example.com", "passwd": "testpassword"}'

#Login
curl -X POST "http://localhost:8000/login/" \
     -H "Content-Type: application/json" \
     -d '{"user": "test_user", "passwd": "testpassword"}'

#Update 
#Erroneous handle
curl -X PUT "http://localhost:8000/profile/{user_id}/" \
     -H "Content-Type: application/json" \
     -d '{"email": "updated_email@example.com"}'
