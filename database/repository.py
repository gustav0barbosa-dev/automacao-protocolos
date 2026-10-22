from database.connection import SessionLocal, init_db
from database.models import Protocolo, TarefaFluxo
from core.logger import get_logger

logger = get_logger(__name__)

class ProtocoloRepository:
    def __init__(self):
        # Garante que as tabelas existam antes de tentar salvar
        init_db()

    def salvar(self, dados: dict, html_raw: str = None):
        db = SessionLocal()
        try:
            num_protocolo = dados.get("numero_protocolo")
            
            # Verifica se o protocolo já existe no banco
            protocolo_existente = db.query(Protocolo).filter_by(numero_protocolo=num_protocolo).first()
            
            if protocolo_existente:
                logger.info(f"Protocolo {num_protocolo} já existe no banco. Atualizando dados...")
                # Remove as tarefas antigas para não duplicar
                db.query(TarefaFluxo).filter_by(protocolo_id=protocolo_existente.id).delete()
                protocolo = protocolo_existente
            else:
                logger.info(f"Salvando novo protocolo {num_protocolo}...")
                protocolo = Protocolo(numero_protocolo=num_protocolo)
                db.add(protocolo)

            # Atualiza os campos do protocolo
            protocolo.data_solicitacao = dados.get("data_solicitacao")
            protocolo.solicitacao = dados.get("solicitacao")
            protocolo.tipo_solicitante = dados.get("tipo_solicitante")
            protocolo.cpf_servidor = dados.get("cpf_servidor")
            protocolo.nome_servidor = dados.get("nome_servidor")
            protocolo.sexo = dados.get("sexo")
            protocolo.matricula = dados.get("matricula")
            protocolo.data_nascimento = dados.get("data_nascimento")
            protocolo.funcao = dados.get("funcao")
            protocolo.data_ingresso = dados.get("data_ingresso")

            protocolo.ultima_data_tarefa = dados.get("ultima_data_tarefa")
            protocolo.dias_em_aberto = dados.get("dias_em_aberto")
            protocolo.prazo_pagamento_retroativo = dados.get("prazo_pagamento_retroativo")
            protocolo.data_obito = dados.get("data_obito")
            # Precisamos dar um flush para gerar o ID do protocolo antes de salvar as tarefas
            db.flush()

            # Salva as tarefas associadas
            tarefas = dados.get("tarefas", [])
            for t in tarefas:
                nova_tarefa = TarefaFluxo(
                    protocolo_id=protocolo.id,
                    status_img=t.get("status_img"),
                    tarefa=t.get("tarefa"),
                    data=t.get("data"),
                    perfil=t.get("perfil"),
                    usuario=t.get("usuario"),
                    opcional=t.get("opcional")
                )
                db.add(nova_tarefa)

            db.commit()
            logger.info(f"Protocolo {num_protocolo} e {len(tarefas)} tarefas salvas com sucesso!")
            
        except Exception as e:
            db.rollback()
            logger.error(f"Erro ao salvar no banco de dados: {e}")
            raise e
        finally:
            db.close()