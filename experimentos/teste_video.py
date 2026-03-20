from ultralytics import YOLO
import cv2

model = YOLO("runs/detect/train/weights/best.pt")

video_path = "video_teste.mp4"
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("Erro ao abrir o vídeo.")
    exit()

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(cap.get(cv2.CAP_PROP_FPS))

out = cv2.VideoWriter(
    "resultado_teste.mp4",
    cv2.VideoWriter_fourcc(*"mp4v"),
    fps,
    (width, height)
)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Fim do vídeo.")
        break

    results = model(frame)
    annotated_frame = results[0].plot()

    out.write(annotated_frame)
    cv2.imshow("Teste com Video", annotated_frame)

    if cv2.waitKey(30) & 0xFF == 27:
        break

cap.release()
out.release()
cv2.destroyAllWindows()

#testar com video