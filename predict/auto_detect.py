"""
Auto-detect ingredients in fridge images using a trained YOLO model.

Run this script from the `predict/` directory:
    cd predict && python auto_detect.py

Drop images into the `inference_images/` folder and predictions will be
saved to `predictions/` automatically.
"""

import os
import time
from pathlib import Path
from ultralytics import YOLO

# Resolve paths relative to this file so the script works regardless of cwd
SCRIPT_DIR = Path(__file__).parent.resolve()
WATCH_FOLDER = SCRIPT_DIR / "inference_images"
OUTPUT_FOLDER = SCRIPT_DIR / "predictions"
MODEL_PATH = SCRIPT_DIR / "../runs/detect/fridge_yolo/weights/best.pt"

# Create folders if they don't exist
WATCH_FOLDER.mkdir(exist_ok=True)
OUTPUT_FOLDER.mkdir(exist_ok=True)

if not MODEL_PATH.exists():
    raise FileNotFoundError(
        f"Model weights not found at {MODEL_PATH}. "
        "Ensure the model has been trained and weights are present."
    )

# Load trained model
model = YOLO(str(MODEL_PATH))

print(f"Watching '{WATCH_FOLDER}' for new images...")

# Keep track of processed files
processed_files = set()

while True:
    for file in os.listdir(WATCH_FOLDER):
        if file.lower().endswith((".jpg", ".jpeg", ".png")) and file not in processed_files:
            image_path = str(WATCH_FOLDER / file)
            print(f"Processing: {file}")
            model.predict(source=image_path, save=True, project=str(OUTPUT_FOLDER), name=".")
            processed_files.add(file)
    time.sleep(2)  # Check every 2 seconds
