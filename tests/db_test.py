import os
from unittest.mock import Mock, patch

import pytest
from pymongo.errors import ConnectionFailure, PyMongoError

from mongodb import Database

MONGO_CLIENT = "mongodb.MongoClient"


@pytest.fixture(autouse=True)
def mock_env_vars():
    with patch.dict(os.environ, {'MONGO_URI': 'mongodb://localhost:27017/testdb'}):
        yield


@pytest.fixture
def test_database(mock_mongo_client):
    with patch(MONGO_CLIENT, return_value=mock_mongo_client):
        return Database(database_name="testdb")


@pytest.fixture
def mock_mongo_client():
    mock_collection = Mock()
    mock_db = Mock()
    mock_db.__getitem__ = Mock(return_value=mock_collection)
    mock_db.list_collection_names.return_value = ['collection1', 'collection2']
    mock_collection.find.return_value = iter([{"_id": 1, "name": "doc1"}, {"_id": 2, "name": "doc2"}])
    mock_collection.update_one.return_value = Mock(matched_count=1, modified_count=1)
    mock_collection.delete_one.return_value = Mock(deleted_count=1)
    mock_client = Mock()
    mock_client.__getitem__ = Mock(return_value=mock_db)
    mock_client.admin.command.return_value = {'ok': 1.0}
    return mock_client


def test_database_init(test_database):
    assert test_database.db_name == "testdb"
    assert test_database.client is not None


def test_initialize_db_successful(test_database, mock_mongo_client):
    test_database.initialize_db()
    assert test_database.client is not None


def test_initialize_db_failure(mock_env_vars, mock_mongo_client):
    with patch(MONGO_CLIENT) as mock_client:
        mock_client.side_effect = [ConnectionFailure("Connection failed"), mock_mongo_client]

        db = Database(database_name="testdb")
        assert db.client is not None


def test_close_connection(test_database):
    test_database.close_connection()
    assert test_database.client is None


def test_process_id_valid(test_database):
    valid_id = "507f1f77bcf86cd799439011"
    result = test_database.process_id(valid_id)
    assert result is not None


def test_process_id_invalid(test_database):
    invalid_id = "invalid"
    result = test_database.process_id(invalid_id)
    assert result is None


def test_create_document(test_database, mock_mongo_client):
    new_document = {"name": "Test", "value": 123}
    collection_name = "test_collection"
    result = test_database.create_document(collection_name, new_document)
    assert result is not None


def test_read_documents(test_database, mock_mongo_client):
    collection_name = "test_collection"
    documents = test_database.read_documents(collection_name)
    assert isinstance(documents, list)


def test_read_documents_with_id(test_database, mock_mongo_client):
    collection_name = "test_collection"
    test_id = "507f1f77bcf86cd799439011"
    document = test_database.read_documents(collection_name, test_id)
    assert document is not None


def test_update_document(test_database, mock_mongo_client):
    collection_name = "test_collection"
    document_id = "507f1f77bcf86cd799439011"
    update_data = {"name": "Updated Test"}
    result = test_database.update_document(collection_name, document_id, update_data)
    assert result


def test_delete_document(test_database, mock_mongo_client):
    collection_name = "test_collection"
    document_id = "507f1f77bcf86cd799439011"
    result = test_database.delete_document(collection_name, document_id)
    assert result


def test_create_document_invalid_input(test_database):
    invalid_document = "not a dictionary"
    collection_name = "test_collection"
    result = test_database.create_document(collection_name, invalid_document)
    assert result is None


def test_read_documents_invalid_id(test_database):
    collection_name = "test_collection"
    invalid_id = "invalid"
    document = test_database.read_documents(collection_name, invalid_id)
    assert document is None


def test_update_document_invalid_data(test_database):
    collection_name = "test_collection"
    document_id = "507f1f77bcf86cd799439011"
    invalid_update_data = "not a dictionary"
    result = test_database.update_document(collection_name, document_id, invalid_update_data)
    assert not result


# Test delete_document with invalid ID
def test_delete_document_invalid_id(test_database):
    collection_name = "test_collection"
    invalid_id = "invalid"
    result = test_database.delete_document(collection_name, invalid_id)
    assert not result


def test_pymongo_error_handling(test_database, mock_mongo_client):
    mock_mongo_client.__getitem__.return_value.list_collection_names.side_effect = PyMongoError
    mock_mongo_client.__getitem__.return_value.__getitem__.return_value.insert_one.side_effect = PyMongoError
    mock_mongo_client.__getitem__.return_value.__getitem__.return_value.find_one.side_effect = PyMongoError
    mock_mongo_client.__getitem__.return_value.__getitem__.return_value.find.side_effect = PyMongoError
    mock_mongo_client.__getitem__.return_value.__getitem__.return_value.update_one.side_effect = PyMongoError
    mock_mongo_client.__getitem__.return_value.__getitem__.return_value.delete_one.side_effect = PyMongoError

    assert test_database.create_document("test_collection", {"name": "Test"}) is None
    assert test_database.read_documents("test_collection") is None
    assert not test_database.update_document("test_collection", "507f1f77bcf86cd799439011", {"name": "Updated"})
    assert not test_database.delete_document("test_collection", "507f1f77bcf86cd799439011")


def test_connection_failure_handling(mock_env_vars):
    with patch(MONGO_CLIENT) as mock_client:
        mock_client.side_effect = [ConnectionFailure("Connection failure"), IndexError("Index error")]
        db = Database(database_name="testdb")
        assert db.client is None


if __name__ == '__main__':
    pytest.main()
