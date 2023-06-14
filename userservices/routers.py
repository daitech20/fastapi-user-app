from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
from fastapi import Depends, HTTPException, status
from datetime import timedelta
from security import validate_token
from fastapi_jwt_auth import AuthJWT
from datetime import datetime, timedelta
from settings import SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS
from pydantic import BaseModel
from fastapi_jwt_auth.exceptions import MissingTokenError, InvalidHeaderError

from services import (
    add_user,
    retrieve_user,
    retrieve_users,
    update_user,
    delete_user,
    authenticate_user
)
from models import (
    ErrorResponseModel,
    ResponseModel,
    UpdateUserModel
)
from schemas import (
    UserSchema,
    UserLoginSchema
)

router = APIRouter()

class Settings(BaseModel):
    authjwt_secret_key: str = SECRET_KEY


@AuthJWT.load_config
def get_config():
    return Settings()


@router.get("/")
async def get_all_user_data(Authorize: AuthJWT = Depends()):

    try:
        Authorize.jwt_required()
        current_user = Authorize.get_jwt_subject()

    except MissingTokenError:
        return ErrorResponseModel(400, "Token not exists")
    except InvalidHeaderError:
        return ErrorResponseModel(401, "Token not valid")
    
    users = await retrieve_users()
    return ResponseModel(users, "Get all user successfully.")


@router.get("/get-user")
async def get_user_data_by_id(id_user: str, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
        current_user = Authorize.get_jwt_subject()

    except MissingTokenError:
        return ErrorResponseModel(400, "Token not exists")
    except InvalidHeaderError:
        return ErrorResponseModel(401, "Token not valid")
    
    try:
        user = await retrieve_user(id_user)
    except:
        return ErrorResponseModel(400, "Not a valid ObjectId, it must be a 12-byte input or a 24-character hex string")
    
    return ResponseModel(user, "Get user successfully.")


@router.post("/add-user", response_description="User data added into the database", dependencies=[Depends(validate_token)])
async def add_user_data(user: UserSchema = Body(...)):
    user = jsonable_encoder(user)
    new_user = await add_user(user)
    if new_user:
        return ResponseModel(new_user, "User added successfully.")
    else:
        return ErrorResponseModel(400, "Bad request")


@router.put("/update-user", response_description="User data updated in to the database", dependencies=[Depends(validate_token)])
async def update_user_data(id_user: str, user_data: UpdateUserModel = Body(...)):
    user_data = jsonable_encoder(user_data)
    check_update = await update_user(id_user, user_data)
    if check_update:
        return ResponseModel(user_data, "User updated successfully.")
    else:
        return ErrorResponseModel(400, "Bad request")


@router.delete("/update-user", response_description="User data is deleted ")
async def delete_user_data(id_user: str):
    check_delete = await delete_user(id_user)
    if check_delete:
        return ResponseModel("", "User deleted successfully.")
    else:
        return ErrorResponseModel(400, "Bad request")
    

@router.post("/login")
async def login(
    Authorize: AuthJWT = Depends(),
    user: UserLoginSchema = Body(...)
):
    user = jsonable_encoder(user)
    user = await authenticate_user(user["username"], user["password"])

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = Authorize.create_access_token(
        subject=user["username"],
        expires_time=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    refresh_token = Authorize.create_refresh_token(
        subject=user["username"],
        expires_time=timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "expires_time": datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    

@router.post('/refresh')
def refresh(
    Authorize: AuthJWT = Depends()
):
    try:
        Authorize.jwt_refresh_token_required()
        current_user = Authorize.get_jwt_subject()
    except BaseException:
        return {"error": "error"}
    
    new_access_token = Authorize.create_access_token(
        subject=current_user,
        expires_time=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    
    return {"access_token": new_access_token}