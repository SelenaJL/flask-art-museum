import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    # g is unique for each request and stores data that can be accessed by multiple functions during the request
    # store and reuse the connection if get_db() is called again in the same request
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
	# return rows that behave like dicts to accessc cols by name
        g.db.row_factory = sqlite3.Row 

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()

    # open_resource() opens a file relative to the flaskr package
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


# create cli cmd for user to call init_db()
@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


# register funtions with the app instance
def init_app(app):
    app.teardown_appcontext(close_db) # call close_db() after returning a response
    app.cli.add_command(init_db_command) # allow calling with flask cmd
