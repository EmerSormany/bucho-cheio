from ..db.database import get_db
from werkzeug.security import check_password_hash

class Login:
    @staticmethod
    def login(user, password):
        if check_password_hash(user['senha_hash'], password):
            return {
                'id': user['id'],
                'name': user['nome'],
                'email': user['email'],
                'admin': user['administrador']
            }
        return None
    
    @staticmethod
    def get_user_by_email(email):
        db = get_db()
        cursor = db.execute(
            'SELECT * FROM usuarios WHERE email = ?',
            (email,)
        )
        return cursor.fetchone()
