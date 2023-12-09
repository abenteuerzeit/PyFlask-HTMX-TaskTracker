import atexit
import logging
import os

from bson.objectid import ObjectId
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, PyMongoError

from utils.connection import database_connection

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Database:
    def __init__(self, database_name="tasktracker"):
        self.db_name = database_name
        self.client = None
        self.collections = []
        self.initialize_db()

    def initialize_db(self, uris=None):
        if self.client:
            return self.client

        if uris is None:
            uris = [
                os.getenv('MONGO_URI'),
                f"mongodb://localhost:27017/{self.db_name}",
            ]

        uri = uris[0]
        if not uri:
            logger.warning("No valid URI found in the current attempt, trying the next option...")
            self.initialize_db(uris[1:])
            return

        try:
            self.client = MongoClient(uri)
            self.client.admin.command('ping')
            self.collections = self.client[self.db_name].list_collection_names()
            atexit.register(self.close_connection)
            logger.info(f"Connected to MongoDB using URI: {uri}")
        except ConnectionFailure:
            logger.error(f"Failed to connect to MongoDB using URI: {uri}, trying the next option...")
            self.initialize_db(uris[1:])
        except IndexError:
            logger.warning("No valid URI found in the current attempt.")

    def close_connection(self):
        if self.client:
            self.client.close()
            self.client = None
            logger.info("MongoDB connection closed.")

    @staticmethod
    def process_id(id_value):
        try:
            return ObjectId(id_value)
        except Exception as e:
            logger.error(f"Invalid ObjectId: {e}")
            return None

    @database_connection
    def create_document(self, collection_name, new_document):
        if not isinstance(new_document, dict):
            logger.error("Invalid document format. Document should be a dictionary.")
            return None

        try:
            collection = self.client[self.db_name][collection_name]
            if collection_name == "users":
                user = collection.find_one({'username': new_document['username']})
                if user:
                    raise ValueError(f"User {new_document['username']} already exists.")
                return collection.insert_one(new_document).inserted_id
            return collection.insert_one(new_document).inserted_id
        except PyMongoError as e:
            logger.error(f"Error adding document to MongoDB {collection_name} collection: {e}")
        except ValueError as e:
            logger.error(f"Error adding document to MongoDB {collection_name} collection: {e}")
        return None

    @database_connection
    def read_documents(self, collection_name, _id=None):
        try:
            collection = self.client[self.db_name][collection_name]

            if _id:
                if collection_name == "users":
                    return collection.find_one({'username': _id}) if _id else None
                _id = self.process_id(_id)
                return collection.find_one({'_id': _id}) if _id else None

            return list(collection.find())
        except PyMongoError as e:
            logger.error(f"Error retrieving document(s) from MongoDB {collection_name} collection: {e}")
            return None if _id else []

    @database_connection
    def update_document(self, collection_name, document_id, update_data):
        if not isinstance(update_data, dict):
            logger.error("Invalid update data format. Data should be a dictionary.")
            return False

        document_id = self.process_id(document_id)
        if not document_id:
            return False

        try:
            collection = self.client[self.db_name][collection_name]
            result = collection.update_one({'_id': document_id}, {'$set': update_data})
            return result.matched_count > 0 and result.modified_count > 0
        except PyMongoError as e:
            logger.error(f"Error updating document in MongoDB {collection_name} collection: {e}")
            return False

    @database_connection
    def delete_document(self, collection_name, document_id):
        document_id = self.process_id(document_id)
        if not document_id:
            return False

        try:
            collection = self.client[self.db_name][collection_name]
            result = collection.delete_one({'_id': document_id})
            return result.deleted_count > 0
        except PyMongoError as e:
            logger.error(f"Error deleting document from MongoDB {collection_name} collection: {e}")


def init_db(context):
    if context and 'db' not in context:
        load_dotenv()
        context.db = Database()
    return context.db
