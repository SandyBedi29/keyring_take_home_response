from fastapi import APIRouter, Depends, status, HTTPException
from ..schemas import users_table
from .. import oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(tags=["LOGIN"])

# LOGIN ROUTER TO CHECK USER NAME AND PASSWORD FROM IN MEMORY USER TABLE
# ONE USER IS AUTHENTICATED JWT TOKEN IS RETURNED

@router.post("/login")
def login_get_token(user_cred: OAuth2PasswordRequestForm = Depends()):
    
    usr_found=False
    
    for usr in users_table:
        if ((usr['email'] == user_cred.username) & (usr['passwd'] == user_cred.password)) :
            usr_found_id=usr['email']
            is_paying=usr['paying']
            usr_found=True
    
    if not usr_found:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Invalid Credentials")
    
    print(usr_found)
    access_token = oauth2.create_access_token(data = {"user_id":user_cred.username})
    return{"user_id":usr_found_id,
           "is_user_paying":is_paying,
           "access_token":access_token, 
           "token_type":"bearer"}

