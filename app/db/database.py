import sqlite3
from flask import g, current_app

class Database:
    def __init__(self, db_path):
        self.db_path = db_path

    def get_db_connection(self):
        if 'db' not in g:
            g.db = sqlite3.connect(self.db_path)
            g.db.row_factory = sqlite3.Row
        return g.db

    def close_db(self, exception=None):
        db = g.pop('db', None)
        if db is not None:
            db.close()

    def init_db_schema(self, app):
        with current_app.app_context():
            db = self.get_db_connection()
            with current_app.open_resource('db/schema.sql', mode='r', encoding='utf-8') as f:
                db.executescript(f.read())
            db.commit()

db = Database(None)

def get_db():
    return db.get_db_connection()

def close_db(exception=None):
    db.close_db(exception)

def init_db(app):
    db.db_path = app.config['DATABASE']
    db.init_db_schema(app)