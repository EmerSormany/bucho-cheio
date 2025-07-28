from flask import Flask
from .db.database import init_db, close_db

def create_app():
    app = Flask(__name__)
    app. config.from_object('config.Config')

    with app.app_context():
        init_db(app)

    from . import routes
    app.register_blueprint(routes.bp)  

    app.teardown_appcontext(close_db)

    return app