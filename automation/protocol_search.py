from core.logger import get_logger
from playwright.sync_api import Page

logger = get_logger(__name__)

class ProtocolSearch:
    def __init__(self, page: Page):
        self.page = page

    def buscar_e_abrir(self, numero_protocolo: str) -> str:
        logger.info(f"Buscando protocolo: {numero_protocolo}")
        
        # Preencher o campo do protocolo
        self.page.fill('input#numeroProtocolo', numero_protocolo)
        
        # Clicar no botão CONSULTAR
        self.page.click('input#btnConsultar')
        
        # Esperar a página de resultado carregar. 
        # O sistema exibe a "LISTA DE TAREFAS DO FLUXO" após a consulta.
        try:
            self.page.wait_for_selector('text="LISTA DE TAREFAS DO FLUXO"', timeout=20000)
        except Exception:
            self.page.wait_for_load_state("networkidle")
            self.page.wait_for_timeout(3000)
        
        logger.info("Consulta concluída, capturando HTML...")
        return self.page.content()