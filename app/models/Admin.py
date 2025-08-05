from ..db.database import get_db

class Admin:
    @staticmethod
    def list_applications_by_date(data):
        db = get_db()
        query = """
            SELECT
                u.id AS usuario_id,
                u.nome,
                u.email,
                u.matricula,
                u.curso,
                r.vaga_id,
                r.situacao,
                qv.data_vagas,
                qv.quantidade
            FROM reserva r
            JOIN usuarios u ON u.id = r.usuario_id
            JOIN quadro_vagas qv ON qv.id = r.vaga_id
            WHERE qv.data_vagas = ?
        """
        return db.execute(query, (data,)).fetchall()
    
    @staticmethod
    def approve_application(usuario_id, vaga_id):
        db = get_db()
        db.execute("""
            UPDATE reserva
            SET situacao = 'ativa'
            WHERE usuario_id = ? AND vaga_id = ?
        """, (usuario_id, vaga_id))

        db.execute("""
            UPDATE quadro_vagas
            SET quantidade = quantidade - 1
            WHERE id = ?
        """, (vaga_id,))

        db.commit()

    @staticmethod
    def deny_application(usuario_id, vaga_id):
        db = get_db()
        db.execute("""
            UPDATE reserva
            SET situacao = 'cancelada'
            WHERE usuario_id = ? AND vaga_id = ?
        """, (usuario_id, vaga_id))
        db.commit()

    @staticmethod
    def deny_application_aproved(usuario_id, vaga_id):
        db = get_db()
        db.execute("""
            UPDATE reserva
            SET situacao = 'cancelada'
            WHERE usuario_id = ? AND vaga_id = ?
        """, (usuario_id, vaga_id))

        db.execute("""
            UPDATE quadro_vagas
            SET quantidade = quantidade + 1
            WHERE id = ?
        """, (vaga_id,))

        db.commit()

