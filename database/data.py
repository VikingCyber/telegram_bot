# import pprint

from pymongo import MongoClient
from pymongo.database import Database


def get_database() -> Database:
    client = MongoClient("localhost", 27017)
    db = client["history_database"]
    return db


# a = get_database()
# collection = a["history"]
# pprint.pprint(collection.find_one({'_id': 1}))
