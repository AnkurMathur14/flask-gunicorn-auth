import os
from pymongo import MongoClient

DATABASE_URL=os.environ.get('DATABASE_URL') or "mongodb://127.0.0.1:27017/"
print(DATABASE_URL)

DATABASE_NAME = "myproject"
client = MongoClient(DATABASE_URL)
db = client[DATABASE_NAME]

class DBManager:
    def __init__(self, collection_name):
        self.collection_name = collection_name
        self.my_collection = db[self.collection_name]

    # insert one or many
    def insert(self, input_data):
        if not input_data:
            return None
        self.my_collection.insert_many(input_data)
        return input_data

    # search one or many
    def search(self, query={}):
        docs = self.my_collection.find(query)
        if not docs:
            return None
        out = [{**doc, "_id": str(doc["_id"])} for doc in docs]
        if len(out) == 1:
            return out[0]
        return out

    # delete one or many
    def delete(self, query={}):
        docs = self.search(query)
        if not docs:
            return None

        self.my_collection.delete_many(query)
        return True

    # update one or many
    def update(self, query={}, data={}):
        docs = self.my_collection.update_many(query, data)
        return docs






