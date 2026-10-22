from dataclasses import dataclass

@dataclass
class Settings:
    BASE_URL: str = "https://sistema.exemplo.com"
    LOGIN_URL: str = f"{BASE_URL}/login"
    TIMEOUT_PADRAO: int = 30
    HEADLESS: bool = False  # False durante o mapeamento, True em produção
    DB_URL: str = "sqlite:///protocolos.db"
    LOG_LEVEL: str = "INFO"

settings = Settings()