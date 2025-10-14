"""Training script for LBPH face recognizer.

Scans the dataset directory for images named in the pattern:
    User.<id>.<num>.jpg

Generates (or overwrites) model/trainingData.yml.
"""

from __future__ import annotations
import os
import cv2
import numpy as np
from PIL import Image
from typing import Tuple, List

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_DIR = os.path.join(BASE_DIR, 'dataset')
MODEL_DIR = os.path.join(BASE_DIR, 'model')
MODEL_PATH = os.path.join(MODEL_DIR, 'trainingData.yml')

os.makedirs(MODEL_DIR, exist_ok=True)


def get_images_with_id(dataset_dir: str) -> Tuple[np.ndarray, List[np.ndarray]]:
    """Load images and extract numeric IDs from filenames.

    Expected filename format: User.<id>.<num>.jpg
    Returns arrays of IDs and images (grayscale).
    """
    if not os.path.isdir(dataset_dir):
        raise FileNotFoundError(f"Dataset directory not found: {dataset_dir}")

    image_paths = [os.path.join(dataset_dir, f) for f in os.listdir(dataset_dir) if f.lower().endswith('.jpg')]
    if not image_paths:
        raise RuntimeError("No images found in dataset. Run data_set.py first.")

    faces: List[np.ndarray] = []
    ids: List[int] = []
    for image_path in image_paths:
        try:
            file_name = os.path.basename(image_path)
            parts = file_name.split('.')
            if len(parts) < 3 or not parts[1].isdigit():
                print(f"[WARN] Skipping unrecognized filename pattern: {file_name}")
                continue
            face_img = Image.open(image_path).convert('L')
            face_np = np.array(face_img, 'uint8')
            user_id = int(parts[1])
            faces.append(face_np)
            ids.append(user_id)
            cv2.imshow('training', face_np)
            cv2.waitKey(1)
        except Exception as e:
            print(f"[ERROR] Could not process {image_path}: {e}")
    if not faces:
        raise RuntimeError("No valid training images after filtering.")
    return np.array(ids), faces


def train() -> None:
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    ids, faces = get_images_with_id(DATASET_DIR)
    recognizer.train(faces, ids)
    recognizer.save(MODEL_PATH)
    cv2.destroyAllWindows()
    print(f"[OK] Training complete. Model saved to {MODEL_PATH}")


if __name__ == '__main__':
    try:
        train()
    except Exception as exc:
        cv2.destroyAllWindows()
        print(f"[FAIL] Training aborted: {exc}")
