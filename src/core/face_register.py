import cv2
import os
import time

# Define paths
BASE_DIR = "/absolute/path/to/PresenSee/"
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
    total_images = 100

    print("Starting face registration. Position yourself in front of the camera.")
    time.sleep(2)  # Give user time to adjust position

    while count < total_images:
        ret, frame = cap.read()
        if not ret:
            print("Camera failed to open.")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(
            gray, scaleFactor=1.2, minNeighbors=5)

        for (x, y, w, h) in faces:
            face_img = gray[y:y+h, x:x+w]  # Capture face in color
            img_path = os.path.join(user_folder, f"{count+1}.jpg")
            cv2.imwrite(img_path, face_img)
            count += 1

            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, f"Capturing {count}/{total_images}", (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        cv2.putText(frame, "Press 'q' to quit early", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        cv2.imshow('Face Registration', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Registration stopped manually.")
            break

    cap.release()
    cv2.destroyAllWindows()
    print(f"Captured {count} images for user: {user_name}")


if __name__ == "__main__":
    user_id = input("Enter User ID (e.g., 101): ").strip()
    user_name = input("Enter User Name (e.g., Alice): ").strip()

    if not user_id.isdigit() or not user_name:
        print("Invalid input. Please enter a numeric ID and a non-empty name.")
    else:
        register_face(user_id, user_name)
