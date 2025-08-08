# ai-recipe-gen
An AI-powered recipe generator that recommends and creates recipes using NLP and machine learning

Training via ssh:

start "" cmd /c "yolo task=detect mode=train model=D:/ai-recipe-gen/runs/detect/fridge_yolo5/weights/last.pt data=data/fridge_data/data.yaml epochs=30 imgsz=640 batch=8 name=fridge_yolo resume=True device=0 > train_log.txt 2>&1"

Monitor training via ssh:
powershell Get-Content train_log.txt -Wait
