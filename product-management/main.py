from fastapi import FastAPI, HTTPException, Depends, status, Response, Request
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import JSONResponse
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from bson import ObjectId
from dotenv import load_dotenv
import os
import requests

app = FastAPI()
security = HTTPBasic()

# MongoDB connection settings
load_dotenv()
MONGO_URL = os.getenv("MONGO_URI")
DB_NAME = "YaEC"
PRODUCTS_COLLECTION = "Products"
 
class Product(BaseModel):
    name: str
    description: str
    price: float

class Admin(BaseModel):
    user: str
    passwd: str
    is_admin: bool
    
class User(BaseModel):
    user: str
    passwd: str


@app.get("/")
def home():
    return "hello from product-management"

@app.on_event("startup")
async def startup_db_client():
    app.mongodb_client = AsyncIOMotorClient(MONGO_URL)
    app.mongodb = app.mongodb_client[DB_NAME][PRODUCTS_COLLECTION]

@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()


async def check_admin(credentials: HTTPBasicCredentials = Depends(security)):
    user = {
        "user": credentials.username, 
        "passwd": credentials.password
    }
    response = requests.post("http://yaec-user-management-1:8000/check_admin/", json=user)
    res = response.json()
    return res
    
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail}
    )


@app.post("/products/", status_code=status.HTTP_201_CREATED)
async def create_product(product: Product, res: Response, is_admin = Depends(check_admin)):
    if is_admin.get("error"):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=is_admin["error"])
    product_doc = product.dict()
    await app.mongodb.insert_one(product_doc)
    return {"message": "Product created"}

@app.get("/products/{product_name}/", status_code=status.HTTP_200_OK)
async def get_product(product_name: str):
    product = await app.mongodb.find_one({"name": product_name})
    if product:
        del product["_id"]
        return product
    raise HTTPException(status_code=404, detail="Product not found")

@app.put("/products/{product_name}/", status_code=status.HTTP_200_OK)
async def update_product(product_name: str, product: Product, is_admin = Depends(check_admin)):
    if is_admin.get("error"):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=is_admin["error"])
    if await app.mongodb.find_one({"name": product_name}):
        await app.mongodb.update_one({"name": product_name}, {"$set": product.dict()})
        return {"message": "Product updated successfully"}
    else:
        raise HTTPException(status_code=404, detail="Product does not exist")
    
@app.delete("/products/{product_name}/", dependencies=[Depends(check_admin)], status_code=status.HTTP_200_OK)
async def delete_product(product_name: str, is_admin = Depends(check_admin)):
    if is_admin.get("error"):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=is_admin["error"])
    if await app.mongodb.find_one({"name": product_name}):
        await app.mongodb.delete_one({"name": product_name})
        return {"message": "Product deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Product does not exist")
    
@app.get("/products/", status_code=status.HTTP_200_OK)
async def list_products(skip: int = 0, limit: int = 10):
    products = [ ]
    cursor = app.mongodb.find().skip(skip).limit(limit)
    async for product in cursor:
        del product["_id"]
        products.append(product)
    return products


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

