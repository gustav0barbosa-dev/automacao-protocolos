import os
from playwright.sync_api import sync_playwright
from config.settings import settings
from core.logger import get_logger

logger = get_logger(__name__)

class BrowserManager:
    def __init__(self):
        self._playwright = None
        self.context = None
        self.page = None
        self.user_data_dir = os.path.expanduser("~/.sigeprev_bot_profile")

    def start(self):
        logger.info("Iniciando navegador...")
        self._playwright = sync_playwright().start()
        
        self.context = self._playwright.chromium.launch_persistent_context(
            user_data_dir=self.user_data_dir,
            headless=False, 
            channel="chrome", 
            viewport={"width": 1366, "height": 768}
        )
        
        if len(self.context.pages) > 0:
            self.page = self.context.pages[0]
        else:
            self.page = self.context.new_page()
            
        self.page.set_default_timeout(settings.TIMEOUT_PADRAO * 1000)
        return self.page

    def stop(self):
        if self.context:
            self.context.close()
        if self._playwright:
            self._playwright.stop()

    def __enter__(self):
        self.start() # <-- Aqui estava o erro! Faltava chamar o start()
        return self

    def __exit__(self, *args):
        self.stop()