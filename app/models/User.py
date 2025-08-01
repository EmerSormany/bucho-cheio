from ..db.database import get_db
from werkzeug.security import generate_password_hash

class User:
    def __init__(self, name, email, password, admin, matriculation, course):
        self.name = name
        self.email = email
        self.password = password
        self.admin = admin
        self.matriculation = matriculation
        self.course = course

    @staticmethod
    def hash_password(password):
        return generate_password_hash(password)

    def create_user(self):
        db = get_db()
        db.execute(
            'INSERT INTO usuarios (nome, email, senha_hash, administrador, matricula, curso) VALUES (?, ?, ?, ?, ?, ?)',
            (self.name, self.email, self.hash_password(self.password), self.admin, self.matriculation, self.course)
        )
        db.commit()

    @staticmethod
    def get_user_by_id(user_id):
        db = get_db()
        cursor = db.execute(
            'SELECT * FROM usuarios WHERE id = ?',
            (user_id,)
        )
        row = cursor.fetchone()
        if row:
            return {
                'id': row['id'],
                'name': row['nome'],
                'email': row['email'],
                'matriculation': row['matricula'],
                'course': row['curso'],
            }
        return None

