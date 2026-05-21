# ai-recipe-gen — Current State

## Project Overview

An ML experimentation project with two main components:

1. **YOLO object detection** — Detects food items in fridge images using YOLOv8/YOLOv11 models.
   Training is orchestrated by `start_training.py` (YOLOv8-medium) and `yolo_nano/start_training.py` (YOLOv8-nano).
   Inference is handled by `predict/auto_detect.py` (watches a folder and runs predictions continuously)
   and `src/test_yolo.py` (one-shot test on `bus.jpg`).
   Trained weights live in `runs/detect/fridge_yolo/` and `yolo_nano/fridge_yolo2/`.

2. **Keras / TensorFlow notebooks**:
   - `notebooks/cnn_identify_nums.ipynb` — CNN for Kaggle MNIST digit recognition (multiple
     architectures including a custom EfficientNetV2-style model with progressive training).
   - `notebooks/ffn_rain_prediction.ipynb` — Feedforward network on Australian weather data
     (via `kagglehub`).

## Run Instructions

### YOLO Inference (watch folder)
```bash
cd predict
python auto_detect.py
# Drop images into predict/inference_images/ — results appear in predict/predictions/
```

### YOLO One-shot Test
```bash
# Run from project root; requires bus.jpg to be present
python src/test_yolo.py
```

### YOLO Training (cross-platform)
```bash
# From project root (requires data/fridge_data/data.yaml + dataset)
python start_training.py
```

### Notebooks
```bash
pip install -r requirements.txt
jupyter notebook notebooks/
```

---

## Issues Table

| ID | Priority | File | Description | Status |
|----|----------|------|-------------|--------|
| 1 | **P0** | `start_training.py` | Mixed tabs/spaces + Windows-only `start "" cmd /c` shell wrapper made `start_training()` unrunnable on macOS/Linux. The tab-indented function body was syntactically inconsistent with the rest of the file. | **Fixed** — rewrote with consistent 4-space indentation and added `sys.platform` guard to emit the right command on Windows vs POSIX. |
| 2 | **P0** | `yolo_nano/start_training.py` | Same mixed tab/space indentation and Windows-only shell command as issue #1. | **Fixed** — same approach as #1. |
| 3 | **P0** | `requirements.txt` | Missing all notebook dependencies: `tensorflow`, `keras`, `keras-cv`, `scikit-learn`, `visualkeras`, `graphviz`, `kagglehub`. Notebooks import all of these; a fresh `pip install -r requirements.txt` would produce an environment that can't run either notebook. | **Fixed** — added the seven missing packages (unpinned to allow compatible resolution). |
| 4 | **P1** | `src/test_yolo.py` | Used `save_dir=` kwarg in `model.predict()`, which was removed in ultralytics 8.x. In current `ultralytics==8.3.169`, this raises a `TypeError` at runtime. | **Fixed** — replaced with `project="runs/detect", name="test"` (the correct API). |
| 5 | **P1** | `data/fridge_data/` | The dataset directory is gitignored and absent. Both training scripts reference `data=data/fridge_data/data.yaml`, so training will fail with "file not found" until the dataset is restored. | **Not fixed** — data must be sourced externally (e.g. from Roboflow/original labeling tool). See note below. |
| 6 | **P2** | `predict/auto_detect.py` | Used bare relative paths (`"inference_images"`, `"predictions"`, `"../runs/..."`) so the script would silently create wrong directories or crash if run from any directory other than `predict/`. Also had no guard against missing model weights — would crash with a cryptic YOLO error. | **Fixed** — paths now resolved relative to `__file__` via `pathlib.Path`, and a clear `FileNotFoundError` is raised if model weights are absent. |
| 7 | **P2** | `notebooks/ffn_rain_prediction.ipynb` (cell 2) | Hardcoded absolute path `/Users/siddheshsongirkar/.cache/kagglehub/...` for the weather CSV. This path does not exist on any other machine (the username is different), so the notebook crashes immediately after the download cell. | **Fixed** — replaced with `os.path.join(path, "weatherAUS.csv")` using the `path` variable returned by `kagglehub.dataset_download()` in the preceding cell. |
| 8 | **P3** | `start_training.py` | `import torch` at the top level but `torch` is never used in the script (the `torch.cuda.empty_cache()` call is commented out). Dead import adds unnecessary overhead. | **Fixed** — removed; replaced with `import sys` (used for platform detection). |
| 9 | **P3** | `predict/predictions2/` | A `predictions2/` directory exists on disk containing one result image, but the script creates/writes to `predictions/`. This is an orphaned output folder from a previous manual rename. | **Not fixed** — safe to delete manually (`rm -rf predict/predictions2/`), but no code change needed. |

---

## Notes on Missing Dataset (`data/fridge_data/`)

The training dataset is intentionally excluded from git (`.gitignore` lists `fridge_data`).
To restore it:
- If originally from Roboflow: re-download with the same workspace/project/version and place at `data/fridge_data/`.
- The `data.yaml` file must define `train:`, `val:`, `nc:`, and `names:` fields matching the labeling used during the runs stored in `runs/detect/fridge_yolo/`.

## Notes on `keras-cv` / `keras_cv.layers.SqueezeAndExcite2D`

`keras-cv` is required by `cnn_identify_nums.ipynb` for the `MBConv` block. As of Keras 3 / keras-cv 0.9+, the `SqueezeAndExcite2D` layer API is stable. If you encounter import errors, pin `keras-cv==0.9.0` and `keras==3.3.3`.
