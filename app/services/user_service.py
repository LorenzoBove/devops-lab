from bson import ObjectId
from pymongo import ReturnDocument
from pymongo.errors import DuplicateKeyError

from app.database.mongodb import users_collection
from app.schemas.user import UserCreate, UserUpdate


def create_user(user: UserCreate):
    try:
        result = users_collection.insert_one(user.model_dump())

    except DuplicateKeyError:
        raise ValueError("User already exists")

    return {
        "id": str(result.inserted_id),
        "name": user.name,
        "email": user.email
    }


def get_users():
    users = users_collection.find()

    return [
        {
            "id": str(user["_id"]),
            "name": user["name"],
            "email": user["email"]
        }
        for user in users
    ]


def get_user(user_id: str):

    if not ObjectId.is_valid(user_id):
        raise ValueError("Invalid user ID")

    user = users_collection.find_one(
        {"_id": ObjectId(user_id)}
    )

    if user is None:
        return None

    return {
        "id": str(user["_id"]),
        "name": user["name"],
        "email": user["email"]
    }


def update_user(user_id: str, user: UserUpdate):

    if not ObjectId.is_valid(user_id):
        raise ValueError("Invalid user ID")

    try:
        updated_user = users_collection.find_one_and_update(
            {"_id": ObjectId(user_id)},
            {
                "$set": {
                    "name": user.name,
                    "email": user.email
                }
            },
            return_document=ReturnDocument.AFTER
        )

    except DuplicateKeyError:
        raise ValueError("User already exists")

    if updated_user is None:
        return None

    return {
        "id": str(updated_user["_id"]),
        "name": updated_user["name"],
        "email": updated_user["email"]
    }



def delete_user(user_id: str):

    if not ObjectId.is_valid(user_id):
        raise ValueError("Invalid user ID")

    result = users_collection.delete_one(
        {"_id": ObjectId(user_id)}
    )

    if result.deleted_count == 0:
        return False

    return True