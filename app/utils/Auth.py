from functools import wraps
from flask import session, render_template


class Auth:
    @staticmethod
    def login_required(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                return render_template('login.html', message="Você precisa estar logado para acessar esta página.")
            return f(*args, **kwargs)
        return decorated_function

    @staticmethod
    def admin_required(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if  'admin' not in session:
                return render_template('home.html', message="Acesso negado. Você precisa ser um administrador para acessar esta página.")
            return f(*args, **kwargs)
        return decorated_function
