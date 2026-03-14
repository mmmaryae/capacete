from ultralytics import YOLO
import cv2

# carrega o modelo treinado
model = YOLO("runs/detect/train/weights/best.pt")

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    
    if not ret:
        break

    # roda a detecção
    results = model(frame)

    # desenha as caixas
    annotated_frame = results[0].plot()

    cv2.imshow("Detector de Capacete", annotated_frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()