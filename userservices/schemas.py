from pydantic import BaseModel, EmailStr, Field


class UserSchema(BaseModel):
    fullname: str = Field(...)
    email: EmailStr = Field(...)
    username: str = Field(...)
    password: str = Field(...)
    
    class Config:
        schema_extra = {
            "example": {
                "fullname": "John Doe",
                "email": "jdoe@x.edu.ng",
                "username": "daitech20",
                "password": "dai123"
            }
        }


class UserLoginSchema(BaseModel):
    username: str = Field(...)
    password: str = Field(...)
    
    class Config:
        schema_extra = {
            "example": {
                "username": "daitech20",
                "password": "dai123"
            }
        }