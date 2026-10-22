from core.browser import BrowserManager
from automation.navigation import NavigationAutomation
from automation.protocol_search import ProtocolSearch
from automation.data_extractor import DataExtractor
from database.repository import ProtocoloRepository
from core.logger import get_logger

logger = get_logger(__name__)


class ProtocoloService:
    def __init__(self):
        self.repo = ProtocoloRepository()

    # ------------------------------------------------------------------
    # MÉTODO PRINCIPAL PARA LOTE
    # ------------------------------------------------------------------
    def processar_lote(self, protocolos: list[str]) -> list[dict]:
        """
        Processa uma lista de protocolos mantendo o navegador aberto.
        O login é feito UMA vez, e reaproveitado para todos os protocolos.
        """
        resultados = []

        with BrowserManager() as browser:
            page = browser.page

            # 1. Garante que estamos logados (uma única vez)
            self._garantir_sessao(page)

            # 2. Loop nos protocolos
            for i, numero in enumerate(protocolos, start=1):
                logger.info(f"[{i}/{len(protocolos)}] Processando protocolo: {numero}")
                try:
                    dados = self._processar_um(page, numero)
                    resultados.append(dados)
                    logger.info(f"✅ Protocolo {numero} processado com sucesso!")
                except Exception as e:
                    logger.error(f"❌ Erro no protocolo {numero}: {e}")
                    resultados.append({"numero_protocolo": numero, "erro": str(e)})

                    # Se o erro foi de sessão (ex: redirecionou para login),
                    # tenta reautenticar e continuar
                    if self._parece_erro_de_sessao(e):
                        logger.warning("Sessão parece ter expirado. Tentando reautenticar...")
                        try:
                            self._garantir_sessao(page, forcar=True)
                        except Exception as login_err:
                            logger.error(f"Não foi possível reautenticar: {login_err}")
                            # Sem sessão, não adianta continuar o lote
                            break

        return resultados

    # ------------------------------------------------------------------
    # PROCESSAMENTO DE UM PROTOCOLO (navegador já aberto e logado)
    # ------------------------------------------------------------------
    def _processar_um(self, page, numero_protocolo: str) -> dict:
        NavigationAutomation(page).ir_para_aba_protocolos()
        html = ProtocolSearch(page).buscar_e_abrir(numero_protocolo)
        dados = DataExtractor(html).extrair_tudo()
        self.repo.salvar(dados, html_raw=html)
        return dados

    # ------------------------------------------------------------------
    # GERENCIAMENTO DE SESSÃO
    # ------------------------------------------------------------------
    def _garantir_sessao(self, page, forcar: bool = False):
        """Verifica se está logado. Se não estiver, pausa para o usuário logar."""
        logger.info("Acessando o SIGEPREV...")
        page.goto("https://sigeprev.spprev.sp.gov.br/")

        # Se forçar, ou se o menu não aparecer em 5s, assume que precisa logar
        precisa_login = forcar
        if not precisa_login:
            try:
                page.wait_for_selector('text="Atendimento"', timeout=5000)
                logger.info("Sessão já ativa. Prosseguindo...")
                return
            except Exception:
                precisa_login = True

        if precisa_login:
            logger.warning("⚠️ SESSÃO EXPIRADA OU NÃO INICIADA!")
            print("\n" + "=" * 60)
            print("👉 FAÇA O LOGIN NO NAVEGADOR (GOV.BR / IDP SP).")
            print("👉 O ROBÔ VAI ESPERAR AUTOMATICAMENTE ATÉ VOCÊ ENTRAR NO SIGEPREV.")
            print("=" * 60 + "\n")

            try:
                page.wait_for_selector('text="Atendimento"', timeout=300000)  # 5 min
                logger.info("Login detectado com sucesso! Continuando automação...")
                page.wait_for_load_state("networkidle")
            except Exception:
                raise TimeoutError("Você não concluiu o login a tempo.")

    @staticmethod
    def _parece_erro_de_sessao(erro: Exception) -> bool:
        """Heurística para detectar se o erro foi por sessão expirada."""
        msg = str(erro).lower()
        pistas = ["login", "sso.acesso.gov.br", "idp.sp.gov.br", "timeout 30000ms",
                  "waiting for locator", "not visible"]
        return any(p in msg for p in pistas)