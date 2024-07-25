from fastapi import APIRouter, Depends, status, HTTPException
import os
from dotenv import load_dotenv
import requests
from datetime import datetime, timezone
from .. import oauth2
from ..schemas import TokenData,users_table

# ROUTER TO GET RATING AND OTHER DETAILS

load_dotenv()
router = APIRouter()

@router.get("/crypto/{input_hash}")
def get_block(input_hash:str, user_id : int = Depends(oauth2.get_current_user)):

    url=os.getenv("ALCHEMY_URL")+os.getenv("ALCHEMY_API_KEY")
    payload = {
        "id": 1,
        "jsonrpc": "2.0",
        "params": [input_hash],
        "method": "eth_getTransactionByHash"
        }
    headers = {
        "accept": "application/json",
        "content-type": "application/json"
        }
    response = requests.post(url, json=payload, headers=headers)

    if not response:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Transaction Hash is not valid")
    
    response_json = response.json()
    block_no_string=response_json["result"]["blockNumber"]

    input_hash_int = int(input_hash,16)
    block_no_int = int(block_no_string,16)
    trans_rating = ((input_hash_int + block_no_int) % 5) + 1

    payload = {
        "jsonrpc": "2.0",
        "method": "eth_getBlockByNumber",
        "params": [hex(block_no_int), True],
        "id": 1
    }

    response = requests.post(url, json=payload)
    trans = response.json()
    block_timestamp=int(trans["result"]["timestamp"],16)
    block_datetime = datetime.fromtimestamp(block_timestamp, tz=timezone.utc)
    current_datetime = datetime.now(tz=timezone.utc)
    transaction_age = current_datetime - block_datetime
    tsec=transaction_age.total_seconds()
    print (tsec)

    uid:TokenData = user_id
    for usr in users_table:
        if (usr['email'] == uid.id):
            is_paying:bool=usr['paying']
    
    if (is_paying or tsec>300):
        return {
            "customer_id":uid.id, 
            "customer_is_paying":is_paying,
            "HASH":input_hash,
            "BLOCK":block_no_string,
            "AGE":str(transaction_age),
            "rating":trans_rating
            }
    
    return {
        "customer_id":uid.id, 
        "customer_is_paying":is_paying,
        "message":"Please buy subscription to avail this service"
        }
