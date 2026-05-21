import subprocess
import sys


def start_training():
    # YOLOv8 nano training command with AMP (automatic mixed precision) enabled
    if sys.platform == "win32":
        command = (
            'start "" cmd /c "yolo task=detect mode=train '
            'model=yolov8n.pt '
            'data=data/fridge_data/data.yaml '
            'epochs=30 imgsz=960 batch=32 name=fridge_yolo '
            'device=0 amp=True workers=8 > train_log.txt 2>&1"'
        )
        subprocess.run(command, shell=True)
    else:
        command = (
            "yolo task=detect mode=train "
            "model=yolov8n.pt "
            "data=data/fridge_data/data.yaml "
            "epochs=30 imgsz=960 batch=32 name=fridge_yolo "
            "device=0 amp=True workers=8"
        )
        subprocess.run(command, shell=True)


def resume_training():
    # YOLOv8 resume training command from last.pt checkpoint
    if sys.platform == "win32":
        command = (
            'start "" cmd /c "yolo task=detect mode=train '
            'model=runs/detect/fridge_yolo2/weights/last.pt '
            'data=data/fridge_data/data.yaml '
            'imgsz=640 '
            'resume=True device=0 amp=True workers=6 > resume_log.txt 2>&1"'
        )
        subprocess.run(command, shell=True)
    else:
        command = (
            "yolo task=detect mode=train "
            "model=runs/detect/fridge_yolo2/weights/last.pt "
            "data=data/fridge_data/data.yaml "
            "imgsz=640 "
            "resume=True device=0 amp=True workers=6"
        )
        subprocess.run(command, shell=True)


if __name__ == "__main__":
    # start_training()
    resume_training()
