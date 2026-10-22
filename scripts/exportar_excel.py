import sys
import os

# Adiciona a pasta raiz do projeto ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd
from database.connection import SessionLocal
from database.models import Protocolo, TarefaFluxo
from utils.validators import validar_protocolo

def exportar():
    # 1. Lê o arquivo protocolos.txt para saber o que filtrar
    protocolos_filtrados = []
    try:
        with open("protocolos.txt", "r", encoding="utf-8") as f:
            for linha in f:
                linha = linha.strip()
                if linha:
                    try:
                        # Normaliza para garantir que bata com o banco (ex: 61610072 -> 0061610072)
                        num_limpo = validar_protocolo(linha)
                        protocolos_filtrados.append(num_limpo)
                    except ValueError:
                        pass # Ignora linhas inválidas no txt
    except FileNotFoundError:
        print("⚠️  Arquivo 'protocolos.txt' não encontrado. O relatório incluirá TODOS os protocolos do banco.")
        protocolos_filtrados = None

    db = SessionLocal()
    try:
        # 2. Faz a query no banco (filtrando ou não)
        query = db.query(Protocolo)
        if protocolos_filtrados:
            query = query.filter(Protocolo.numero_protocolo.in_(protocolos_filtrados))
        
        protocolos = query.all()

        if not protocolos:
            print("❌ Nenhum protocolo encontrado no banco para os filtros do 'protocolos.txt'.")
            return

        # Pega os IDs dos protocolos filtrados para pegar as tarefas certas
        ids_protocolos = [p.id for p in protocolos]

        # 3. Monta os dados para o Excel
        dados_protocolos = [{
            "Nº Protocolo": p.numero_protocolo,
            "Data Solicitação": p.data_solicitacao,
            "Última Movimentação": p.ultima_data_tarefa,
            "Dias em Aberto": p.dias_em_aberto,
            "Prazo Retroativo": p.prazo_pagamento_retroativo,
            "Data Óbito": p.data_obito,
            "Solicitação": p.solicitacao,
            "Tipo Solicitante": p.tipo_solicitante,
            "CPF Servidor": p.cpf_servidor,
            "Nome Servidor": p.nome_servidor,
            "Matrícula": p.matricula,
            "Função": p.funcao,
        } for p in protocolos]

        # 4. Busca as tarefas apenas dos protocolos filtrados
        tarefas = db.query(TarefaFluxo).filter(TarefaFluxo.protocolo_id.in_(ids_protocolos)).all()
        
        dados_tarefas = [{
            "Protocolo ID": t.protocolo_id,
            "Status": t.status_img.replace(".png", ""),
            "Tarefa": t.tarefa,
            "Data": t.data,
            "Perfil": t.perfil,
            "Usuário": t.usuario,
            "Opcional": t.opcional,
        } for t in tarefas]

        # 5. Salva em um arquivo Excel com 2 abas
        with pd.ExcelWriter("relatorio_protocolos.xlsx", engine="openpyxl") as writer:
            pd.DataFrame(dados_protocolos).to_excel(writer, sheet_name="Protocolos", index=False)
            pd.DataFrame(dados_tarefas).to_excel(writer, sheet_name="Tarefas", index=False)

        print(f"✅ Arquivo 'relatorio_protocolos.xlsx' gerado com sucesso com {len(protocolos)} protocolos!")
    finally:
        db.close()

if __name__ == "__main__":
    exportar()