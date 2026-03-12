import os
import xml.etree.ElementTree as ET

# Caminhos
annotations_dir = "dataset/annotations"
images_dir = "dataset/images"
labels_dir = "dataset/labels"

os.makedirs(labels_dir, exist_ok=True)

# Mapeamento das classes
classes = ["helmet"]

def convert_box(size, box):
    dw = 1.0 / size[0]
    dh = 1.0 / size[1]
    x = (box[0] + box[1]) / 2.0
    y = (box[2] + box[3]) / 2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x *= dw
    w *= dw
    y *= dh
    h *= dh
    return x, y, w, h

for xml_file in os.listdir(annotations_dir):
    if not xml_file.endswith(".xml"):
        continue

    xml_path = os.path.join(annotations_dir, xml_file)
    tree = ET.parse(xml_path)
    root = tree.getroot()

    size = root.find("size")
    width = int(size.find("width").text)
    height = int(size.find("height").text)

    txt_filename = os.path.splitext(xml_file)[0] + ".txt"
    txt_path = os.path.join(labels_dir, txt_filename)

    with open(txt_path, "w") as out_file:
        for obj in root.findall("object"):
            class_name = obj.find("name").text

            if class_name not in classes:
                continue

            class_id = classes.index(class_name)

            xmlbox = obj.find("bndbox")
            xmin = float(xmlbox.find("xmin").text)
            xmax = float(xmlbox.find("xmax").text)
            ymin = float(xmlbox.find("ymin").text)
            ymax = float(xmlbox.find("ymax").text)

            bb = convert_box((width, height), (xmin, xmax, ymin, ymax))
            out_file.write(f"{class_id} {' '.join(map(str, bb))}\n")

print("Conversão concluída com sucesso!")