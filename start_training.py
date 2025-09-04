import subprocess
import torch
import datetime


def start_training():
    # YOLOv11 training command with AMP (automatic mixed precision) enabled
    # Write timestamp to train_log.txt before starting training
    with open("train_log.txt", "w") as log_file:
        log_file.write(f"Training started at: {datetime.datetime.now()}\n\n")
    command = (
        'start "" cmd /c "yolo task=detect mode=train '
        'model=yolo11m.pt '
        'data=data/fridge_data_v2.1/data.yaml '
        'epochs=100 imgsz=512 batch=32 name=fridge_yolo11_v1.1 cache=disk '
        'device=0 amp=True workers=12 >> train_log.txt 2>&1"'
    )
# Launch in new CMD window
    subprocess.run(command, shell=True)

def resume_training():
    # YOLOv8 resume training command from last.pt checkpoint
    command = (
        'start "" cmd /c "yolo task=detect mode=train '
        'model=runs/detect/fridge_yolo/weights/last.pt '
        'data=data/fridge_data/data.yaml '
        'epochs=60 imgsz=512 cache=disk '
        'resume=True device=0 amp=True workers=12 freeze=22 > resume_log.txt 2>&1"'
    )
    subprocess.run(command, shell=True)


if __name__ == "__main__":
    torch.cuda.empty_cache()
    start_training()
  
    #resume_training()
