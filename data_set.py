"""User enrollment script.

Captures 100 face images for a new user and stores:
 - Images in dataset/ as User.<id>.<n>.jpg
 - Metadata (name, major, sex, reg_time) in SQLite 'users' table

Press 'q' or ESC to abort early.
"""

import cv2
import sqlite3
import numpy as np
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'usersdatabase.db')
DATASET_DIR = os.path.join(BASE_DIR, 'dataset')

# Connect database
conn = sqlite3.connect(DB_PATH)
cons = conn.cursor()

os.makedirs(DATASET_DIR, exist_ok=True)

# Load cascade classifier file
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("[ERROR] Cannot open webcam. Please check that a camera is connected and not used by another application.")
    conn.close()
    raise SystemExit(1)

# --- New inputs ---
user_name = input("Please enter your name: ").strip()
major = input("Please enter your major: ").strip()
sex = input("Please enter your sex (M/F): ").strip().upper()
if sex not in ("M", "F"):
    print('[WARN] Invalid sex value, storing as blank.')
    sex = ''

Picture_Num = 0
id = None  

lenght_boundingbox = 30
thick_boundingbox  = 5

can_show = True  # Will switch to False if HighGUI (imshow) unsupported

while True:
    ret, img = cap.read()
    if not ret:
        print("[WARN] Frame capture failed, stopping.")
        break

    img = cv2.resize(img, (960,720))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x,y,w,h) in faces:
        Picture_Num += 1

        # Insert user only once
        if id is None:
            reg_time = str(datetime.now())[:16]
            cons.execute(
                'INSERT INTO users (name, major, sex, reg_time) VALUES (?, ?, ?, ?)',
                (user_name, major, sex, reg_time)
            )
            id = cons.lastrowid

        x1, y1 = x + w, y + h
        cv2.rectangle(img, (x,y), (x+w,y+h), (255,255,255), 2)

        # Fancy bounding box
        cv2.line(img, (x,y), (x+lenght_boundingbox,y),(255,0,255), thick_boundingbox)
        cv2.line(img, (x,y), (x,y+lenght_boundingbox),(255,0,255), thick_boundingbox)
        cv2.line(img, (x1,y), (x1-lenght_boundingbox,y),(255,0,255), thick_boundingbox)
        cv2.line(img, (x1,y), (x1,y+lenght_boundingbox),(255,0,255), thick_boundingbox)
        cv2.line(img, (x,y1), (x+lenght_boundingbox,y1),(255,0,255), thick_boundingbox)
        cv2.line(img, (x,y1), (x,y1-lenght_boundingbox),(255,0,255), thick_boundingbox)
        cv2.line(img, (x1,y1), (x1-lenght_boundingbox,y1),(255,0,255), thick_boundingbox)
        cv2.line(img, (x1,y1), (x1,y1-lenght_boundingbox),(255,0,255), thick_boundingbox)

        cv2.putText(img, "Detect Face", (x+5,y-5), cv2.FONT_HERSHEY_PLAIN, 1.5, (0,255,0), 2)
        cv2.putText(img, str(datetime.now())[:16], (600,70), cv2.FONT_HERSHEY_SIMPLEX, 1,(255,255,51),2,cv2.LINE_AA)
        cv2.putText(img, f"Processing {Picture_Num}", (20,70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,255), 2)

        # Save face image
        cv2.imwrite(os.path.join(DATASET_DIR, f"User.{id}.{Picture_Num}.jpg"), gray[y:y+h, x:x+w])
        # Small delay to avoid identical frames & let camera adjust
        cv2.waitKey(50)

        if Picture_Num % 10 == 0:
            print(f"[INFO] Captured {Picture_Num}/100 images for user id {id}")
    cv2.imshow('Enrollment', img)
    key = cv2.waitKey(1) & 0xFF
    if key in (27, ord('q')):
        print('\n[INFO] User aborted capture early.')
        break
    if Picture_Num >= 100: # Capture 100 images per user
        print('\n[INFO] Reached 100 images. Stopping capture.')
        break

cap.release()
if id is not None:
    conn.commit()
conn.close()
cv2.destroyAllWindows()
