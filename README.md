# PresenSee – Face Recognition Attendance System

**PresenSee** is a lightweight face recognition-based attendance management system built using OpenCV.  
It captures and recognizes faces through a webcam and marks attendance automatically in a CSV file. The attendance can later be exported to Excel format for easy viewing and reporting.

This project is intended for **learning and prototyping purposes**, using simple and lightweight models.

---

## Features

- Face registration through webcam.
- Face detection and recognition using OpenCV’s LBPH model.
- Auto-generates daily attendance CSV files.
- Exports CSV attendance logs to Excel format.
- Lightweight and easy to run on any system.

---

## Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/PresenSee.git
cd PresenSee
```

### 2. Create and Activate a Virtual Environment (Recommended)

```bash
python3 -m venv venv
source venv/bin/activate  # For Linux/Mac
venv\Scripts\activate     # For Windows
```

### 3. Install Required Packages

```bash
pip install -r requirements.txt
```

### 4. Configuration

All scripts under `src/core/` use a base directory path `BASE_DIR` that must be updated according to your machine:

```python
BASE_DIR = "/absolute/path/to/PresenSee"
```

Make sure to replace it in:
- `face_register.py`
- `face_trainer.py`
- `face_recognition.py`
- `convertToExcel.py`

---

## Project Structure

```
PresenSee/
│
├── attendance/               # Stores daily attendance CSVs (auto-generated)
├── database/                 # Stores Excel exports of attendance
├── dataset/
│   └── users/                # Contains face image folders for each user
├── models/
│   ├── haarcascade_frontalface_default.xml
│   └── trainer.yml
├── src/core/
│   ├── face_register.py      # Script to register new users
│   ├── face_trainer.py       # Trains the recognizer with user images
│   └── face_recognition.py   # Real-time face recognition and attendance
├── convertToExcel.py         # Converts CSV attendance logs to .xlsx
├── requirement.txt
└── README.md
```

---

## How to Use

### 1. Register a New User

```bash
python src/core/face_register.py
```

> Enter user ID and name when prompted. The script will capture 100 images from your webcam.

---

### 2. Train the Model

```bash
python src/core/face_trainer.py
```

> This generates a `trainer.yml` model based on registered face data.

---

### 3. Run Face Recognition and Mark Attendance

```bash
python src/core/face_recognition.py
```

> The camera window will open, and faces will be detected.  
> On successful recognition, attendance will be logged to `/attendance/%d-%B-%Y.csv`.

---

### 4. Export Attendance to Excel

```bash
python convertToExcel.py
```

> Converts the latest attendance CSV to `.xlsx` format and saves it in the `/database/` folder.

---

## Requirements

Only the essentials:
```txt
opencv-contrib-python
pandas
numpy
openpyxl
```

---

## Notes

- Camera auto-closes after a timeout (default: 60 seconds) or if you press `q`.
- Ensure good lighting and clear face visibility for best recognition accuracy.

