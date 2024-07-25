from typing import Optional
from pydantic import BaseModel

class User(BaseModel):
    user_email: str
    user_pass: str
    is_paying: bool

class Token(BaseModel):
    access_token: str
    token_type:str

class TokenData(BaseModel):
    id: Optional[str]

users_table = [
    {"email":"sandy01@test.com","passwd":"pass","paying":False},
    {"email":"sandy02@test.com","passwd":"pass","paying":False},
    {"email":"sandy03@test.com","passwd":"1234","paying":True},
    {"email":"sandy04@test.com","passwd":"pass","paying":False},
    {"email":"sandy05@test.com","passwd":"pass","paying":False}
    ]

# This is more of a placeholder as other schemas can be used here
# All system variables are defined here, so cn be changed centrally
# I have created a blank models.py as database.py for DB Operations. 