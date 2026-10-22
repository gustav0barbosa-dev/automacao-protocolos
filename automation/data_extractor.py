import re
from bs4 import BeautifulSoup
from datetime import datetime
from parsers.regex_patterns import RegexPatterns
from core.logger import get_logger

logger = get_logger(__name__)

class DataExtractor:
    def __init__(self, html: str):
        self.html = html
        self.soup = BeautifulSoup(html, 'html.parser')

    def _extrair_regex(self, pattern: str) -> str | None:
        # Usamos DOTALL para o ponto pegar quebras de linha
        match = re.search(pattern, self.html, re.DOTALL | re.IGNORECASE)
        if match:
            return match.group(1).strip()
        return None

    def extrair_dados_atendimento(self) -> dict:
        logger.info("Extraindo dados do atendimento e servidor...")
        
        data_sol_str = self._extrair_regex(RegexPatterns.DATA_SOLICITACAO)
        
        dias_aberto = 0
        if data_sol_str:
            try:
                data_sol = datetime.strptime(data_sol_str, "%d/%m/%Y")
                dias_aberto = (datetime.now() - data_sol).days
            except Exception as e:
                logger.warning(f"Erro ao calcular dias em aberto: {e}")

        dados = {
            "numero_protocolo": self._extrair_regex(RegexPatterns.NUMERO_PROTOCOLO),
            "data_solicitacao": data_sol_str,
            "solicitacao": self._extrair_regex(RegexPatterns.SOLICITACAO),
            "tipo_solicitante": self._extrair_regex(RegexPatterns.TIPO_SOLICITANTE),
            
            "cpf_servidor": self._extrair_regex(RegexPatterns.CPF_SERVIDOR),
            "nome_servidor": self._extrair_regex(RegexPatterns.NOME_SERVIDOR),
            "sexo": self._extrair_regex(RegexPatterns.SEXO),
            "matricula": self._extrair_regex(RegexPatterns.MATRICULA),
            "data_nascimento": self._extrair_regex(RegexPatterns.DATA_NASCIMENTO),
            "funcao": self._extrair_regex(RegexPatterns.FUNCAO),
            "data_ingresso": self._extrair_regex(RegexPatterns.DATA_INGRESSO),
            
            # Novos campos
            "dias_em_aberto": dias_aberto,
            "data_obito": self._extrair_regex(RegexPatterns.DATA_OBITO),
            "prazo_pagamento_retroativo": self._extrair_regex(RegexPatterns.PRAZO_RETROATIVO)
        }
        return dados

    def extrair_tarefas_fluxo(self) -> list[dict]:
        """
        Usa BeautifulSoup para extrair a tabela de tarefas.
        Regex é muito ruim para extrair tabelas (<tr> e <td>).
        """
        logger.info("Extraindo lista de tarefas do fluxo...")
        tarefas = []
        
        # Encontra a tabela que contém as tarefas. 
        # Podemos buscar pelo cabeçalho "Status" ou "Tarefa"
        tabelas = self.soup.find_all('table')
        tabela_tarefas = None
        for tabela in tabelas:
            if "Tarefa" in tabela.get_text() and "Status" in tabela.get_text():
                tabela_tarefas = tabela
                break
        
        if not tabela_tarefas:
            logger.warning("Tabela de tarefas não encontrada no HTML.")
            return tarefas

        # Pula a primeira linha (cabeçalho) e itera sobre as linhas de dados
        linhas = tabela_tarefas.find_all('tr')[1:]
        
        for linha in linhas:
            colunas = linha.find_all('td')
            if len(colunas) >= 6: # Garante que a linha tem as colunas esperadas
                # O texto da coluna de status fica vazio porque é uma imagem, 
                # então pegamos a URL da imagem para saber o status
                img_status = colunas[0].find('img')
                status_img = img_status['src'].split('/')[-1] if img_status else "desconhecido"
                
                tarefa = {
                    "status_img": status_img,
                    "tarefa": colunas[1].get_text(strip=True),
                    "data": colunas[2].get_text(strip=True),
                    "perfil": colunas[3].get_text(strip=True),
                    "usuario": colunas[4].get_text(strip=True),
                    "opcional": colunas[5].get_text(strip=True),
                }
                tarefas.append(tarefa)
                
        return tarefas

    def extrair_tudo(self) -> dict:
        dados = self.extrair_dados_atendimento()
        tarefas = self.extrair_tarefas_fluxo()
        dados["tarefas"] = tarefas
        
        # Descobre a última data de movimentação olhando a lista de tarefas
        datas = []
        for t in tarefas:
            if t.get("data"):
                try:
                    # Formato: "19/08/2026 16:12:50"
                    dt = datetime.strptime(t["data"], "%d/%m/%Y %H:%M:%S")
                    datas.append(dt)
                except:
                    pass # Ignora linhas sem data (como a última tarefa cancelada no seu print)
                    
        if datas:
            # Pega a data mais recente da lista
            ultima_data = max(datas)
            dados["ultima_data_tarefa"] = ultima_data.strftime("%d/%m/%Y %H:%M:%S")
        else:
            dados["ultima_data_tarefa"] = None
            
        return dados