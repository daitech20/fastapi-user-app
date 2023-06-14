import motor.motor_asyncio
from settings import MONGODB_URI
from bson.objectid import ObjectId
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer


client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URI)
database = client.users
user_collection = database.get_collection("users_collection")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# helpers
def user_helper(user) -> dict:
    return {
        "id": str(user["_id"]),
        "fullname": user["fullname"],
        "email": user["email"],
        "username": user["username"],
        "password": user["password"]
    }


async def retrieve_users():
    users = []
    async for user in user_collection.find():
        users.append(user_helper(user))
    return users


# Retrieve a user with a matching ID
async def retrieve_user(id: str) -> dict:
    user = await user_collection.find_one({"_id": ObjectId(id)})
    if user:
        return user_helper(user)
    else:
        return False


async def retrieve_user_by_username(username: str) -> dict:
    user = await user_collection.find_one({"username": username})
    if user:
        return user_helper(user)
    else:
        return False


async def add_user(user_data: dict) -> dict:
    user_data["password"] = pwd_context.hash(user_data["password"])
    user = await retrieve_user_by_username(user_data["username"])
    
    if user:
        False
    else:
        user = await user_collection.insert_one(user_data)
        new_user = await user_collection.find_one({"_id": user.inserted_id})
        return user_helper(new_user)


async def update_user(id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    user = await user_collection.find_one({"_id": ObjectId(id)})
    if user:
        updated_user = await user_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_user:
            return True
        return False


async def delete_user(id: str):
    user = await user_collection.find_one({"_id": ObjectId(id)})
    if user:
        await user_collection.delete_one({"_id": ObjectId(id)})
        return True
    else:
        return False
    

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


async def authenticate_user(username: str, password: str):
    user = await retrieve_user_by_username(username)

    if not user:
        return False
    if not verify_password(password, user["password"]):
        return False
    return user