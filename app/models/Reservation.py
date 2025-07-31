from ..db.database import get_db

class Reservation:
    def __init__(self, user_id, vacancy_id, qr_code):
        self.user_id = user_id
        self.vacancy_id = vacancy_id
        self.qr_code = qr_code
        self.status = 'pendente'

    def save(self):
        db = get_db()
        db.execute(
            "INSERT INTO reserva (usuario_id, vaga_id, situacao, qr_code) VALUES (?, ?, ?, ?)",
            (self.user_id, self.vacancy_id, self.status, self.qr_code)
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
    
    # método para teste, deverá ser removido ou alterado
    @staticmethod
    def get_reservations():
        db = get_db()
        cursor = db.execute(
            'SELECT * FROM reserva'
        )
        return cursor.fetchall()