from fastapi import FastAPI, HTTPException, Depends, status, Response, Request
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import JSONResponse
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
print("ENV", load_dotenv())
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
    print(user)
    response = requests.post("http://user-service:8000/login/", json=user)
    res = response.json()
    return res, user

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail}
    )

@app.post("/orders/")
async def create_order(order: Order, res: Response, is_user = Depends(authenticate_user)):
    is_user = is_user[0]
    if is_user.get("error"):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=is_user["error"])
    order.order_id += order.user_id
    order_doc = order.dict()
    result = await app.mongodb.insert_one(order_doc)
    return {"message": "Created Order"}

@app.get("/orders/{order_id}/")
async def read_order(order_id: str, res: Response, is_user = Depends(authenticate_user)):
    is_user = is_user[0]
    if is_user.get("error"):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=is_user["error"])
    order = await app.mongodb.find_one({"order_id": order_id})
    if order:
        del order["_id"]
        return order
    raise HTTPException(status_code=404, detail="Order not found")

@app.put("/orders/{order_id}/")
async def update_order(order_id: str, order: Order,  res: Response, is_user = Depends(authenticate_user)):
    is_user = is_user[0]
    if is_user.get("error"):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=is_user["error"])
    o = await app.mongodb.find_one({"order_id": order_id})
    if o:
        order.order_id = o["order_id"]
        await app.mongodb.update_one({"order_id": order_id}, {"$set": order.dict()})
        return {"message": "Order updated successfully"}
    raise HTTPException(status_code=404, detail="Order not found")
    
@app.delete("/orders/{order_id}/")
async def delete_order(order_id: str, res: Response, is_user = Depends(authenticate_user)):
    is_user = is_user[0]
    if is_user.get("error"):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=is_user["error"])
    order = await app.mongodb.find_one({"order_id": order_id})
    if order:
        await app.mongodb.delete_one({"order_id": order_id})
        return {"message": "Order deleted successfully"}
    raise HTTPException(status_code=404, detail="Order not found")
    
@app.get("/orders/")
async def list_orders(res: Response, is_user = Depends(authenticate_user)):
    if is_user[0].get("error"):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=is_user["error"])
    orders = []
    cursor = app.mongodb.find({"user_id": is_user[1]["user"]})
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

