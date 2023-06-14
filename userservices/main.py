from fastapi import FastAPI
from routers import router as UserRouter
import uvicorn


app = FastAPI()
app.include_router(UserRouter, tags=["User"], prefix="/user")


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)