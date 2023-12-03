from flask import Flask, render_template, request, redirect, url_for, g

from utils.connection import Database

app = Flask(__name__)


def get_db():
    if 'db' not in g:
        g.db = Database()
    return g.db


@app.route('/')
def home_page():
    """Display the home page with the list of tasks."""
    db = get_db()
    return render_template('index.html', tasks=db.get_all_tasks())


# Route to display the form for adding a new task
@app.route('/task/new')
def show_new_task_form():
    """Display the form to add a new task."""
    modal_title = request.args.get('modal_title', 'Default Title')
    return render_template('new_task_form.html', modal_title=modal_title)


# Route to create a new task
@app.route('/task/create', methods=['POST'])
def add_new_task():
    """Add a new task and return the updated task list."""
    new_task = {"title": request.form['title']}
    db = get_db()
    db.add_task(new_task)
    return render_template('task_list.html', tasks=db.get_all_tasks())


# Route to display the form for editing a task
@app.route('/task/<string:task_id>/edit')
def show_edit_task_form(task_id):
    """Display the form to edit an existing task."""
    db = get_db()
    task = db.get_task(task_id)
    if task:
        return render_template('edit_task_form.html', task=task)
    return redirect(url_for('page_not_found'))


# Route to update a task
@app.route('/task/<string:task_id>/update', methods=['POST'])
def update_task(task_id):
    """Update an existing task and return the updated task list."""
    db = get_db()
    updated_title = request.form['title']
    db.update_task(task_id, {"title": updated_title})
    return render_template('task_list.html', tasks=db.get_all_tasks())


# Route dialog to delete a task
@app.route('/task/<string:task_id>/delete')
def show_delete_task_form(task_id):
    """Display the form to delete an existing task."""
    db = get_db()
    task = db.get_task(task_id)
    if task:
        return render_template('delete_task_form.html', task=task)
    return redirect(url_for('page_not_found'))


@app.route('/task/<string:task_id>/drop', methods=['DELETE'])
def delete_task(task_id):
    """Delete a task and return the updated task list."""
    db = get_db()
    db.delete_task(task_id)
    return render_template('task_list.html', tasks=db.get_all_tasks())


# Modal
@app.route('/modal')
def show_modal():
    return render_template('modal.html')


@app.route('/cancel')
def cancel():
    db = get_db()
    return render_template('task_list.html', tasks=db.get_all_tasks())


# Error handling for 404 Not Found
@app.errorhandler(404)
def page_not_found(e):
    print(e.__traceback__.tb_frame.f_code.co_filename)
    print(request.url)
    print(e)
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
