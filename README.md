# Automação SIGEPREV - Consulta e Extração de Protocolos

Este projeto é uma automação em Python desenvolvida para realizar consultas em lote de protocolos no sistema **SIGEPREV (SPPREV)**. O robô utiliza a biblioteca **Playwright** para navegar no sistema, **BeautifulSoup** e **Regex** para extrair dados estruturados e **SQLAlchemy** para persistir as informações em um banco de dados local (SQLite).

## Funcionalidades

- **Login Assistido:** Integração inteligente com o Gov.br / IDP SP. O robô abre o navegador, aguarda o login manual (contornando bloqueios de captcha e 2FA) e assume o controle automaticamente.
- **Processamento em Lote:** Lê uma lista de protocolos de um arquivo `.txt` e os processa de uma só vez, sem fechar o navegador e sem precisar logar várias vezes.
- **Extração de Dados:**
  - Dados gerais do atendimento (Data, Tipo, Solicitante).
  - Dados do servidor (Nome, CPF, Matrícula, Função).
  - Dados de Óbito e Prazo de Pagamento Retroativo.
  - Lista completa de tarefas do fluxo (Status, Usuário, Perfil, Data).
- **Inteligência de Dados:** Calcula automaticamente os *Dias em Aberto* desde a data de solicitação e extrai a *Última Data de Movimentação*.
- **Upsert no Banco de Dados:** Se o protocolo já existir no banco, seus dados e tarefas são atualizados (evitando duplicações).
- **Exportação para Excel:** Gera um relatório `.xlsx` contendo duas abas (Protocolos e Tarefas), filtrando apenas os protocolos que foram solicitados no lote.

## Tecnologias Utilizadas

- **Python 3.10+**
- **Playwright** (Automação do navegador)
- **BeautifulSoup4 / LXML** (Parsing de HTML)
- **SQLAlchemy** (ORM e Banco de Dados SQLite)
- **Pandas / OpenPyXL** (Exportação de relatórios)
- **Regex** (Extração de campos específicos)

## Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/automacao-protocolos.git
   cd automacao-protocolos

2. Ative a venv:
    ```bash
    python -m venv venv
    .\venv\Scripts\Activate.ps1

3. Instale as bibliotecas: 
    ```bash
    pip install --upgrade pip
    pip install -r requirements.txt 
    playwright install chromium

4. Execute o programa:
    coloque os protocolos dentro do arquivo "protocolos.txt", um protocolo por linha.
    ```bash
    python Main.py

5. Gerar relatório Excel
    ```bash
    python scripts/exportar_excel.py

## Estrutura do Projeto
automacao_protocolos/
├── config/          # Configurações globais e credenciais (.env)
├── core/            # Gerenciador do navegador e logs
├── automation/      # Scripts de navegação, busca e extração
├── parsers/         # Regras de Regex e parsing HTML
├── database/        # Modelos do SQLAlchemy, conexão e repositório
├── services/        # Orquestração do fluxo de trabalho
├── utils/           # Validadores e funções auxiliares
├── scripts/         # Scripts extras (ex: exportar_excel.py)
├── main.py          # Ponto de entrada da automação
└── requirements.txt # Dependências do projeto

## Colaboradores
- Gustavo Barbosa - Estagiário • SPPREV-DTR-SSI