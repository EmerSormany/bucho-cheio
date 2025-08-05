from flask import Flask
from .db.database import init_db, close_db
from . import routes
from .utils.Auth import Auth

def create_app():
    app = Flask(__name__)
    app. config.from_object('config.Config')

    with app.app_context():
        init_db(app)

    app.before_request(Auth.load_logged_user)

    app.register_blueprint(routes.bp)  

    app.teardown_appcontext(close_db)

    return app