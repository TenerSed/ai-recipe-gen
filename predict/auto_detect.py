import os
import time
from ultralytics import YOLO

# Paths
WATCH_FOLDER = "inference_images"
OUTPUT_FOLDER = "predictions"
MODEL_PATH = "../runs/detect/fridge_yolo/weights/best.pt"

# Create folders if they don't exist
os.makedirs(WATCH_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Load your trained model
model = YOLO(MODEL_PATH)

print(f"Watching '{WATCH_FOLDER}' for new images...")

# Keep track of processed files
processed_files = set()

while True:
    for file in os.listdir(WATCH_FOLDER):
        if file.lower().endswith((".jpg", ".jpeg", ".png")) and file not in processed_files:
            image_path = os.path.join(WATCH_FOLDER, file)
            print(f"Processing: {file}")
            model.predict(source=image_path, save=True, project=OUTPUT_FOLDER, name=".")
            processed_files.add(file)
    time.sleep(2)  # Check every 2 seconds