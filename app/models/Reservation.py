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
    def get_aplication_status(user_id, vacancy_id):
        db = get_db()
        cursor = db.execute(
            'SELECT situacao FROM reserva WHERE usuario_id = ? AND vaga_id = ?',
            (user_id, vacancy_id)
        )
        return cursor.fetchone()

    @staticmethod
    def get_reservation(user_id):
        db = get_db()
        cursor = db.execute(
        """
        SELECT
            r.situacao,
            r.qr_code,
            qv.data_vagas
        FROM reserva AS r
        JOIN quadro_vagas AS qv ON r.vaga_id = qv.id
        WHERE r.usuario_id = ?
        """,
        (user_id,))
        row = cursor.fetchone()
        return {
            'status': row['situacao'],
            'qr_code': row['qr_code'],
            'data_vagas': row['data_vagas']
        } if row else None