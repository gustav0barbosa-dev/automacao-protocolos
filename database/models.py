from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()

class Protocolo(Base):
    __tablename__ = "protocolos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    numero_protocolo = Column(String, unique=True, nullable=False, index=True)
    data_solicitacao = Column(String)
    solicitacao = Column(String)
    tipo_solicitante = Column(String)
    
    cpf_servidor = Column(String)
    nome_servidor = Column(String)
    sexo = Column(String)
    matricula = Column(String)
    data_nascimento = Column(String)
    funcao = Column(String)
    data_ingresso = Column(String)

    ultima_data_tarefa = Column(String)          # Ex: "19/08/2026 16:12:50"
    dias_em_aberto = Column(Integer)             # Ex: 15 (calculado a partir da data de solicitação)
    prazo_pagamento_retroativo = Column(String)  # Ex: "Sim", "Não", ou uma data
    data_obito = Column(String)
    
    coletado_em = Column(DateTime, default=datetime.utcnow)

    # Relacionamento 1 para N
    tarefas = relationship("TarefaFluxo", back_populates="protocolo", cascade="all, delete-orphan")

class TarefaFluxo(Base):
    __tablename__ = "tarefas_fluxo"

    id = Column(Integer, primary_key=True, autoincrement=True)
    protocolo_id = Column(Integer, ForeignKey('protocolos.id'))
    
    status_img = Column(String) # Ex: tarefa_finalizada16x16.png
    tarefa = Column(String)     # Ex: Enviar Processo
    data = Column(String)       # Ex: 19/05/2015 14:09:14
    perfil = Column(String)     # Ex: DP. ATEND. PM
    usuario = Column(String)    # Ex: DPPM129878
    opcional = Column(String)   # Ex: Não

    protocolo = relationship("Protocolo", back_populates="tarefas")