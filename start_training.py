import subprocess

def start_training():
# YOLOv8 training command with AMP (automatic mixed precision) enabled
# AMP is enabled by default in Ultralytics, but we pass it explicitly for clarity
	command = (
			'start "" cmd /c "yolo task=detect mode=train '
			'model=yolov8n.pt '
			'data=data/fridge_data/data.yaml '
			'epochs=30 imgsz=640 batch=8 name=fridge_yolo '
			'device=0 amp=True > train_log.txt 2>&1"'
	)

# Launch in new CMD window
	subprocess.run(command, shell=True)


if __name__ == "__main__":
    start_training()