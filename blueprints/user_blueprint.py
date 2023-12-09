import logging
from datetime import datetime

import bcrypt
from flask import Blueprint, current_app, request, render_template, session

user = Blueprint('user', __name__)


@user.route('/users/signup', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'GET':
        return render_template('users/create.html', title="New User")
    user_data = request.form.to_dict()
    session['user_id'] = str(current_app.db.create_document('users', {
        'created_at': datetime.now(),
        'username': user_data['username'],
        'password': bcrypt.hashpw(user_data['password'].encode('utf-8'), bcrypt.gensalt())
    }))
    if not session['user_id']:
        return f"Error creating user: {user_data['username']}", 400
    session['username'] = user_data['username']
    logging.info(f"sign_up = () => {session['username']}")
    return render_template('navbar.html')
    # TODO: return render_template('users/signup_success.html', new_user=new_user, links=links)


@user.route('/users/login', methods=['GET', 'POST'])
def login():
    logging.info(f"login = () => users/login.html")
    if request.method == 'GET':
        return render_template('users/login.html', title="Login")
    login_data = request.form.to_dict()
    user_data = current_app.db.read_documents('users', login_data['username'])
    if user_data and bcrypt.checkpw(login_data['password'].encode('utf-8'), user_data['password']):
        session['user_id'] = str(user_data['_id'])
        session['username'] = user_data['username']
        return render_template('navbar.html')
    return "Username or password incorrect')", 400
    # TODO: return render_template('users/login_fail.html')


@user.route('/users/<string:user_id>/logout')
def logout(user_id):
    print(f"logout = ({user_id}) => {session['username']}")
    session.clear()
    return render_template('navbar.html')

# TODO: Read user

# TODO: Update user

# TODO: Delete user
