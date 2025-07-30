from flask import Blueprint, render_template, request, session
from flask.views import MethodView
from .models.User import User
from .models.Login import Login

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
            if Login.get_user_by_email(email):
                return render_template('user.html', message="Email já cadastrado.")

            new_user = User(name, email, password, admin, matriculation, course)
            new_user.create_user()

            return render_template('index.html', message="Cadastrado com sucesso!")
        except Exception as e:
            return str(e), 500
            # return 'Erro no servidor', 500
        
bp.add_url_rule('/user', view_func=UserView.as_view('user'))

class LoginView(MethodView):
    def get(self):
        return render_template('login.html')

    def post(self):
        email = request.form.get('email')
        password = request.form.get('password')

        try:
            found_user = Login.get_user_by_email(email)

            if not found_user:
                return render_template('login.html', message="Dados inválidos.")

            user = Login.login(found_user, password)

            if user:
                session['user_id'] = user['id']

                if user['admin'] == 1:
                    session['admin'] = user['admin']

                # alterar retorno render_template para páginas de acorodo por tipo de usuário
                return render_template('index.html', message="Login realizado com sucesso!")
            else:
                return render_template('login.html', message="Email ou senha inválidos.")
        except Exception as e:
            print(f"Erro ao realizar login: {e}")
            return str(e), 500
            # return 'Erro no servidor', 500

bp.add_url_rule('/login', view_func=LoginView.as_view('login'))

class LogoutView(MethodView):
    def post(self):
        session.pop('user_id', None)
        session.pop('admin', None)
        return render_template('index.html', message="Logout realizado com sucesso!")
    
bp.add_url_rule('/logout', view_func=LogoutView.as_view('logout'))