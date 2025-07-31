from ..db.database import get_db

class Vacancies:
    def __init__(self, date, vacancies):
        self.date = date
        self.vacancies = vacancies

    def create_vacancy(self):
        db = get_db()
        db.execute(
            'INSERT INTO quadro_vagas (data_vagas, quantidade) VALUES (?, ?)',
            (self.date, self.vacancies)
        )
        db.commit()
        return 
    
    @staticmethod
    def get_vacancies_by_date(date):
        db = get_db()
        cursor = db.execute(
            'SELECT id FROM quadro_vagas WHERE data_vagas = ?',
            (date,)
        ).fetchone()
        if cursor:
            return cursor['id']
        return None