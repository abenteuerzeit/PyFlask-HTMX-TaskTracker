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

    def __init__(self):
        if not hasattr(self, '_initialized'):
            self.__connected = False
            self.__tasks = []
            self.__task_db = None
            self.__connect_to_mongodb()
            self._initialized = True
            atexit.register(self.__close_connection)

    def __connect_to_mongodb(self):
        load_dotenv()
        uri = os.getenv('MONGO_URI')
        if uri:
            try:
                self.__client = MongoClient(uri, server_api=ServerApi('1'))
                self.__client.admin.command('ping')
                self.__task_db = self.__client['tasktracker']['tasks']
                self.__connected = True
                print("Connected to MongoDB")
            except ConnectionFailure:
                self.__client = None
                self.__task_db = None
                self.__connected = False
                print("Failed to connect to MongoDB, using in-memory storage.")
        else:
            print("No MongoDB URI found, using in-memory storage.")

    def __close_connection(self):
        if self.__connected and self.__client:
            self.__client.close()
            print("MongoDB connection closed.")

    @staticmethod
    def process_id(id_value):
        try:
            return ObjectId(id_value)
        except Exception as e:
            print(f"Invalid ObjectId: {e}")
            return None

    def add_task(self, task):
        if not isinstance(task, dict):
            print("Invalid task format. Task should be a dictionary.")
            return None

        if self.__connected:
            try:
                result = self.__task_db.insert_one(task)
                return result.inserted_id
            except PyMongoError as e:
                print(f"Error adding task to MongoDB: {e}")
                return None
        else:
            task_id = ObjectId()
            task['_id'] = task_id
            self.__tasks.append(task)
            return task_id

    def get_task(self, task_id):
        task_id = self.process_id(task_id)
        if task_id is None:
            return None

        if self.__connected:
            try:
                return self.__task_db.find_one({'_id': task_id})
            except PyMongoError as e:
                print(f"Error retrieving task from MongoDB: {e}")
                return None
        else:
            return next((task for task in self.__tasks if task['_id'] == task_id), None)

    def update_task(self, task_id, update_data):
        if not isinstance(update_data, dict):
            print("Invalid update data format. Data should be a dictionary.")
            return False

        task_id = self.process_id(task_id)
        if task_id is None:
            return False

        if self.__connected:
            try:
                result = self.__task_db.update_one({'_id': task_id}, {'$set': update_data})
                return result.matched_count > 0 and result.modified_count > 0
            except PyMongoError as e:
                print(f"Error updating task in MongoDB: {e}")
                return False
        else:
            task = next((task for task in self.__tasks if task['_id'] == task_id), None)
            if not task:
                return False
            task.update(update_data)
            return True

    def delete_task(self, task_id):
        task_id = self.process_id(task_id)
        if task_id is None:
            return False

        if self.__connected:
            try:
                result = self.__task_db.delete_one({'_id': task_id})
                return result.deleted_count > 0
            except PyMongoError as e:
                print(f"Error deleting task from MongoDB: {e}")
                return False
        else:
            task = self.get_task(task_id)
            if task:
                self.__tasks.remove(task)
                return True
            return False

    def get_all_tasks(self):
        if self.__connected:
            try:
                return list(self.__task_db.find())
            except PyMongoError as e:
                print(f"Error retrieving all tasks from MongoDB: {e}")
                return []
        else:
            return self.__tasks
