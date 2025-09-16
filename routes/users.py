from fastapi import APIRouter, Form, status, HTTPException
from typing import Annotated
from pydantic import EmailStr
from db import users_collection
import bcrypt

# create users router
users_router = APIRouter()


# define endpoints
@users_router.post("/users/sign up")
def register_user(
    username: Annotated[str, Form()],
    email: Annotated[EmailStr, Form()],
    password: Annotated[str, Form(min_length=8)],
):

    # ensure user does not exist
    user_count = users_collection.count_documents(filter={"email": email})
    if user_count > 0:
        raise HTTPException(status.HTTP_409_CONFLICT, "User already exists!")

    # hash user password
    hashed_password = bcrypt.hashpw(bytes(password.encode("utf-8")), bcrypt.gensalt())

    # save user into database
    users_collection.insert_one(
        {
            "username": username,
            "email": email,
            "password": hashed_password.decode("utf-8"),
        }
    )
    # Return response

    return {"message": "User registered successfully!"}
