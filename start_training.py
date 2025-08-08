import subprocess

def start_training():
    command = (
        'start "" cmd /c "yolo task=detect mode=train '
        'model=D:/ai-recipe-gen/runs/detect/fridge_yolo5/weights/last.pt '
        'data=data/fridge_data/data.yaml epochs=30 imgsz=640 batch=8 '
        'name=fridge_yolo resume=True device=0 amp=True > train_log.txt 2>&1"'
    )

    subprocess.run(command, shell=True)

if __name__ == "__main__":
    start_training()