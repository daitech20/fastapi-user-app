from fastapi import FastAPI
import sys
sys.path.append("C:\\Users\\steven\\Documents\\daindp2\\learn_FastApi\\UserServices\\userservices")
from userservices.routers import router as UserRouter


app = FastAPI()
app.include_router(UserRouter, tags=["User"], prefix="/user")


@app.get("/", tags=["Root"])
async def root():
    return {"message": "Hello World"}