import cv2
import numpy as np
import os
from PIL import Image

# Define paths
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
USER_DATA_PATH = os.path.join(BASE_DIR, "dataset", "users")
TRAINER_PATH = os.path.join(BASE_DIR, "models", "trainer.yml")

# Initialize face recognizer
recognizer = cv2.face.LBPHFaceRecognizer_create()


def get_images_and_labels(dataset_path):
    face_samples = []
    ids = []

    for user_folder in os.listdir(dataset_path):
        user_path = os.path.join(dataset_path, user_folder)
        if not os.path.isdir(user_path) or "_" not in user_folder:
            continue

        user_id = int(user_folder.split('_')[0])

        for image_file in os.listdir(user_path):
            img_path = os.path.join(user_path, image_file)
            img = Image.open(img_path).convert('L')  # Already cropped
            img_numpy = np.array(img, 'uint8')

            face_samples.append(img_numpy)
            ids.append(user_id)

    return face_samples, np.array(ids)


print("Training face recognizer... This may take a while.")
faces, ids = get_images_and_labels(USER_DATA_PATH)

if len(faces) == 0:
    print("No face data found. Please register users first.")
else:
    recognizer.train(faces, ids)
    recognizer.write(TRAINER_PATH)
    print("Training completed. Model saved at", TRAINER_PATH)
