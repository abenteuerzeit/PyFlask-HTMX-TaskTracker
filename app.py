from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# In-memory database setup (a simple list)
tasks = []


# Utility function to find a task by ID
def get_task(task_id):
    return next((task for task in tasks if task['id'] == task_id), None)


# Utility function to generate a new task ID
def generate_new_task_id():
    return max(task['id'] for task in tasks) + 1 if tasks else 1


# Home page route
@app.route('/')
def home_page():
    """Display the home page with the list of tasks."""
    return render_template('index.html', tasks=tasks)


# Route to display the form for adding a new task
@app.route('/task/new')
def show_new_task_form():
    """Display the form to add a new task."""
    modal_title = request.args.get('modal_title', 'Default Title')
    return render_template('new_task_form.html', modal_title=modal_title)


# Route to create a new task
@app.route('/task/create', methods=['POST'])
def add_new_task():
    """Create a new task and return the updated task list."""
    new_id = generate_new_task_id()
    new_task = {"id": new_id, "title": request.form['title']}
    tasks.append(new_task)
    return render_template('task_list.html', tasks=tasks)


# Route to display the form for editing a task
@app.route('/task/<int:task_id>/edit')
def show_edit_task_form(task_id):
    """Display the form to edit an existing task."""
    task = get_task(task_id)
    if task:
        return render_template('edit_task_form.html', task=task)
    return redirect(url_for('page_not_found'))


# Route to update a task
@app.route('/task/<int:task_id>/update', methods=['POST'])
def update_task(task_id):
    """Update an existing task and return the updated task list."""
    task = get_task(task_id)
    if task:
        task['title'] = request.form['title']
        return render_template('task_list.html', tasks=tasks)
    return redirect(url_for('page_not_found'))


# Route dialog to delete a task
@app.route('/task/<int:task_id>/delete')
def show_delete_task_form(task_id):
    """Display the form to delete an existing task."""
    task = get_task(task_id)
    if task:
        return render_template('delete_task_form.html', task=task)
    return redirect(url_for('page_not_found'))


@app.route('/task/<int:task_id>/drop', methods=['DELETE'])
def delete_task(task_id):
    """Delete a task and return the updated task list."""
    task = get_task(task_id)
    if task:
        tasks.remove(task)
        return render_template('task_list.html', tasks=tasks)
    return redirect(url_for('page_not_found'))


# Modal
@app.route('/modal')
def show_modal():
    return render_template('modal.html')


@app.route('/cancel')
def cancel():
    return render_template('task_list.html', tasks=tasks)


# Error handling for 404 Not Found
@app.errorhandler(404)
def page_not_found(e):
    print(e)
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
