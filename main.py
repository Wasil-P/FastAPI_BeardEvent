from models.db import SessionLocal, engine, DBContext

import os
from fastapi import FastAPI, Request, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
from sqlalchemy.orm import Session


app = FastAPI()
templates = Jinja2Templates(directory="templates")
load_dotenv()

secret_key = os.getenv("SECRET_KEY")
app.mount("/static", StaticFiles(directory="static"), name="static")


def get_db():
    with DBContext() as db:
        yield db


@app.get("/")
async def root():
    return {"message": "Hello World"}

