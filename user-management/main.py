from fastapi import FastAPI, HTTPException, Depends, status, Response, Request
from fastapi.responses import JSONResponse
from motor.motor_asyncio import AsyncIOMotorClient
from passlib.context import CryptContext
from pydantic import BaseModel
from bson import ObjectId
from dotenv import load_dotenv
from datetime import datetime, timedelta
from uuid import uuid4
import os


app = FastAPI()

# MongoDB connection settings
load_dotenv()
MONGO_URL = os.getenv("MONGO_URI")
DB_NAME = "YaEC"
USER_COLLECTION = "Users"
TOKEN_COLLECTION = "Tokens"
VALIDITY = 10



# Password hashing settings
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Token(BaseModel):
    user: str
    token: str
    creation: datetime

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
    print(MONGO_URL)
    app.mongodb_client = AsyncIOMotorClient(MONGO_URL)
    app.mongodb = app.mongodb_client[DB_NAME]
    print("----------------------------------------DONE------------------------------------")

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
    return await db[USER_COLLECTION].count_documents({"$or": [{"user": user.user}, {"email": user.email}]}) == 0

async def create_token(user: str, db) -> str:
    token = str(uuid4()) + user + str(datetime.now())
    await db[TOKEN_COLLECTION].insert_one({"user": user, "token": token, "creation": datetime.now()})
    return token
    # passTokens[user] = Token.parse_obj({"token": token, "creation": datetime.now()})
    
async def authenticate_token(user: UserLogin, login: bool):
    db = app.mongodb
    is_authenticated = await authenticate_user(user, db)
    token = await db[TOKEN_COLLECTION].find_one({"user": user.user})
    print("TOKEN", token)
    if token:
        is_valid_token = token["creation"] + timedelta(hours=VALIDITY) > datetime.now()
        is_correct_token = token["token"] == user.passwd
        
        if is_correct_token and is_valid_token:
            return {"message": "Login successful"}
        elif is_valid_token and is_authenticated: 
            return {"token": token["token"]}
        elif not is_valid_token and is_correct_token:
            await db[TOKEN_COLLECTION].delete_one({"user": token["user"]})
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Regenerate token")
        elif not is_correct_token and not is_authenticated:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials")

    if is_authenticated and login:
        token = await create_token(user.user, db)
        return {"token": token}

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials")
        
    
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail}
    )

@app.get("/")
def user_home():
    return "Hello from user"

# Register route for user registration
@app.post("/register/", status_code=status.HTTP_201_CREATED)
async def register_new_user(user: UserRegister, res: Response):
    print("hello")
    db = app.mongodb
    if await user_exists(user, db) == False:
        return {"message": "Username or email already taken"}
    await register_user(user, db)
    return {"message": "User registered successfully"}

# Login route for user authentication
@app.post("/login/", status_code=status.HTTP_202_ACCEPTED)
async def login_user(user: UserLogin, res: Response):
    res = await authenticate_token(user, True)
    return res

@app.post("/check_admin/", status_code=status.HTTP_202_ACCEPTED)
async def check_admin(user: UserLogin, res: Response):
    db = app.mongodb
    res = await authenticate_token(user, False)
    admin_count = await db[USER_COLLECTION].count_documents({"$and": [{"user": user.user}, {"is_admin": True}]})
    if admin_count > 0:
        return {"message": "Login successful"}
    else:
        raise HTTPException(status_code=401, detail="Not Admin")
        
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

@app.delete("/del_cache/{user}/", status_code=status.HTTP_200_OK)
async def debug_del_cache(user: str):
    if await app.mongodb[TOKEN_COLLECTION].findOne({"user": user}):
        await app.mongodb[TOKEN_COLLECTION].deleteOne({"user": user})
        return {"ok": 1} 
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Key not found")



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
