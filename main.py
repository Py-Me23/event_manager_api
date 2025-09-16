from fastapi import FastAPI
import cloudinary
from routes.events import events_router
from routes.users import users_router
import os
from dotenv import load_dotenv

# configure cloudinary
cloudinary.config(
    cloud_name=os.getenv("CLOUD_NAME"),
    api_key=os.getenv("API_KEY"),
    api_secret=os.getenv("API_SECRET"),
)

tags_metadata = [
    {
        "name": "HOME",
        "desciption": "General API information",
    },
    {
        "name": "EVENTS",
        "desciption": "Endpoints for searching  events",
    },
    {
        "name": "GET ONE EVENTS",
        "desciption": "Endpoints for searching  one event",
    },
]


# for emoji: windows + the colon key
app = FastAPI(
    title="🎊Events Finder API",
    description="Welcome to 😘AfiSante Events",
    openapi_tags=tags_metadata,
)


# http://localhost:8000/docs is the same as  http://127.0.0.1:8000
# the end point has a method of get, the slash means homepage. status code by default is 200.


@app.get("/", tags=["HOME"])
def get_home():
    return {"message": "You are on the home page"}


# include routers
app.include_router(events_router)
app.include_router(users_router)
