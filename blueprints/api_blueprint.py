from flask import Blueprint, render_template, request, current_app

api = Blueprint('api', __name__)


@api.route('/users>')
@api.route('/tasks')
def list_documents(collection):
    """List documents in a collection."""
    component = f"{collection}/list.html"
    documents = current_app.db.read_documents(collection)
    if collection == "tasks":
        return render_template(
            component,
            view={
                'title': 'Tasks',
                'collection': 'tasks',
                'documents': documents
            })
    elif collection == "users":
        return render_template(
            component,
            users=documents
        )
    return render_template(
        'errors/404.html',
        message=f"Collection {collection} not found."
    )


@api.route('/<string:collection>/create', methods=['POST'])
def create_document(collection):
    """Create a new document in a collection."""
    component = f"{collection}/list.html"
    document = request.form.to_dict()
    _id = current_app.db.create_document(collection, document)
    if not _id:
        print(f"Error creating a new document in {collection}.")
        return render_template(
            'errors/500.html',
            message=f"Error creating a new document."
        )
    print(f"New document created in {collection} with ID: {_id}")
    documents = current_app.db.read_documents(collection)
    return render_template(
        component, documents=documents
    )


@api.route('/<string:collection>/<string:document_id>/update', methods=['POST', 'PUT'])
def update_document(collection, document_id):
    """Update an existing document in a collection."""
    component = f"{collection}/list.html"
    update_data = request.form.to_dict()
    current_app.db.update_document(collection, document_id, update_data)
    return render_template(
        component,
        documents=current_app.db.read_documents(collection)
    )


@api.route('/<string:collection>/<string:document_id>/drop', methods=['DELETE'])
def delete_document(collection, document_id):
    """Delete a document from a collection."""
    component = f"{collection}/list.html"
    current_app.db.delete_document(
        collection, document_id
    )
    return render_template(
        component,
        documents=current_app.db.read_documents(collection)
    )
