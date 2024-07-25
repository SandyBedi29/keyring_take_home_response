from jose import JWTError, jwt
from datetime import UTC, datetime,timedelta
from . import schemas
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv
import os

# auth_api verifies the user name and password based on user input (in mem user table)
# then it call the create_access_token to generate jwt token and also to get token expitation minutes
# for alchemy_api then i have added this dependency to have a valid token
# get_current_user function calls the verify_access_token as once the token is valid the api route is opened
  
load_dotenv()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def create_access_token(data:dict):
    
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")))
    to_encode.update({"exp":expire})

    encoded_jwt = jwt.encode(to_encode, os.getenv("SECRET_KEY"), algorithm=os.getenv("ALGORITHM"))

    return encoded_jwt

def verify_access_token(token:str,cred_exception):

    try:
        payload = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=[os.getenv("ALGORITHM")])
        id: str = payload.get("user_id")
        if id is None:
            raise cred_exception
        token_data=schemas.TokenData(id = id)
    except JWTError as e:
        raise cred_exception
    
    return token_data

def get_current_user(token:str = Depends(oauth2_scheme)):
    credentials_expection=HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid Credentials",
        headers={"WWW-Authenticate":"Bearer"})
    return verify_access_token(token,credentials_expection)