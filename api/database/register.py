from pymongo import MongoClient
import pymongo
import datetime
from .database import Database as DB


class UserDatabase(DB):
    def __init__(self, uri) -> None:
        self.client = MongoClient(uri)
        self.database = self.client["code11"]
        self.collection = self.database["note-app"]

    async def insert(self, username, password, email):
        return self.collection.insert_one(
            {"username": username, "email": email, "password": password}
        )

    async def delete(self):
        pass

    async def get(self, type, username, password, email=None):
        if type == "username":
            return self.collection.find_one(
                {"username": username, "password": password}
            )
        elif type == "email":
            return self.collection.find_one(
                {"username": username, "password": password, "email": email}
            )

    async def update(self):
        pass
