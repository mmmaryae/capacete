from ultralytics import YOLO
import cv2

model = YOLO(r"C:\Users\Acer\Desktop\capacete-ia\runs\detect\train2\weights\best.pt")

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    results = model(frame)

    annotated_frame = results[0].plot()

    cv2.imshow("Detecção de Capacete", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()