import cv2
import os
import time

# Define paths
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
HAARCASCADE_PATH = os.path.join(
    BASE_DIR, "models", "haarcascade_frontalface_default.xml")
USER_DATA_PATH = os.path.join(BASE_DIR, "dataset", "users")

# Load Haar cascade for face detection
face_cascade = cv2.CascadeClassifier(HAARCASCADE_PATH)


def register_face(user_id, user_name):
    user_folder = os.path.join(USER_DATA_PATH, f"{user_id}_{user_name}")
    os.makedirs(user_folder, exist_ok=True)

    cap = cv2.VideoCapture(0)
    count = 0

    print("Starting face registration. Position yourself in front of the camera.")
    time.sleep(2)

    while count < 100:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            face_img = frame[y:y+h, x:x+w]
            img_path = os.path.join(user_folder, f"{count}.jpg")
            cv2.imwrite(img_path, face_img)
            count += 1

            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, f"Capturing {count}/100", (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        cv2.imshow('Face Registration', frame)
        if cv2.waitKey(100) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print(f"Captured {count} images for user {user_name}.")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Register a user's face")
    parser.add_argument("--id", required=True, help="User ID (e.g., 101)")
    parser.add_argument("--name", required=True,
                        help="User name (e.g., Alice)")

    args = parser.parse_args()

    user_id = args.id.strip()
    user_name = args.name.strip()

    if not user_id.isdigit() or not user_name:
        print("Invalid input. Please enter a numeric ID and a non-empty name.")
    else:
        register_face(user_id, user_name)
