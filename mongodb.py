from flask import Flask, request, render_template, redirect, url_for

from utils.connection import Database

app = Flask(__name__)
db = Database()  # Instantiate the Database class


@app.route('/<string:collection>/<string:document>/', methods=['GET'])
@app.route('/<string:collection>/<string:document>/<string:action>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def manage_document(collection, document, action='READ'):
    context = {
        'collection': collection,
        'document': document,
        'action': action,
        'fields': request.args,
        'document_data': None
    }

    if action == 'CREATE' and request.method == 'POST':
        # Logic to handle document creation
        db.create_document(collection, request.form.to_dict())
        return redirect(url_for('manage_document', collection=collection, document='new', action='READ'))

    elif action == 'READ':
        # Logic to read and display a document
        raise NotImplementedError
        # context['document_data'] = db.read_document(document, collection)

    elif action == 'UPDATE' and request.method == 'POST':
        # Logic to update a document
        db.update_document(collection, document, request.form.to_dict())
        return redirect(url_for('manage_document', collection=collection, document=document, action='READ'))

    elif action == 'DELETE' and request.method == 'POST':
        # Logic to delete a document
        db.delete_document(collection, document)
        return redirect(url_for('manage_document', collection=collection, document='new', action='READ'))

    return render_template('documents/document_manager.html', **context)


if __name__ == '__main__':
    app.run(debug=True)
