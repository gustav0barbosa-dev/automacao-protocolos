from core.browser import BrowserManager
from config.credentials import Credentials
from config.settings import settings
from core.logger import get_logger

logger = get_logger(__name__)

class LoginAutomation:
    def __init__(self, browser: BrowserManager):
        self.browser = browser
        self.page = browser.page

    def executar(self):
        logger.info("Iniciando login...")
        # TODO: preencher com seletores reais após mapeamento
        self.page.goto(settings.LOGIN_URL)

        # self.page.fill('input[name="usuario"]', Credentials.USUARIO)
        # self.page.fill('input[name="senha"]', Credentials.SENHA)
        # self.page.click('button[type="submit"]')
        # self.page.wait_for_load_state("networkidle")

        logger.info("Login realizado com sucesso.")