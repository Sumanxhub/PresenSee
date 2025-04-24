import cv2
import os
import pandas as pd
from datetime import datetime

# Define paths
BASE_DIR = "/absolute/path/to/PresenSee/"
HAARCASCADE_PATH = os.path.join(
    BASE_DIR, "models", "haarcascade_frontalface_default.xml")
TRAINER_PATH = os.path.join(BASE_DIR, "models", "trainer.yml")
USER_DATA_PATH = os.path.join(BASE_DIR, "dataset", "users")
ATTENDANCE_DIR = os.path.join(BASE_DIR, "attendance")

# Ensure attendance directory exists
os.makedirs(ATTENDANCE_DIR, exist_ok=True)

# Load face recognition model
face_cascade = cv2.CascadeClassifier(HAARCASCADE_PATH)
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read(TRAINER_PATH)

# Load user data
users = {}
for folder in os.listdir(USER_DATA_PATH):
    if "_" in folder:
        user_id, name = folder.split("_", 1)
        users[int(user_id)] = name

# Function to mark attendance per day


def mark_attendance(user_id, user_name):
    now = datetime.now()
    date_str = now.strftime('%d-%B-%Y')
    time_str = now.strftime('%H:%M')
    filename = os.path.join(ATTENDANCE_DIR, f"{date_str}.csv")

    if not os.path.exists(filename):
        df = pd.DataFrame(columns=['ID', 'Name', 'Date', 'Time'])
        df.to_csv(filename, index=False)

    df = pd.read_csv(filename)
    if not ((df['ID'] == str(user_id)) & (df['Date'] == date_str)).any():
        df.loc[len(df)] = [str(user_id), user_name, date_str, time_str]
        df.to_csv(filename, index=False)
        return True
    return False


# Open camera
cap = cv2.VideoCapture(0)
start_time = datetime.now()
recognized_users = {}
recognition_time = 60

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(
        gray, scaleFactor=1.2, minNeighbors=5, minSize=(50, 50))

    for (x, y, w, h) in faces:
        face_id, confidence = recognizer.predict(gray[y:y+h, x:x+w])
        confidence = round(100 - confidence, 2)

        # print(f"Detected ID: {face_id}, Confidence: {confidence}")

        if confidence > 30 and face_id in users:
            user_name = users[face_id]
            color, label = (0, 255, 0), f'{user_name} ({confidence}%)'

            if face_id not in recognized_users:
                recognized_users[face_id] = user_name
                if mark_attendance(face_id, user_name):
                    print(f'Attendance marked for {user_name}')
        else:
            color, label = (0, 0, 235), 'Unknown'

        cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
        cv2.putText(frame, label, (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

    # Instruction to quit
    cv2.putText(frame, f"Press 'q' to quit early", (10, frame.shape[0] - 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    # Show attendance log on screen
    log_y_offset = 30
    log_x_position = frame.shape[1] - 250
    for uid, uname in recognized_users.items():
        cv2.putText(frame, f'Attendance: {uname}', (log_x_position, log_y_offset),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        log_y_offset += 30

    cv2.imshow('Face Recognition - PresenSee', frame)

    # Exit after recognition_time seconds or on 'q' key
    if (datetime.now() - start_time).seconds > recognition_time or cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
