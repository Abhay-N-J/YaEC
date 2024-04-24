from fastapi import FastAPI, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from bson import ObjectId
from dotenv import load_dotenv
import os

app=FastAPI()


class Review(BaseModel):
    product_name: str
    user_name: str
    rating: int
    comment: str

# MongoDB connection settings
load_dotenv()
MONGO_URL = os.getenv("MONGO_URI")
DB_NAME = "YaEC"
REVIEW_COLLECTION = "Reviews"

@app.get("/")
def home():
    return "hello from review-management"

@app.on_event("startup")
async def startup_db_client():
    app.mongodb_client = AsyncIOMotorClient(MONGO_URL)
    app.mongodb = app.mongodb_client[DB_NAME][REVIEW_COLLECTION]

@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()

@app.post("/reviews/")
async def create_review(review: Review):
    review_doc = review.dict()
    result = await app.mongodb.insert_one(review_doc)
    return {"id": str(result.inserted_id)}

@app.get("/reviews/{product_name}/")
async def read_review(product_name: str):
    reviews = []
    async for review in app.mongodb.find({"product_name": product_name}):
        del review["_id"]
        reviews.append(review)
    return {"reviews": reviews}

@app.get("/reviews/{user_name}/{product_name}/")
async def read_review(user_name: str, product_name: str):
    review = await app.mongodb.find_one({"product_name": product_name, "user_name": product_name})
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    review = review.dict()
    del review["_id"]
    return {"reviews": review}

@app.put("/reviews/{user_name}/{product_name}/")
async def update_review(user_name: str, product_name: str, review: Review):
    review = await app.mongodb.find_one({"user_name": user_name, "product_name": product_name})
    if review:    
        await app.mongodb.update_one({"user_name": user_name, "product_name": product_name}, {"$set": review.dict()})
        return {"message": "Review updated successfully"}
    raise HTTPException(status_code=404, detail="Review not found")


@app.delete("/reviews/{user_name}/{product_name}/")
async def delete_review(user_name: str, product_name: str):
    review = await app.mongodb.find_one({"user_name": user_name, "product_name": product_name})
    if review:
        await app.mongodb.delete_one({"user_name": user_name, "product_name": product_name})
        return {"message": "Review deleted successfully"}
    raise HTTPException(status_code=404, detail="Review not found")

@app.get("/reviews/")
async def list_reviews():
    reviews = []
    cursor = app.mongodb.find()
    async for review in cursor:
        del review["_id"]
        reviews.append(review)
    return reviews


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)