import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from pydantic import ValidationError
from settings import SECRET_KEY, ALGORITHM

reusable_oauth2 = HTTPBearer(
    scheme_name='Authorization'
)


def validate_token(http_authorization_credentials=Depends(reusable_oauth2)) -> str:
    """
    Decode JWT token to get username => return username
    """
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
        
    try:
        payload = jwt.decode(http_authorization_credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get('sub')
    except(jwt.PyJWTError, ValidationError):
        raise credentials_exception