from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

# create blueprint for blog post functions (index, create, update, delete)
bp = Blueprint('blog', __name__)


# create INDEX view to display all posts
@bp.route('/')
def index():
    db = get_db()
    # fetch all from post table and order to show most recent first
    # use JOIN to include author information from the user table in the result
    posts = db.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('blog/index.html', posts=posts)


# create CREATE view
@bp.route('/create', methods=('GET', 'POST'))
@login_required # redirect to login instead of 401 "Unauthorized"
def create():
    # process input if user submitted form
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None
	
	# validate title is not empty
        if not title:
            error = 'Title is required.'

	# show error message or add new post to db
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (title, body, author_id)'
                ' VALUES (?, ?, ?)',
                (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('blog.index'))
    
    # else display form
    return render_template('blog/create.html')


# helper function to get a post and optionally validate if author matches logged in user
# called in both UPDATE and DELETE views
def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(id)) # HTTP status code for "Not Found"

    if check_author and post['author_id'] != g.user['id']: 
        abort(403) # HTTP status code for "Forbidden"

    return post


# create UPDATE view
@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required # redirect to login instead of 401 "Unauthorized"
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
	    # similar to create view except uses UPDATE over INSERT
            db.execute(
                'UPDATE post SET title = ?, body = ?'
                ' WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)


# create DELETE view
# since there is no template, only handle the POST method then redirect
@bp.route('/<int:id>/delete', methods=('POST',))
@login_required # redirect to login instead of 401 "Unauthorized"
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('blog.index'))
