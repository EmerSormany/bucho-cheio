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
    
    # método para teste, deverá ser alterado
    @staticmethod
    def get_reservations_by_date():
        db = get_db()
        cursor = db.execute(
            'SELECT * FROM quadro_vagas WHERE data = ?',
        )
        return cursor.fetchall()

    @staticmethod
    def get_aplication_status(user_id, vacancy_id):
        db = get_db()
        cursor = db.execute(
            'SELECT situacao FROM reserva WHERE usuario_id = ? AND vaga_id = ?',
            (user_id, vacancy_id)
        )
        return cursor.fetchone()