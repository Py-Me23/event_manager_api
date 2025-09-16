from fastapi import Form, File, UploadFile, HTTPException, status, APIRouter
from db import events_collection
from bson.objectid import ObjectId
from utils import replace_mongo_id
from typing import Annotated
import cloudinary
import cloudinary.uploader


# you create events router
events_router = APIRouter()


@events_router.get("/events")  # query parameter
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


#  allows users to upload a file
@events_router.post("/events", tags=["EVENTS"])
def post_events(
    title: Annotated[str, Form()],
    description: Annotated[str, Form()],
    flyer: Annotated[UploadFile, File()],
):
    #  upload flyer to cloudinary to get a url

    upload_result = cloudinary.uploader.upload(flyer.file)
    print(upload_result)
    # insert event into database
    events_collection.insert_one(
        {
            "title": title,
            "description": description,
            "flyer": upload_result["secure_url"],
        }
    )
    # return response
    return {"message": "Events added successfully"}


@events_router.get("/events/{event_id}")  # path parameter
def get_events_id(event_id):
    # check if event id is valid
    if not ObjectId.is_valid(event_id):
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY, "Invalid mongo id recieved!"
        )
    # get event from database by id
    event = events_collection.find_one({"_id": ObjectId(event_id)})
    # return response
    return {"data": replace_mongo_id(event)}


@events_router.put("/events/{event_id}")
def replace_event(
    event_id,
    title: Annotated[str, Form()],
    description: Annotated[str, Form()],
    flyer: Annotated[UploadFile, File()],
):
    # check if event_id is valid mongo id
    if not ObjectId.is_valid(event_id):
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY, "Invalid mongo id recieved!"
        )
    # upload flyer to cloudinary to get a url
    upload_result = cloudinary.uploader.upload(flyer.file)
    # replace event in database
    events_collection.replace_one(
        filter={"_id": ObjectId(event_id)},
        replacement={
            "title": title,
            "description": description,
            "flyer": upload_result["secure_url"],
        },
    )
    # return response
    return {"message": "Event replaced successfully"}


@events_router.delete("/events/{event_id}")
def delete_event(event_id):
    # check if event_id is valiid mongo id
    if not ObjectId.is_valid(event_id):
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY, "Invalid mongo id recieved!"
        )
    # delete event from database
    delete_result = events_collection.delete_one(filter={"_id": ObjectId(event_id)})
    if not delete_result.deleted_count:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "No event found to delete!")
    # return response
    return {"message": "Event successfully deleted!"}
