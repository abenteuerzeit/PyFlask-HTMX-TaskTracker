import atexit
import logging
import os

from bson import ObjectId
from bson.errors import InvalidId
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, PyMongoError

from utils.connection import database_connection

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DEFAULT_URI = "mongodb://localhost:27017/"


class Database:
    """Database class for handling MongoDB operations."""

    def __init__(self, database_name="tasktracker"):
        """Initialize the database with a given name."""
        self.db_name = database_name
        self.client = None
        self.collections = []
        self.initialize_db()

    def get_uri(self, uris):
        """Return the first valid URI from a list of URIs."""
        for uri in uris:
            if uri:
                return uri
        return None

    def initialize_db(self, uris=None):
        """Initialize the database connection."""
        if self.client:
            return self.client

        uris = uris if uris else [
            os.getenv('MONGO_URI'),
            f"{DEFAULT_URI}{self.db_name}"
        ]
        for uri in uris:
            if not uri:
                continue

            try:
                self.client = MongoClient(uri)
                self.client.admin.command('ping')
                db = self.client[self.db_name]
                self.collections = db.list_collection_names()
                atexit.register(self.close_connection)
                logger.info("Connected to MongoDB using URI: %s", uri)
                break
            except ConnectionFailure:
                logger.error("Failed to connect to %s, trying next...", uri)
            except IndexError:
                logger.warning("No valid URIs available.")

    def close_connection(self):
        """Close the database connection."""
        if self.client:
            self.client.close()
            self.client = None
            logger.info("Database connection closed.")

    @staticmethod
    def process_id(id_value):
        """Convert a string to an ObjectId, if possible."""
        try:
            return ObjectId(id_value)
        except InvalidId as e:
            logger.error("Invalid ObjectId: %s", e)
            return None

    def execute_db_operation(self, collection_name, operation, *args):
        """Execute a database operation safely."""
        try:
            if self.client is None:
                raise ConnectionFailure("Not connected to MongoDB.")
            collection = self.client[self.db_name][collection_name]
            return operation(collection, *args)
        except ConnectionFailure as e:
            logger.error("Error connecting to database: %s", e)
        except PyMongoError as e:
            logger.error("Database operation error: %s", e)
        except InvalidId as e:
            logger.error("Invalid ObjectId: %s", e)
        return None

    @database_connection
    def create_document(self, collection_name, new_document):
        """Create a new document in the specified collection."""
        if not isinstance(new_document, dict):
            logger.error("Document should be a dictionary.")
            return None

        def insert_document(collection, document):
            return collection.insert_one(document).inserted_id

        return self.execute_db_operation(
            collection_name,
            insert_document,
            new_document
        )

    @database_connection
    def read_documents(self, collection_name, _id=None):
        """Read documents from the specified collection."""
        def find_document(collection, document_id):
            query = {'_id': document_id} if document_id else {}
            return list(collection.find(query))

        original_id = _id
        _id = self.process_id(_id) if _id else None
        if original_id is not None and _id is None:
            logger.error("Invalid ObjectId.")
            return None

        return self.execute_db_operation(collection_name, find_document, _id)
    
    @database_connection
    def update_document(self, collection_name, document_id, update_data):
        """Update a document in the specified collection."""
        if not isinstance(update_data, dict):
            logger.error("Data should be a dictionary.")
            return False

        document_id = self.process_id(document_id)
        if not document_id:
            return False

        def update_doc(collection, doc_id, data):
            result = collection.update_one({'_id': doc_id}, {'$set': data})
            return result.matched_count > 0 and result.modified_count > 0

        return self.execute_db_operation(
            collection_name,
            update_doc,
            document_id,
            update_data
        )

    @database_connection
    def delete_document(self, collection_name, document_id):
        """Delete a document from the specified collection."""
        document_id = self.process_id(document_id)
        if not document_id:
            return False

        def delete_doc(collection, doc_id):
            result = collection.delete_one({'_id': doc_id})
            return result.deleted_count > 0

        return self.execute_db_operation(
            collection_name,
            delete_doc,
            document_id
        )


def init_db(context):
    """Initialize the database within a given context."""
    if context and 'db' not in context:
        load_dotenv()
        context.db = Database()
    return context.db
