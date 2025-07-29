import os

class Config:
    """
    Classe de configurações base para a aplicação Flask.
    """

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'minha_chave_padrao_para_desenvolvimento'

    DATABASE = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'app', 'db', 'database.db')