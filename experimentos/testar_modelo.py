from ultralytics import YOLO
import cv2

model = YOLO("model/best.pt")

image = cv2.imread("teste3.PNG")

results = model(image)

annotated = results[0].plot()

cv2.imshow("Teste Capacete", annotated)
cv2.waitKey(0)
cv2.destroyAllWindows()

#testar com imagens