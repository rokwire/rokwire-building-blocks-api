import click
from flask import current_app, g
from flask.cli import with_appcontext
from pymongo import MongoClient
from pymongo.errors import PyMongoError

from config import Config


def get_db():
    if 'dbclient' not in g:
        if current_app.config['DBTYPE'] == 'mongoDB':
            try:
                g.dbclient = MongoClient(Config['MONGO_URL'])
            except PyMongoError:
                print("MongoDB connection failed.")
                if 'dbclient' in g:
                    g.pop('dbclient', None)
                return None
            g.db = g.dbclient[Config.DB_NAME]
    return g.db


def close_db(e=None):
    if current_app.config['DBTYPE'] == 'mongoDB':
        g.pop('db', None)
        dbclient = g.pop('dbclient', None)
        if dbclient is not None:
            dbclient.close()


def init_db():
    db = get_db()
    # with current_app.open_resource('schema.sql') as f:
    #     db.executescript(f.read().decode('utf8'))


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')
