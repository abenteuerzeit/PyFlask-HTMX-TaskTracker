from flask import Blueprint, render_template, request

from utils.connection import Database

api_blueprint = Blueprint('api', __name__)
api_blueprint.db = Database()


@api_blueprint.route('/<string:collection>/create', methods=['POST'])
def create_document(collection):
    """Create a new document in a collection."""
    component = f"{collection}/list.html"
    document = request.form.to_dict()
    _id = api_blueprint.db.create_document(collection, document)
    if not _id:
        print(f"Error creating new document in {collection}.")
        return render_template(
            'errors/500.html',
            message=f"Error creating new document."
        )
    print(f"New document created in {collection} with ID: {_id}")
    documents = api_blueprint.db.read_documents(collection)
    return render_template(
        component, documents=documents
    )


@api_blueprint.route('/<string:collection>/<string:document_id>/update', methods=['POST', 'PUT'])
def update_document(collection, document_id):
    """Update an existing document in a collection."""
    component = f"{collection}/list.html"
    update_data = request.form.to_dict()
    api_blueprint.db.update_document(collection, document_id, update_data)
    return render_template(
        component,
        documents=api_blueprint.db.read_documents(collection)
    )


@api_blueprint.route('/<string:collection>/<string:document_id>/drop', methods=['DELETE'])
def delete_document(collection, document_id):
    """Delete a document from a collection."""
    component = f"{collection}/list.html"
    api_blueprint.db.delete_document(
        collection, document_id
    )
    return render_template(
        component,
        documents=api_blueprint.db.read_documents(collection)
    )
