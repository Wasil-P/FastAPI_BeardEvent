import os
from fastapi import FastAPI, Request, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
from routers.users import router as users_router


app = FastAPI()
templates = Jinja2Templates(directory="templates")
load_dotenv()

secret_key = os.getenv("SECRET_KEY")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def root():
    return {"message": "Welcome to the app BeardEvent"}


app.include_router(
    router=users_router,
    prefix="/users",
                    )
