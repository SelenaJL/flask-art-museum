import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

# create blueprint for authentication functions (register, login, logout)
bp = Blueprint('auth', __name__, url_prefix='/auth')


# create REGISTER view
@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST': # user submitted the form
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
	
	# validate input is not empty
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
	# validate username is not already registered
        elif db.execute(
            'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = 'User {} is already registered.'.format(username)
	
	# insert new user data into db
	# do not store password directly, securely hash
        if error is None:
            db.execute(
                'INSERT INTO user (username, password) VALUES (?, ?)',
                (username, generate_password_hash(password))
            )
            db.commit()
	    # generate URL based on the endpoint to allow for URL changes in the future
            return redirect(url_for('auth.login')) # redirect to login page

        flash(error)

    return render_template('auth/register.html')


# create LOGIN view
@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST': # user submitted the form
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

	# query for user data
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

	# verify user exists
        if user is None:
            error = 'Incorrect username.'
	# verify password matches
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear() # session is a dict that stores data across requests
            session['user_id'] = user['id'] # user data will now be available on subsequent requests
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')


# register function to fun before the view funtions,, no matter the requested URL
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id') # check if user data is tored

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()


# create LOGOUT view
@bp.route('/logout')
def logout():
    session.clear() # remove user data from existing session
    return redirect(url_for('index'))


# decorator to check if a user is logged in for blog views
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
	# if no user is loaded, redirect to the login page
	# otherwise, the original view is called
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
