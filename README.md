# AI-Based Face Recognition Attendance for Smart Classrooms

Face registration, LBPH model training, and real-time recognition with attendance logging using OpenCV (Haar + LBPH), SQLite, and CSV.

## Features
- User enrollment (captures 100 face images per user)
- LBPH face recognizer training (`opencv-contrib-python`)
- Real-time recognition + on-screen overlay
- Attendance logging to CSV and optional SQLite attendance table
- Adjustable confidence threshold (trackbar) in detection
- Session duplicate prevention

## Project Structure
```
creat_db.py          # Initialize SQLite (users + attendance tables)
data_set.py          # Enroll new user & capture images
training.py          # Train LBPH model from dataset/
detection.py         # Real-time recognition & attendance logging
model/               # trainingData.yml stored here
dataset/             # Captured face images (User.<id>.<n>.jpg)
usersdatabase.db     # SQLite database (after creat_db.py)
attendance.csv       # Attendance records (appended)
```

## Quick Start (Windows PowerShell)
```powershell
python -m venv .venv
.venv\Scripts\Activate
pip install -r requirements.txt

python creat_db.py           # Initialize DB (safe to re-run)
python data_set.py           # Enroll each user (repeat as needed)
python training.py           # Train model (re-run after adding users)
python detection.py          # Run live recognition
```
Press `q` or `ESC` in the detection window to exit.

## Requirements
See `requirements.txt` (core: opencv-contrib-python, numpy, pillow).

## Workflow Details
1. Enrollment stores user row in `users` and images in `dataset/`.
2. Training scans `dataset/` and builds `model/trainingData.yml`.
3. Detection loads model, recognizes faces, and logs attendance.
4. CSV header columns: `User ID, Name, Major, Sex, Datetime`.
5. DB attendance table (if desired) can be extended for analytics.

## Configuration
Adjust these in `detection.py`:
- `DEFAULT_CONFIDENCE_THRESHOLD`: lower => stricter matches.
- `USE_TRACKBAR`: toggle runtime threshold control.

## Troubleshooting
| Issue | Cause | Fix |
|-------|-------|-----|
| `LBPHFaceRecognizer_create` missing | Wrong OpenCV build | `pip install opencv-contrib-python` |
| No window / imshow error | Headless environment | Use a local machine or full OpenCV build |
| Model not found | Training not run | Run `training.py` after enrollment |
| Low accuracy | Poor lighting / few images | Improve lighting; retrain |

## Future Improvements
- Per-day duplicate suppression
- Face alignment (dlib or mediapipe)
- Flask / FastAPI dashboard
- Export/analytics scripts

## License
MIT License (add LICENSE file).

## Acknowledgements
OpenCV community & standard Haar cascades.
# AI-Based-Face-Recognition-Attendance-for-Smart-Classrooms
