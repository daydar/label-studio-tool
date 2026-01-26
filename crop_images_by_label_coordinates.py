import json
import os
import glob
import re
from PIL import Image

# Konfiguration der Pfade
JSON_DIR = "coordinates"
IMAGE_DIR = "page_images"

def process_json_files(json_folder, image_folder):
    output_base_dir = "crops"
    if not os.path.exists(output_base_dir):
        os.makedirs(output_base_dir)

    # Findet alle JSON-Dateien im Ordner "coordinates"
    json_files = glob.glob(os.path.join(json_folder, "*.json"))

    if not json_files:
        print(f"Keine JSON-Dateien in '{json_folder}' gefunden.")
        return

    for json_file_path in json_files:
        with open(json_file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        tasks = data if isinstance(data, list) else [data]

        for task in tasks:
            # Pfad aus JSON extrahieren
            raw_path = task.get("file_upload", task.get("data", {}).get("image", ""))
            full_filename = os.path.basename(raw_path)

            # REGEX: Alles vor dem ersten Bindestrich (inklusive Bindestrich) entfernen
            clean_filename = re.sub(r"^.*?-", "", full_filename)

            # Pfad zum page_images Ordner zusammenbauen
            img_path = os.path.join(image_folder, clean_filename)
            print(f"🔎 Suche nach Bild: {img_path}")

            if not os.path.exists(img_path):
                print(f"⚠️ Bild nicht gefunden: {img_path}")
                continue

            img = Image.open(img_path)
            label_counts = {}

            for annotation in task.get("annotations", []):
                for res in annotation.get("result", []):
                    if "value" not in res:
                        continue

                    val = res["value"]
                    label = val.get("rectanglelabels", ["unknown"])[0]

                    # Umrechnung von Prozent in Pixel
                    orig_w, orig_h = res["original_width"], res["original_height"]
                    left = val["x"] * orig_w / 100
                    top = val["y"] * orig_h / 100
                    right = (val["x"] + val["width"]) * orig_w / 100
                    bottom = (val["y"] + val["height"]) * orig_h / 100

                    crop = img.crop((left, top, right, bottom))

                    # Naming
                    label_counts[label] = label_counts.get(label, 0) + 1
                    clean_name_stem = os.path.splitext(clean_filename)[0]
                    save_name = f"{clean_name_stem}_{label}_{label_counts[label]}.png"

                    crop.save(os.path.join(output_base_dir, save_name))

            print(f"✅ Erledigt: {clean_filename}")


if __name__ == "__main__":
    process_json_files(JSON_DIR, IMAGE_DIR)
