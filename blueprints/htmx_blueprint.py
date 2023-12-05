from flask import Blueprint, render_template

from utils.connection import Database

htmx_blueprint = Blueprint('htmx', __name__)
htmx_blueprint.db = Database()


@htmx_blueprint.route('/')
def home_page():
    """Display the home page with the list of tasks."""
    return render_template(
        'index.html',
        documents=htmx_blueprint.db.read_documents("tasks"),
        collection="tasks")


@htmx_blueprint.route('/modal')
def show_modal():
    return render_template(
        'modal.html'
    )


@htmx_blueprint.route('/cancel')
def cancel():
    return render_template(
        'tasks/list.html',
        documents=htmx_blueprint.db.read_documents("tasks")
    )


@htmx_blueprint.route('/<string:collection>/new')
def show_new_form(collection):
    """Display the form to add a new document to a collection."""
    component = f"{collection}/new.html"
    view_title = f"New {collection.capitalize()[:-1]}"
    return render_template(
        component,
        title=view_title
    )


@htmx_blueprint.route('/<string:collection>/<string:document_id>/edit')
def show_edit_form(collection, document_id):
    """Display the form to edit an existing document."""
    component = f"{collection}/edit.html"
    document = htmx_blueprint.db.read_documents(collection, document_id)
    if document:
        return render_template(
            component,
            document=document
        )
    return render_template(
        'errors/404.html',
        message=f"Document with ID {document_id} not found in {collection}."
    )


@htmx_blueprint.route('/<string:collection>/<string:document_id>/delete')
def show_delete_form(collection, document_id):
    """Display the form to delete an existing document."""
    component = f"{collection}/delete.html"
    document = htmx_blueprint.db.read_documents(collection, document_id)
    if document:
        return render_template(
            component,
            document=document
        )
    return render_template(
        'errors/404.html',
        message=f"Document with ID {document_id} not found in {collection}."
    )


@htmx_blueprint.route('/users>')
@htmx_blueprint.route('/tasks')
def list_documents(collection):
    """List documents in a collection."""
    component = f"{collection}/list.html"
    documents = htmx_blueprint.db.read_documents(collection)
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
