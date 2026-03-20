# Capacete IA

Sistema que usa a câmera do dispositivo para detectar em tempo real
se as pessoas estão usando capacete. Quando alguém fica 3 segundos
sem capacete, o sistema dispara um alerta, salva uma foto e registra
no banco de dados.

---

## Tecnologias

- Python + YOLOv8 — detecção de capacete
- FastAPI — API que conecta a IA com o site
- OpenCV — leitura da câmera
- MySQL — banco de dados dos alertas


Projeto acadêmico — detecção de EPI com visão computacional.