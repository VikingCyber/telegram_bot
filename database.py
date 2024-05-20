from pymongo import MongoClient
from pymongo.database import Database


def get_database() -> Database:
    client = MongoClient("localhost", 27017)
    db = client["history_database"]
    return db
