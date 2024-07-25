from fastapi import FastAPI
from .routers import alchemy_api, auth_api

app = FastAPI()

# TWO ROUTES DEFINED
# AUTH_API TO LOGIN AND GET JWT TOKEN
# FOR THIS EXCERCISE ASSUMED IN MEMORY USER TABLE AND SAVED IN SCHEMA

app.include_router(auth_api.router)
app.include_router(alchemy_api.router)


