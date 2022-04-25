import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext
from sales import data


def get_db():
    """Get or create a connection to the database."""
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    """Close the connection to the database."""
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    """Initialize the database for the app."""
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

    # load and populate data
    data.load_all_data(db)


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    """Register the database to the app."""
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)