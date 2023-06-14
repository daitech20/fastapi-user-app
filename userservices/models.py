from typing import Optional
from pydantic import BaseModel, EmailStr
from fastapi import HTTPException


class UpdateUserModel(BaseModel):
    fullname: Optional[str]
    email: Optional[EmailStr]
    username: Optional[str]
    password: Optional[int]

    class Config:
        schema_extra = {
            "example": {
                "fullname": "John Doe",
                "email": "jdoe@x.edu.ng",
                "username": "daitech20",
                "password": "dai123"
            }
        }
    
    
def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(code, message):
    raise HTTPException(
        status_code=code, detail=message
    )