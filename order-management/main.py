from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from bson import ObjectId
from dotenv import load_dotenv
from uuid import uuid4
from datetime import datetime
import os
import requests

app = FastAPI()
security = HTTPBasic()

class Order(BaseModel):
    user_id: str
    product_id: str
    order_id: str = str(uuid4())
    quantity: int
    status: str
    created_at: datetime = datetime.now()

    
    
# MongoDB connection settings
load_dotenv()
MONGO_URL = os.getenv("MONGO_URI")
DB_NAME = "YaEC"
ORDER_COLLECTION = "Orders"


@app.on_event("startup")
async def startup_db_client():
    app.mongodb_client = AsyncIOMotorClient(MONGO_URL)
    app.mongodb = app.mongodb_client[DB_NAME][ORDER_COLLECTION]

@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()

async def authenticate_user(credentials: HTTPBasicCredentials = Depends(security)):
    user = {
        "user": credentials.username,
        "passwd": credentials.password
    }
    response = requests.post("http://yaec-user-management-1:8000/login/", json=user)
    res = response.json()
    if res["message"] == "Login successful":
        return user
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")

# async def check_admin(user: dict = Depends(authenticate_user)):     
#     response = requests.post("http://yaec-user-management-1:8000/check_admin/", json=user)
#     res = response.json()
#     if res["message"] == "Login successful":
#         return True
#     else:
#         raise HTTPException(status_code=403, detail="User is not an admin")


@app.post("/orders/")
async def create_order(order: Order):
    order.order_id += order.user_id
    order_doc = order.dict()
    result = await app.mongodb.insert_one(order_doc)
    return {"id": str(result.inserted_id)}

@app.get("/orders/{order_id}/")
async def read_order(order_id: str):
    order = await app.mongodb.find_one({"order_id": order_id})
    if order:
        del order["_id"]
        return order
    raise HTTPException(status_code=404, detail="Order not found")

@app.put("/orders/{order_id}/")
async def update_order(order_id: str, order: Order):
    order.order_id += order.user_id
    order = await app.mongodb.find_one({"order_id": order_id})
    if order:
        await app.mongodb.update_one({"order_id": order_id}, {"$set": order.dict()})
        return {"message": "Order updated successfully"}
    raise HTTPException(status_code=404, detail="Order not found")
    
@app.delete("/orders/{order_id}/")
async def delete_order(order_id: str):
    order = await app.mongodb.find_one({"order_id": order_id})
    if order:
        await app.mongodb.delete_one({"order_id": order_id})
        return {"message": "Order deleted successfully"}
    raise HTTPException(status_code=404, detail="Order not found")
    
@app.get("/orders/")
async def list_orders():
    orders = []
    cursor = app.mongodb.find()
    async for order in cursor:
        del order["_id"]
        orders.append(order)
    return orders

@app.get("/")
def home():
    return "hello from order-management"

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

