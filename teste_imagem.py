from ultralytics import YOLO

model = YOLO(r"C:\Users\Acer\Desktop\capacete-ia\runs\detect\train2\weights\best.pt")

results = model.predict(
    source=r"C:\Users\Acer\Desktop\capacete-ia\teste2.png",
    conf=0.5,
    save=True,
    show=True
)

print("Teste concluído")