from core.logger import get_logger
from playwright.sync_api import Page

logger = get_logger(__name__)

class NavigationAutomation:
    def __init__(self, page: Page):
        self.page = page

    def ir_para_aba_protocolos(self):
        logger.info("Navegando diretamente para a página de Consulta de Protocolo...")
        
        # URL exata da tela de consulta (extraída do HTML)
        url_consulta = "https://sigeprev.spprev.sp.gov.br/spprev/jsp/atendimento/consultaProtocoloNew.jsp"
        
        self.page.goto(url_consulta)
        self.page.wait_for_load_state("networkidle")
        
        # Verifica se realmente carregou o formulário
        self.page.wait_for_selector('input#numeroProtocolo', timeout=15000)
        logger.info("Página de consulta carregada com sucesso.")