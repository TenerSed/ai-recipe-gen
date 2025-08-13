import subprocess
import torch


def start_training():
# YOLOv8 training command with AMP (automatic mixed precision) enabled
		command = (
				'start "" cmd /c "yolo task=detect mode=train '
				'model=yolov8m.pt '
				'data=data/fridge_data/data.yaml '
				'epochs=30 imgsz=512 batch=32 name=fridge_yolo cache=disk '
                'device=0 amp=True workers=12 freeze=22 > train_log.txt 2>&1"'
		)
	# Launch in new CMD window
		subprocess.run(command, shell=True)

def resume_training():
    # YOLOv8 resume training command from last.pt checkpoint
    command = (
        'start "" cmd /c "yolo task=detect mode=train '
        'model=runs/detect/fridge_yolo5/weights/last.pt '
        'data=data/fridge_data/data.yaml '
        'epochs=60 imgsz=512 cache=disk '
        'resume=True device=0 amp=True workers=12 > resume_log.txt 2>&1"'
    )
    subprocess.run(command, shell=True)


if __name__ == "__main__":
	#torch.cuda.empty_cache()
    #start_training()
  
    resume_training()
