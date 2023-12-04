from flask import Flask, render_template, request

from config import DevelopmentConfig
from utils.connection import Database

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
app.db = Database()


@app.route('/')
def home_page():
    """Display the home page with the list of tasks."""
    return render_template('index.html',
                           documents=app.db.read_documents("tasks"),
                           collection="tasks")


@app.route('/<string:collection>/new')
def show_new_form(collection):
    """Display the form to add a new document to a collection."""
    component = f"{collection}/new.html"
    view_title = f"New {collection.capitalize()[:-1]}"
    return render_template(component, title=view_title)


@app.route('/<string:collection>/create', methods=['POST'])
def create_document(collection):
    """Create a new document in a collection."""
    component = f"{collection}/list.html"
    document = request.form.to_dict()
    _id = app.db.create_document(collection, document)
    if not _id:
        print(f"Error creating new document in {collection}.")
        return render_template('errors/500.html', message=f"Error creating new document.")
    print(f"New document created in {collection} with ID: {_id}")
    documents = app.db.read_documents(collection)
    return render_template(component, documents=documents)


@app.route('/users>')
@app.route('/tasks')
def list_documents(collection):
    """List documents in a collection."""
    component = f"{collection}/list.html"
    documents = app.db.read_documents(collection)
    if collection == "tasks":
        return render_template(component, view={
            'title': 'Tasks',
            'collection': 'tasks',
            'documents': documents
        })
    elif collection == "users":
        return render_template(component, users=documents)
    return render_template('errors/404.html', message=f"Collection {collection} not found.")


@app.route('/<string:collection>/<string:document_id>/edit')
def show_edit_form(collection, document_id):
    """Display the form to edit an existing document."""
    component = f"{collection}/edit.html"
    document = app.db.read_documents(collection, document_id)
    if document:
        return render_template(component, document=document)
    return render_template('errors/404.html', message=f"Document with ID {document_id} not found in {collection}.")


@app.route('/<string:collection>/<string:document_id>/update', methods=['POST', 'PUT'])
def update_document(collection, document_id):
    """Update an existing document in a collection."""
    component = f"{collection}/list.html"
    update_data = request.form.to_dict()
    app.db.update_document(collection, document_id, update_data)
    return render_template(component, documents=app.db.read_documents(collection))


# show delete form
@app.route('/<string:collection>/<string:document_id>/delete')
def show_delete_form(collection, document_id):
    """Display the form to delete an existing document."""
    component = f"{collection}/delete.html"
    document = app.db.read_documents(collection, document_id)
    if document:
        return render_template(component, document=document)
    return render_template('errors/404.html', message=f"Document with ID {document_id} not found in {collection}.")


@app.route('/<string:collection>/<string:document_id>/drop', methods=['DELETE'])
def delete_document(collection, document_id):
    """Delete a document from a collection."""
    component = f"{collection}/list.html"
    app.db.delete_document(collection, document_id)
    return render_template(component, documents=app.db.read_documents(collection))


# Modal
@app.route('/modal')
def show_modal():
    return render_template('modal.html')


@app.route('/cancel')
def cancel():
    return render_template('tasks/list.html', documents=app.db.read_documents("tasks"))


if __name__ == '__main__':
    app.run(debug=True)
