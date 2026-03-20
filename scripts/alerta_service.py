# salva os alertas no banco de dados MySQL
# usuario_id por enquanto é 1 (padrão)
# quando integrar com o login, substituir pelo ID real do usuário logado

from datetime import datetime
import mysql.connector
import logging

logger = logging.getLogger(__name__)

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "capacete_ia"
}

# usuario padrão até integrar com o login
# quando integrar: trocar esse 1 pelo ID real do usuário logado

USUARIO_ID_PADRAO = 1


def conectar_banco():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        logger.error(f"Erro ao conectar no banco: {e}")
        return None


def montar_alerta(caminho_imagem, tempo_alerta, origem="camera_1", usuario_id=None):
    agora = datetime.now()
    return {
        "status": "sem_capacete",
        "mensagem": f"Pessoa sem capacete por mais de {tempo_alerta} segundos",
        "tempo_alerta": tempo_alerta,
        "imagem": caminho_imagem,
        "data": agora.strftime("%d/%m/%Y"),
        "hora": agora.strftime("%H:%M:%S"),
        "data_hora": agora.strftime("%Y-%m-%d %H:%M:%S"),
        "origem": origem,
        "usuario_id": usuario_id if usuario_id is not None else USUARIO_ID_PADRAO,
    }


def enviar_alerta(alerta):
    conn = conectar_banco()
    if conn is None:
        return
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO alertas
                (status, mensagem, tempo_alerta, imagem, data, hora, data_hora, origem, usuario_id)
            VALUES
                (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            alerta["status"],
            alerta["mensagem"],
            alerta["tempo_alerta"],
            alerta["imagem"],
            alerta["data"],
            alerta["hora"],
            alerta["data_hora"],
            alerta["origem"],
            alerta["usuario_id"],
        ))
        conn.commit()
        logger.info(f"Alerta salvo — usuario_id: {alerta['usuario_id']} — {alerta['hora']}")
    except Exception as e:
        logger.error(f"Erro ao salvar alerta: {e}")
    finally:
        cursor.close()
        conn.close()


def enviar_status(resposta: dict):
    # o backend preenche aqui quando estiver pronto
    pass