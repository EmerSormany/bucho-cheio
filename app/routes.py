from flask import Blueprint, render_template, request
from flask.views import MethodView
from .models.User import User

bp = Blueprint('main', __name__)

class IndexView(MethodView):
    def get(self):
        return render_template('index.html')

bp.add_url_rule('/', view_func=IndexView.as_view('index'))

class UserView(MethodView):
    # concluir, verificar controle de rota por tipo de usuário
    def get(self):
        return render_template('user.html')
    
    def post(self):
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        matriculation = request.form.get('matriculation')
        course = request.form.get('course')
        admin = request.form.get('admin')

        admin = 1 if admin == 'on' else 0

        try:
            new_user = User(name, email, password, admin, matriculation, course)
            new_user.create_user()
            return render_template('index.html', message="Cadastrado com sucesso!")
        except Exception as e:
            # return str(e), 500
            return 'Erro no servidor', 500
        
bp.add_url_rule('/user', view_func=UserView.as_view('user'))