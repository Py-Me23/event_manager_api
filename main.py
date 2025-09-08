from fastapi import FastAPI, Form, File, UploadFile
from db import events_collection
from pydantic import BaseModel
from bson.objectid import ObjectId
from utils import replace_mongo_id
from typing import Annotated


class EventModel(BaseModel):
    title: str
    description: str


app = FastAPI()

# http://localhost:8000/docs is the same as  http://127.0.0.1:8000
# the end point has a method of get, the slash means homepage. status code by default is 200.


@app.get("/", status_code=204, response_description="No content")
def get_home():
    return {"message": "You are on the home page"}


# Events endpoints
@app.get("/events")  # query parameter
def get_events(title="", description="", limit=10, skip=0):
    # Get all events from database
    events = events_collection.find(
        filter={
            "$or": [
                {"title": {"$regex": title, "$options": "i"}},
                {"description": {"$regex": description, "$options": "i"}},
            ]
        },
        limit=int(limit),
        skip=int(skip),
    ).to_list()

    # Return response
    return {"data": list(map(replace_mongo_id, events))}


@app.post("/events")
def post_events(
    title: Annotated[str, Form()],
    description: Annotated[str, Form()],
    flyer: Annotated[UploadFile, File()],
):
    # insert event into database
    # events_collection.insert_one(event.model_dump())
    # return response
    return {"message": "Events added successfully"}


@app.get("/events/{event_id}")  # path parameter
def get_events_id(event_id):
    # get event from database by id
    event = events_collection.find_one({"_id": ObjectId(event_id)})
    # return response
    return {"data": replace_mongo_id(event)}
