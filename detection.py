"""Real-time face recognition & attendance logging.

Features:
 - LBPH recognition (opencv-contrib)
 - Duplicate prevention per session
 - CSV logging + optional DB attendance table
 - Adjustable confidence threshold via trackbar
 - Press 'q' or ESC to quit
"""

from __future__ import annotations
import cv2
import numpy as np
import sqlite3
import os
import csv
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'usersdatabase.db')
MODEL_DIR = os.path.join(BASE_DIR, 'model')
TRAINER_PATH = os.path.join(MODEL_DIR, 'trainingData.yml')
CSV_PATH = os.path.join(BASE_DIR, 'attendance.csv')

# Config
DEFAULT_CONFIDENCE_THRESHOLD = 65  # Lower value => stricter match
USE_TRACKBAR = True

def ensure_csv(path: str) -> None:
    if not os.path.isfile(path):
        with open(path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['User ID', 'Name', 'Major', 'Sex', 'Datetime'])


def log_csv(uid: int, name: str, major: str, sex: str, timestamp: str) -> None:
    with open(CSV_PATH, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([uid, name, major, sex, timestamp])


def log_db(conn: sqlite3.Connection, uid: int, timestamp: str) -> None:
    try:
        conn.execute("INSERT INTO attendance (user_id, timestamp) VALUES (?, ?)", (uid, timestamp))
        conn.commit()
    except sqlite3.Error as e:
        print(f"[WARN] Could not insert attendance into DB: {e}")


def main() -> None:
    if not os.path.isfile(TRAINER_PATH):
        print("Please train the data first")
        return

    ensure_csv(CSV_PATH)

    # DB
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Recognition objects
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read(TRAINER_PATH)

    recorded_ids: set[int] = set()  # session-level duplicates

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("[ERROR] Cannot open webcam")
        conn.close()
        return

    cv2.namedWindow('Face Recognition')
    threshold_holder = {'value': DEFAULT_CONFIDENCE_THRESHOLD}

    def on_trackbar(val):  # val 0..100
        threshold_holder['value'] = max(1, val)

    if USE_TRACKBAR:
        cv2.createTrackbar('ConfThresh', 'Face Recognition', DEFAULT_CONFIDENCE_THRESHOLD, 100, on_trackbar)

    while True:
        ret, frame = cap.read()
        if not ret:
            print('[WARN] Frame grab failed, exiting loop.')
            break
        frame = cv2.resize(frame, (960, 720))
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5)

        if len(faces) == 0:
            cv2.putText(frame, 'No face detected', (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

        for (x, y, w, h) in faces:
            roi = gray[y:y+h, x:x+w]
            user_id, conf = recognizer.predict(roi)
            threshold = threshold_holder['value']
            # Lower conf means better match; invert for display percent
            score_pct = max(0, min(100, int(100 - conf)))

            if conf < threshold:
                cursor.execute('SELECT name, major, sex FROM users WHERE id = ?', (user_id,))
                row = cursor.fetchone()
                if row:
                    name, major, sex = row
                    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    if user_id not in recorded_ids:
                        log_csv(user_id, name, major, sex, now)
                        log_db(conn, user_id, now)
                        recorded_ids.add(user_id)
                    color = (40, 200, 40)
                    label = name
                else:
                    color = (128, 128, 255)
                    label = 'Unregistered'
            else:
                color = (0, 0, 230)
                label = 'Unknown'

            cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
            cv2.putText(frame, label, (x+5, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
            cv2.putText(frame, f'{score_pct}%', (x+5, y+h-8), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,255), 2)

        cv2.putText(frame, f'Recorded: {len(recorded_ids)}', (20, 700), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255,255,0), 2)
        cv2.putText(frame, datetime.now().strftime('%H:%M:%S'), (840, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2)

        cv2.imshow('Face Recognition', frame)
        key = cv2.waitKey(30) & 0xFF
        if key in (27, ord('q')):
            break

    cap.release()
    cv2.destroyAllWindows()
    conn.close()


if __name__ == '__main__':
    main()
