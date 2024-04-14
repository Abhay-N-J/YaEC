from fastapi import FastAPI, HTTPException, Depends, status, Response
from motor.motor_asyncio import AsyncIOMotorClient
from passlib.context import CryptContext
from pydantic import BaseModel
from bson import ObjectId
from dotenv import load_dotenv
import os

app = FastAPI()

# MongoDB connection settings
load_dotenv()
MONGO_URL = os.getenv("MONGO_URI")
DB_NAME = "YaEC"
USER_COLLECTION = "Users"


# Password hashing settings
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserRegister(BaseModel):
    user: str
    email: str
    passwd: str

class UserLogin(BaseModel):
    user: str
    passwd: str

class UserProfileUpdate(BaseModel):
    email: str
    # Add more fields as required for the user profile update

@app.on_event("startup")
async def startup_db_client():
    app.mongodb_client = AsyncIOMotorClient(MONGO_URL)
    app.mongodb = app.mongodb_client[DB_NAME]

@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()


# Function to hash password
def hash_password(password: str):
    return pwd_context.hash(password)

# Function to verify password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Function to register a new user
async def register_user(user: UserRegister, db):
    user.passwd = hash_password(user.passwd)
    user_doc = user.dict()
    user_doc["is_admin"] = False
    result = await db[USER_COLLECTION].insert_one(user_doc)

# Function to authenticate user
async def authenticate_user(user: UserLogin, db) -> bool:
    stored_user = await db[USER_COLLECTION].find_one({"user": user.user})
    if not stored_user:
        return False
    if not verify_password(user.passwd, stored_user["passwd"]):
        return False
    return True

# Function to update user profile
async def update_user_profile(user_id: str, profile_update: UserProfileUpdate, db):
    result = await db[USER_COLLECTION].update_one(
        {"_id": ObjectId(user_id)}, {"$set": profile_update.dict()}
    )
    return result.modified_count > 0

async def user_exists(user: UserRegister, db) -> bool:
    return await db[USER_COLLECTION].count_documents({"user": user.user}) == 0

# Register route for user registration
@app.post("/register/", status_code=status.HTTP_201_CREATED)
async def register_new_user(user: UserRegister, res: Response):
    db = app.mongodb
    if await user_exists(user, db) == False:
        return {"message": "Username or email already taken"}
    await register_user(user, db)
    return {"message": "User registered successfully"}

# Login route for user authentication
@app.post("/login/", status_code=status.HTTP_202_ACCEPTED)
async def login_user(user: UserLogin, res: Response):
    db = app.mongodb
    authenticated = await authenticate_user(user, db)
    if not authenticated:
        res.status_code = status.HTTP_401_UNAUTHORIZED
        return {"message": "Invalid credentials"}
    return {"message": "Login successful"}

@app.post("/check_admin/", status_code=status.HTTP_202_ACCEPTED)
async def check_admin(user: UserLogin, res: Response):
    db = app.mongodb
    authenticated = await authenticate_user(user, db)
    if not authenticated or await db[USER_COLLECTION].count_documents({"$and": [{"user": user.user}, {"is_admin": True}]}) == 0:
        res.status_code = status.HTTP_401_UNAUTHORIZED
        return {"message": "Invalid credentials"}
    return {"message": "Login successful"}

# Route for updating user profile 
# TODO #INCOMPLETE #ERRONEOUSS
@app.put("/profile/{user_id}/",status_code=status.HTTP_200_OK)
async def update_profile(user_id: str, profile_update: UserProfileUpdate, res: Response):
    db = app.mongodb
    updated = await update_user_profile(user_id, profile_update, db)
    if not updated:
        res.status_code = status.HTTP_404_NOT_FOUND
        return {"message": "User not found"}
    return {"message": "Profile updated successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
