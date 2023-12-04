import atexit
import os

from bson.objectid import ObjectId
from dotenv import load_dotenv
from pymongo.errors import ConnectionFailure, PyMongoError
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


class Database:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Database, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, database_name="tasktracker"):
        if not hasattr(self, '_initialized'):
            self.__db = database_name
            self.__collections = []
            load_dotenv()
            self.__initialize_db()
            atexit.register(self.__close_connection)
            self._initialized = True

    def __initialize_db(self, uris=None):
        if uris is None:
            uris = [
                os.getenv('MONGO_URI'),
                "mongodb://localhost:27017/" + self.__db,
            ]

        uri = uris[0]
        if uri:
            try:
                self.__client = MongoClient(uri, server_api=ServerApi('1'))
                self.__client.admin.command('ping')
                self.__collections = self.__client[self.__db].list_collection_names()
                self.__is_connected = True
                print(f"Connected to MongoDB using URI: {uri}")
            except ConnectionFailure:
                print(f"Failed to connect to MongoDB using URI: {uri}, trying next option...")
                self.__initialize_db(uris[1:])
        else:
            print("No valid URI found in current attempt, trying next option...")
            self.__initialize_db(uris[1:])

    def __close_connection(self):
        if self.__is_connected and self.__client:
            self.__client.close()
            self.__is_connected = False
            print("MongoDB connection closed.")

    @staticmethod
    def process_id(id_value):
        try:
            return ObjectId(id_value)
        except Exception as e:
            print(f"Invalid ObjectId: {e}")
            return None

    def create_document(self, collection_name, new_document):
        if not self.__is_connected:
            raise ConnectionError("Not connected to MongoDB.")
        if not isinstance(new_document, dict):
            print("Invalid document format. Document should be a dictionary.")
            return None
        try:
            collection = self.__client[self.__db][collection_name]
            return collection.insert_one(new_document).inserted_id
        except PyMongoError as e:
            print(f"Error adding document to MongoDB: {e}")
            return None

    def read_documents(self, collection_name, _id=None):
        if not self.__is_connected:
            raise ConnectionError("Not connected to MongoDB.")
        try:
            collection = self.__client[self.__db][collection_name]
            if _id:
                _id = self.process_id(_id)
                return collection.find_one({'_id': _id}) if _id else None
            else:
                return list(collection.find())
        except PyMongoError as e:
            print(f"Error retrieving document(s) from MongoDB: {e}")
            return None if _id else []

    def update_document(self, collection_name, document_id, update_data):
        if not self.__is_connected:
            raise ConnectionError("Not connected to MongoDB.")
        if not isinstance(update_data, dict):
            print("Invalid update data format. Data should be a dictionary.")
            return False
        document_id = self.process_id(document_id)
        if document_id is None:
            return False
        try:
            collection = self.__client[self.__db][collection_name]
            result = collection.update_one({'_id': document_id}, {'$set': update_data})
            return result.matched_count > 0 and result.modified_count > 0
        except PyMongoError as e:
            print(f"Error updating document in MongoDB {collection_name} collection: {e}")
            return False

    def delete_document(self, collection_name, document_id):
        if not self.__is_connected:
            raise ConnectionError("Not connected to MongoDB.")
        document_id = self.process_id(document_id)
        if document_id is None:
            return False
        try:
            collection = self.__client[self.__db][collection_name]
            result = collection.delete_one({'_id': document_id})
            return result.deleted_count > 0
        except PyMongoError as e:
            print(f"Error deleting document from MongoDB {collection_name} collection: {e}")
            return False


def get_db(g):
    if 'db' not in g:
        g.db = Database()
    return g.db
