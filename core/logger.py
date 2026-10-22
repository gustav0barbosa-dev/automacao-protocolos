import logging
import os

def get_logger(name: str) -> logging.Logger:
    # Garante que a pasta 'logs' exista no projeto
    if not os.path.exists('logs'):
        os.makedirs('logs')

    logger = logging.getLogger(name)

    # Se o logger já foi configurado, apenas o retorna (evita mensagens duplicadas)
    if not logger.handlers:
        logger.setLevel(logging.INFO)

        # Formato da mensagem: Data - Nome do arquivo - Nível - Mensagem
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # 1. Handler para mostrar no terminal
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        # 2. Handler para salvar no arquivo logs/automacao.log
        file_handler = logging.FileHandler('logs/automacao.log', encoding='utf-8')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger