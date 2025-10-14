# Copilot Instructions for face_detection_open_cv

## Project Overview
This project implements a face detection and recognition system using OpenCV and SQLite. It supports user registration (with face image capture), model training, and real-time face recognition with attendance logging.

## Key Components
- `creat_db.py`: Initializes the SQLite database (`usersdatabase.db`) and creates the `users` table.
- `data_set.py`: Captures face images from webcam, collects user info, and stores images in `dataset/` and user data in the database.
- `training.py`: Trains an LBPH face recognizer on images in `dataset/` and saves the model to `model/trainingData.yml`.
- `detection.py`: Runs real-time face recognition, annotates video, and logs recognized users to `attendance.csv`.
- `dataset/`: Stores face images as `User.<id>.<num>.jpg`.
- `model/`: Stores the trained model file.

## Developer Workflows
- **Initialize DB:** Run `creat_db.py` before first use or after schema changes.
- **Add User:** Run `data_set.py` and follow prompts. Captures 100 images per user.
- **Train Model:** Run `training.py` after adding users/images.
- **Recognize Faces:** Run `detection.py` to start recognition and attendance logging.

## Conventions & Patterns
- Face images are named as `User.<id>.<num>.jpg`.
- All scripts use absolute paths for database/model files.
- Attendance is logged only once per user per session in `detection.py`.
- Uses OpenCV's built-in Haar cascades and LBPH recognizer.

## Integration Points
- SQLite database for user metadata.
- CSV file for attendance logs.
- OpenCV for all image/video processing.

## Tips for AI Agents
- Always ensure the database and model files exist before running detection.
- When adding new scripts, follow the pattern of absolute paths and modular separation (DB, dataset, model, detection).
- For new data flows, update both the database schema and the relevant scripts.
- Use the same face detection and recognition pipeline as in existing scripts for consistency.

## Example Workflow
1. `python creat_db.py`
2. `python data_set.py` (repeat for each user)
3. `python training.py`
4. `python detection.py`

Refer to each script for further details on arguments and logic.
