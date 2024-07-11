from fastapi import FastAPI
from routers.users_routers import router as users_router
from routers.events_routers import router as events_router


app = FastAPI()


@app.get("/")
def root():
    return {"message": "Welcome to the app BeardEvent"}


app.include_router(
    router=users_router,
    prefix="/users",
                    )

app.include_router(
    router=events_router,
    prefix="/events",
                    )