from ultralytics import YOLO

def test_yolo():
    model = YOLO("yolov8n.pt")  # load the small pretrained model
    # Save results here instead of result.save()
    results = model.predict(source="bus.jpg", conf=0.3, save=True, save_dir="runs/detect/test")

    result = results[0]
    print(f"Detected classes: {[model.names[int(cls)] for cls in result.boxes.cls]}")

    # Show annotated image in a window
    result.show()

if __name__ == "__main__":
    test_yolo()