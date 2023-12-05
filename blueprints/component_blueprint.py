from flask import Blueprint, render_template, current_app

component = Blueprint('component', __name__)


@component.route('/')
def home_page():
    """Display the home page with the list of tasks."""
    tasks = current_app.db.read_documents("tasks")
    return render_template(
        'index.html',
        documents=tasks,
        collection="tasks"
    )


@component.route('/modal')
def show_modal():
    return render_template(
        'modal.html'
    )


@component.route('/cancel')
def cancel():
    return render_template(
        'tasks/list.html',
        documents=current_app.db.read_documents("tasks")
    )


@component.route('/<string:collection>/new')
def show_new_form(collection):
    """Display the form to add a new document to a collection."""
    add_to_collection_form = f"{collection}/new.html"
    view_title = f"New {collection.capitalize()[:-1]}"
    return render_template(
        add_to_collection_form,
        title=view_title
    )


@component.route('/<string:collection>/<string:document_id>/edit')
def show_edit_form(collection, document_id):
    """Display the form to edit an existing document."""
    edit_collection_form = f"{collection}/edit.html"
    document = current_app.db.read_documents(collection, document_id)
    if document:
        return render_template(
            edit_collection_form,
            document=document
        )
    return render_template(
        'errors/404.html',
        message=f"Document with ID {document_id} not found in {collection}."
    )


@component.route('/<string:collection>/<string:document_id>/delete')
def show_delete_form(collection, document_id):
    """Display the form to delete an existing document."""
    delete_collection_form = f"{collection}/delete.html"
    document = current_app.db.read_documents(collection, document_id)
    if document:
        return render_template(
            delete_collection_form,
            document=document
        )
    return render_template(
        'errors/404.html',
        message=f"Document with ID {document_id} not found in {collection}."
    )

