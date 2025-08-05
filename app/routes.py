from flask import Blueprint, render_template, request, session
from flask.views import MethodView
from .models.User import User
from .models.Login import Login
from .models.Vacancies import Vacancies
from .models.Reservation import Reservation
from .models.Admin import Admin
from .utils.Auth import Auth
from .utils.QRcode import QRCode
from datetime import date, timedelta

bp = Blueprint('main', __name__)

class IndexView(MethodView):
    def get(self):
        return render_template('index.html')

bp.add_url_rule('/', view_func=IndexView.as_view('index'))

class UserView(MethodView):
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

# rota de cadastro de usuário  
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
                    return render_template('panel.html', message="Painel da administração.")

                return render_template('home.html', message="Login realizado com sucesso!")
            else:
                return render_template('login.html', message="Dados inválidos.")
        except Exception as e:
            return str(e), 500
            # return 'Erro no servidor', 500

# rota de login
bp.add_url_rule('/login', view_func=LoginView.as_view('login'))

class LogoutView(MethodView):
    def post(self):
        session.pop('user_id', None)
        session.pop('admin', None)
        return render_template('index.html', message="Logout realizado com sucesso!")
    
# rota de logout
bp.add_url_rule('/logout', view_func=LogoutView.as_view('logout'))

class HomeView(MethodView):
    @Auth.login_required
    def get(self):
        return render_template('home.html')
    
# rota do usuário comum
bp.add_url_rule('/home', view_func=HomeView.as_view('home'))

class VacanciesView(MethodView):
    @Auth.login_required
    @Auth.admin_required
    def get(self):
        return render_template('vacancies.html')

    @Auth.login_required
    @Auth.admin_required
    def post(self):
        date = request.form.get('date')
        quantity = request.form.get('quantity')

        try:
            new_vacancy = Vacancies(date, quantity)
            new_vacancy.create_vacancy()
            return render_template('vacancies.html', message="Vagas criadas com sucesso!")
        except Exception as e:
            return str(e), 500
            # return 'Erro no servidor', 500

# rota para cadastrar vagas, apenas para admin
bp.add_url_rule('/vacancies', view_func=VacanciesView.as_view('vacancies'))

class ReservationView(MethodView):
    @Auth.login_required
    def get(self):
        user = User.get_user_by_id(session.get('user_id'))
        return render_template('reservation.html', user=user)

    @Auth.login_required
    def post(self):
        user_id = session.get('user_id')
        try:
            tomorrow = date.today() + timedelta(days=1)
            id_vacancy = Vacancies.get_vacancies_by_date(tomorrow.strftime('%Y-%m-%d'))

            if id_vacancy is None:
                return render_template('reservation.html', message="Não há vagas disponíveis para amanhã.")
            
            qr_code = QRCode.generate_qr_code(user_id, id_vacancy)
            reservation = Reservation(user_id, id_vacancy, qr_code)
            reservation.save()

            return render_template('reservation.html', message="Reserva realizada com sucesso!")

        except Exception as e:
            return render_template('reservation.html', message="Você já possui uma reserva para amanhã.")
            # return 'Erro no servidor', 500

#  rota para se candidatar a uma vaga
bp.add_url_rule('/reservation', view_func=ReservationView.as_view('reservation'))

class AdminView(MethodView):
    @Auth.login_required
    @Auth.admin_required
    def get(self):
        date = request.args.get('date')

        if date:
            try:
                reservations = Admin.list_applications_by_date(date)

                if not reservations:
                    return render_template('panel.html', message="Nenhuma candidatura encontrada para esta data.")
                return render_template('panel.html', data=reservations, date=date)
            except Exception as e:
                return str(e), 500
                # return 'Erro no servidor', 500
        else:
            return render_template('panel.html')
    
    @Auth.login_required
    @Auth.admin_required
    def post(self):
        total = int(request.form.get('total_lines'))

        for i in range(1, total + 1):
            user_id = request.form.get(f'user_id_{i}')
            vacancy_id = request.form.get(f'vacancy_id_{i}')
            new_situation = request.form.get(f'new_situation_{i}')

            try:
                current_status = Reservation.get_aplication_status(user_id, vacancy_id)
                if new_situation == 'ativa' and (current_status['situacao'] == 'pendente' or current_status['situacao'] == 'cancelada'):
                    Admin.approve_application(user_id, vacancy_id)
                elif new_situation == 'cancelada' and current_status['situacao'] == 'ativa':
                    Admin.deny_application_aproved(user_id, vacancy_id)
                elif new_situation == 'cancelada' and current_status['situacao'] == 'pendente':
                    Admin.deny_application(user_id, vacancy_id)
            except Exception as e:
                return str(e), 500
                # return 'Erro no servidor', 500

        return render_template('panel.html', message="Reservas atualizadas com sucesso!")

# rota do painel de administração 
bp.add_url_rule('/admin', view_func=AdminView.as_view('admin'))