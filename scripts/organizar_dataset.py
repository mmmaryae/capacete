import os
import random
import shutil

source_dirs = [
    "dataset_bruto/helmet",
    "dataset_bruto/no_helmet"
]

images = []

for dir in source_dirs:
    for file in os.listdir(dir):
        if file.endswith(".jpg") or file.endswith(".png"):
            images.append((dir, file))

random.shuffle(images)

split = int(len(images) * 0.8)

train = images[:split]
val = images[split:]
def copiar(dataset, tipo):
    for pasta, img in dataset:
        nome = img.split(".")[0]

        img_src = os.path.join(pasta, img)
        txt_src = os.path.join(pasta, nome + ".txt")

        if not os.path.exists(txt_src):
            continue

        img_dst = f"dataset_yolo/images/{tipo}/{img}"
        txt_dst = f"dataset_yolo/labels/{tipo}/{nome}.txt"

        shutil.copy(img_src, img_dst)
        shutil.copy(txt_src, txt_dst)

copiar(train, "train")
copiar(val, "val")

print("Dataset organizado!")