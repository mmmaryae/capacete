import os
import random
import shutil

# Pastas de origem
images_dir = "dataset/images"
labels_dir = "dataset/labels"

# Pastas de destino
train_images_dir = "dataset/images/train"
val_images_dir = "dataset/images/val"
train_labels_dir = "dataset/labels/train"
val_labels_dir = "dataset/labels/val"

# Criar pastas se não existirem
os.makedirs(train_images_dir, exist_ok=True)
os.makedirs(val_images_dir, exist_ok=True)
os.makedirs(train_labels_dir, exist_ok=True)
os.makedirs(val_labels_dir, exist_ok=True)

# Lista de imagens
image_files = [f for f in os.listdir(images_dir) if f.endswith((".jpg", ".jpeg", ".png"))]

# Embaralhar
random.shuffle(image_files)

# Separação 80/20
split_index = int(len(image_files) * 0.8)
train_files = image_files[:split_index]
val_files = image_files[split_index:]

def move_files(file_list, img_dest, lbl_dest):
    for image_file in file_list:
        image_src = os.path.join(images_dir, image_file)
        image_dst = os.path.join(img_dest, image_file)

        label_file = os.path.splitext(image_file)[0] + ".txt"
        label_src = os.path.join(labels_dir, label_file)
        label_dst = os.path.join(lbl_dest, label_file)

        if os.path.exists(image_src):
            shutil.copy(image_src, image_dst)

        if os.path.exists(label_src):
            shutil.copy(label_src, label_dst)

move_files(train_files, train_images_dir, train_labels_dir)
move_files(val_files, val_images_dir, val_labels_dir)

print("Divisão concluída com sucesso!")
print(f"Treino: {len(train_files)} imagens")
print(f"Validação: {len(val_files)} imagens")