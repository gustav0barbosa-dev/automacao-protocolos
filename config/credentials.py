import os
from dotenv import load_dotenv

load_dotenv()

class Credentials:
    USUARIO = os.getenv("SISTEMA_USUARIO")
    SENHA = os.getenv("SISTEMA_SENHA")

    @classmethod
    def validar(cls):
        if not cls.USUARIO or not cls.SENHA:
            raise ValueError("Credenciais não configuradas no .env")