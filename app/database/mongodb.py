import os

from pymongo import MongoClient


MONGODB_URL = os.getenv(
    "MONGODB_URL",
    "mongodb://localhost:27017"
)

MONGODB_DATABASE = os.getenv(
    "MONGODB_DATABASE",
    "devops_lab"
)

client = MongoClient(MONGODB_URL)

database = client[MONGODB_DATABASE]

users_collection = database["users"]


def create_indexes():
    users_collection.create_index(
        [
            ("name", 1),
            ("email", 1)
        ],
        unique=True
    )