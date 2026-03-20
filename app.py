"""
API do sistema de detecção de EPI.
Recebe frames do navegador, processa com YOLO e salva alertas no banco.

Rode com: uvicorn app:app --reload

Rotas disponíveis:
  POST /api/processar        → recebe frame, roda YOLO, retorna resultado
  GET  /api/alertas          → lista todos os alertas (filtra por ?usuario_id=1)
  GET  /api/alertas/hoje     → alertas do dia (filtra por ?usuario_id=1)
"""

import time
import logging
from pathlib import Path
from typing import Optional

import cv2
import numpy as np
import mysql.connector
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from ultralytics import YOLO
import uvicorn

from scripts.alerta_service import montar_alerta, enviar_alerta, DB_CONFIG
from scripts.resposta_front import montar_resposta_front

# ==================== CONFIGURAÇÕES ====================
BASE_DIR    = Path(__file__).parent
MODEL_PATH  = BASE_DIR / "model" / "best.pt"
CAPTURE_DIR = BASE_DIR / "captures"
CAPTURE_DIR.mkdir(exist_ok=True)

ALERT_THRESHOLD_SECONDS = 3
COOLDOWN_SECONDS        = 10
DISPLAY_ALERT_DURATION  = 2
JPEG_QUALITY            = 95

# ==================== LOGGING ====================
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ==================== MODELO ====================
logger.info("Carregando modelo YOLO...")
model = YOLO(str(MODEL_PATH))
logger.info("Modelo carregado!")

# ==================== ESTADO POR USUÁRIO ====================
# cada usuário tem seu próprio estado de detecção independente
estados_usuarios = {}

def get_estado_usuario(usuario_id: int) -> dict:
    if usuario_id not in estados_usuarios:
        estados_usuarios[usuario_id] = {
            "tempo_sem_capacete_inicio": None,
            "ultimo_alerta": 0,
            "mostrar_alerta_ate": 0,
        }
    return estados_usuarios[usuario_id]

# ==================== APP ====================
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# serve as fotos capturadas para o frontend acessar
app.mount("/captures", StaticFiles(directory="captures"), name="captures")

# ==================== ROTAS ====================

@app.post("/api/processar")
async def processar_frame(request: Request):
    """
    Recebe um frame do navegador em bytes.
    Roda o YOLO, aplica lógica de alerta e retorna o resultado.

    Header esperado: X-Usuario-ID (int) — padrão 1 até integrar com login

    Retorna JSON com:
      status, tempo_sem_capacete, alerta, mensagem, acao_front, alerta_registrado
    """
    # pega o ID do usuário logado — quando integrar com login, vem automaticamente
    usuario_id = int(request.headers.get("X-Usuario-ID", 1))

    body = await request.body()
    nparr = np.frombuffer(body, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    if frame is None:
        return {"erro": "Frame inválido"}

    results = model(frame, verbose=False)

    detectou_sem_capacete = any(
        model.names[int(box.cls[0].item())] == "sem_capacete"
        for box in (results[0].boxes or [])
    )

    estado = get_estado_usuario(usuario_id)
    agora = time.time()

    if detectou_sem_capacete:
        em_cooldown = (agora - estado["ultimo_alerta"]) < COOLDOWN_SECONDS

        if em_cooldown:
            estado["tempo_sem_capacete_inicio"] = None
            resposta = montar_resposta_front(
                status="cooldown", tempo=0,
                alerta=False, imagem=None
            )
        else:
            if estado["tempo_sem_capacete_inicio"] is None:
                estado["tempo_sem_capacete_inicio"] = agora
            tempo_decorrido = agora - estado["tempo_sem_capacete_inicio"]

            if tempo_decorrido >= ALERT_THRESHOLD_SECONDS:
                nome = time.strftime("alerta_%Y%m%d_%H%M%S.jpg")
                caminho = str(CAPTURE_DIR / nome)
                cv2.imwrite(caminho, frame, [cv2.IMWRITE_JPEG_QUALITY, JPEG_QUALITY])
                alerta = montar_alerta(
                    caminho_imagem=caminho,
                    tempo_alerta=ALERT_THRESHOLD_SECONDS,
                    origem=f"camera_usuario_{usuario_id}",
                    usuario_id=usuario_id
                )
                enviar_alerta(alerta)
                estado["ultimo_alerta"] = agora
                estado["mostrar_alerta_ate"] = agora + DISPLAY_ALERT_DURATION
                estado["tempo_sem_capacete_inicio"] = None
                logger.warning(f"ALERTA — usuario {usuario_id}: {caminho}")

            resposta = montar_resposta_front(
                status="sem_capacete",
                tempo=tempo_decorrido,
                alerta=(tempo_decorrido >= ALERT_THRESHOLD_SECONDS),
                imagem=None
            )
    else:
        estado["tempo_sem_capacete_inicio"] = None
        resposta = montar_resposta_front(
            status="com_capacete", tempo=0,
            alerta=False, imagem=None
        )

    resposta["alerta_registrado"] = agora < estado["mostrar_alerta_ate"]
    return resposta


@app.get("/api/alertas")
def listar_alertas(usuario_id: Optional[int] = None):
    """Lista todos os alertas. Filtra por usuario_id se informado."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        if usuario_id:
            cursor.execute(
                "SELECT * FROM alertas WHERE usuario_id = %s ORDER BY criado_em DESC",
                (usuario_id,)
            )
        else:
            cursor.execute("SELECT * FROM alertas ORDER BY criado_em DESC")
        alertas = cursor.fetchall()
        return {"alertas": alertas}
    except Exception as e:
        return {"erro": str(e)}
    finally:
        cursor.close()
        conn.close()


@app.get("/api/alertas/hoje")
def alertas_hoje(usuario_id: Optional[int] = None):
    """Retorna os alertas do dia atual."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        if usuario_id:
            cursor.execute(
                "SELECT * FROM alertas WHERE DATE(criado_em) = CURDATE() AND usuario_id = %s ORDER BY criado_em DESC",
                (usuario_id,)
            )
        else:
            cursor.execute(
                "SELECT * FROM alertas WHERE DATE(criado_em) = CURDATE() ORDER BY criado_em DESC"
            )
        alertas = cursor.fetchall()
        return {"total": len(alertas), "alertas": alertas}
    except Exception as e:
        return {"erro": str(e)}
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)