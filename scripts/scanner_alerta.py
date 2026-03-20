# arquivo principal da IA
# rode com: python scripts\scanner_alerta.py

import logging
import time
from pathlib import Path
from typing import Optional

import cv2
from ultralytics import YOLO

from resposta_front import montar_resposta_front
from alerta_service import montar_alerta, enviar_alerta, enviar_status

BASE_DIR    = Path(__file__).parent.parent
MODEL_PATH  = BASE_DIR / "model" / "best.pt"
CAPTURE_DIR = BASE_DIR / "captures"
LOG_PATH    = BASE_DIR / "epi_scanner.log"

ALERT_THRESHOLD_SECONDS = 3
COOLDOWN_SECONDS        = 10
DISPLAY_ALERT_DURATION  = 2
JPEG_QUALITY            = 95
VIDEO_SOURCE            = 0
EXIT_KEY                = 27

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_PATH),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def setup_environment() -> bool:
    try:
        CAPTURE_DIR.mkdir(parents=True, exist_ok=True)
        logger.info(f"Pasta de captura: {CAPTURE_DIR}")
        return True
    except Exception as e:
        logger.error(f"Erro ao configurar ambiente: {e}")
        return False


def load_model(model_path: Path) -> Optional[YOLO]:
    try:
        logger.info(f"Carregando modelo: {model_path}")
        model = YOLO(str(model_path))
        logger.info("Modelo carregado com sucesso!")
        return model
    except FileNotFoundError:
        logger.error(f"Modelo não encontrado: {model_path}")
        return None
    except Exception as e:
        logger.error(f"Erro ao carregar modelo: {e}")
        return None


def initialize_camera(source: int = 0) -> Optional[cv2.VideoCapture]:
    try:
        cap = cv2.VideoCapture(source)
        if not cap.isOpened():
            logger.error("Não foi possível abrir a câmera.")
            return None
        logger.info("Câmera inicializada com sucesso!")
        return cap
    except Exception as e:
        logger.error(f"Erro ao inicializar câmera: {e}")
        return None


def detect_missing_ppe(results, model) -> bool:
    if not results or results[0].boxes is None:
        return False
    return any(
        model.names[int(box.cls[0].item())] == "sem_capacete"
        for box in results[0].boxes
    )


def capture_and_alert(frame, caminho_imagem: str,
                      tempo_alerta: float, origem: str = "camera_1") -> bool:
    try:
        cv2.imwrite(caminho_imagem, frame,
                    [cv2.IMWRITE_JPEG_QUALITY, JPEG_QUALITY])
        alerta = montar_alerta(
            caminho_imagem=caminho_imagem,
            tempo_alerta=tempo_alerta,
            origem=origem
        )
        enviar_alerta(alerta)
        logger.warning(f"ALERTA REGISTRADO: {caminho_imagem}")
        return True
    except Exception as e:
        logger.error(f"Erro ao capturar alerta: {e}")
        return False

def draw_status(frame, status: str, tempo: float = 0,
                alerta_registrado: bool = False) -> None:
    font = cv2.FONT_HERSHEY_SIMPLEX
    if status == "sem_capacete":
        color = (0, 0, 255)
        if tempo < ALERT_THRESHOLD_SECONDS:
            text = f"Sem capacete {tempo:.1f}s"
        else:
            text = f"ALERTA: sem capacete por {tempo:.1f}s"
        cv2.putText(frame, text, (20, 40), font, 1, color, 2)
    # com_capacete e cooldown: tela limpa, não escreve nada
    if alerta_registrado:
        cv2.putText(frame, "ALERTA REGISTRADO", (20, 80),
                    font, 1, (0, 255, 0), 3)


def main():
    if not setup_environment():
        return

    model = load_model(MODEL_PATH)
    if model is None:
        return

    cap = initialize_camera(VIDEO_SOURCE)
    if cap is None:
        return

    tempo_sem_capacete_inicio: Optional[float] = None
    ultimo_alerta = 0
    mostrar_alerta_registrado_ate = 0

    logger.info("Iniciando scanner de EPI...")

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                logger.error("Erro na captura da câmera.")
                break

            results = model(frame, verbose=False)
            annotated_frame = results[0].plot()

            agora = time.time()
            detectou = detect_missing_ppe(results, model)

            if detectou:
                em_cooldown = (agora - ultimo_alerta) < COOLDOWN_SECONDS

                if em_cooldown:
                    tempo_sem_capacete_inicio = None
                    resposta = montar_resposta_front(
                        status="cooldown", tempo=0,
                        alerta=False, imagem=None
                    )
                else:
                    if tempo_sem_capacete_inicio is None:
                        tempo_sem_capacete_inicio = agora
                    tempo_decorrido = agora - tempo_sem_capacete_inicio

                    if tempo_decorrido >= ALERT_THRESHOLD_SECONDS:
                        nome = time.strftime("alerta_%Y%m%d_%H%M%S.jpg")
                        caminho = str(CAPTURE_DIR / nome)
                        if capture_and_alert(frame, caminho, ALERT_THRESHOLD_SECONDS):
                            mostrar_alerta_registrado_ate = agora + DISPLAY_ALERT_DURATION
                            ultimo_alerta = agora
                            tempo_sem_capacete_inicio = None

                    resposta = montar_resposta_front(
                        status="sem_capacete", tempo=tempo_decorrido,
                        alerta=(tempo_decorrido >= ALERT_THRESHOLD_SECONDS),
                        imagem=None
                    )
            else:
                tempo_sem_capacete_inicio = None
                resposta = montar_resposta_front(
                    status="com_capacete", tempo=0,
                    alerta=False, imagem=None
                )

            enviar_status(resposta)

            draw_status(
                annotated_frame,
                status=resposta.get("status", "com_capacete"),
                tempo=resposta.get("tempo_sem_capacete", 0),
                alerta_registrado=(agora < mostrar_alerta_registrado_ate)
            )

            cv2.imshow("Scanner EPI", annotated_frame)
            if cv2.waitKey(1) & 0xFF == EXIT_KEY:
                logger.info("Encerrando scanner...")
                break

    except KeyboardInterrupt:
        logger.info("Scanner interrompido pelo usuário.")
    except Exception as e:
        logger.error(f"Erro inesperado: {e}", exc_info=True)
    finally:
        cap.release()
        cv2.destroyAllWindows()
        logger.info("Scanner encerrado.")


if __name__ == "__main__":
    main()