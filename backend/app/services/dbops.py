import os
from dotenv import load_dotenv
from pymongo import MongoClient

class dbOps():
    def __init__(self):
        load_dotenv()
        self.__atlas_key = os.getenv("ATLAS_CONNECTION_STRING")
        self.__db_name = os.getenv("DB_NAME")
        self.__collection_name_text = os.getenv("COLLECTION_NAME_TEXT")
        self.__collection_name_img = os.getenv("COLLECTION_NAME_IMG")
    
    def insert_text(self, text):
        with MongoClient(self.__atlas_key) as client:
            db = client[self.__db_name]
            collection = db[self.__collection_name_text]
            result = collection.insert_many(text)
        return result.inserted_ids

    def insert_img(self, img):
        with MongoClient(self.__atlas_key) as client:
            db = client[self.__db_name]
            collection = db[self.__collection_name_img]
            result = collection.insert_many(img)
        return result.inserted_ids