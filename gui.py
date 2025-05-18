import tkinter as tk
from tkinter import messagebox
import subprocess
import sys
import os
import threading
import time

# Set base directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Script paths
REGISTER_SCRIPT = os.path.join(BASE_DIR, "src", "core", "face_register.py")
TRAINER_SCRIPT = os.path.join(BASE_DIR, "src", "core", "face_trainer.py")
RECOGNITION_SCRIPT = os.path.join(
    BASE_DIR, "src", "core", "face_recognition.py")
CONVERT_SCRIPT = os.path.join(BASE_DIR, "src", "core", "convertToExcel.py")

# GUI setup
root = tk.Tk()
root.title("PresenSee - Attendance Management")
root.geometry("420x380")
root.resizable(False, False)

title_label = tk.Label(root, text="PresenSee", font=("Helvetica", 20, "bold"))
title_label.pack(pady=15)

status_msg = tk.StringVar()
status_label = tk.Label(root, textvariable=status_msg,
                        fg="blue", font=("Arial", 10))
status_label.pack()


def update_status(message, delay_clear=4):
    status_msg.set(message)
    root.update()
    if delay_clear:
        def clear_msg():
            time.sleep(delay_clear)
            status_msg.set("")
        threading.Thread(target=clear_msg, daemon=True).start()


def run_script(script_path, args=None):
    try:
        command = [sys.executable, script_path]
        if args:
            command.extend(args)
        subprocess.run(command)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to run script:\n{e}")


def register_face():
    # Input dialog for both ID and Name
    popup = tk.Toplevel(root)
    popup.title("Register Face")
    popup.geometry("300x180")
    popup.resizable(False, False)

    tk.Label(popup, text="Enter User ID:").pack(pady=5)
    id_entry = tk.Entry(popup)
    id_entry.pack(pady=5)

    tk.Label(popup, text="Enter User Name:").pack(pady=5)
    name_entry = tk.Entry(popup)
    name_entry.pack(pady=5)

    def submit():
        user_id = id_entry.get().strip()
        user_name = name_entry.get().strip()

        if not user_id.isdigit() or not user_name:
            messagebox.showwarning(
                "Invalid Input", "Please enter a numeric ID and a valid name.")
        else:
            popup.destroy()
            update_status(f"Registering face for {user_name}...")
            # run_script(REGISTER_SCRIPT, [user_id, user_name])
            run_script(REGISTER_SCRIPT, ["--id", user_id, "--name", user_name])
            update_status(f"Face registered for {user_name}.")

    tk.Button(popup, text="Submit", command=submit, width=15).pack(pady=10)


def train_model():
    update_status("Training model...")
    run_script(TRAINER_SCRIPT)
    update_status("Model training completed.")


def recognize_and_mark():
    update_status("Starting face recognition...")
    run_script(RECOGNITION_SCRIPT)
    update_status("Recognition completed.")


def convert_csv_to_excel():
    update_status("Converting CSV to Excel...")
    run_script(CONVERT_SCRIPT)
    update_status("Converted to Excel.")


# Buttons
button_style = {'width': 35, 'height': 2, 'font': ("Arial", 10)}

tk.Button(root, text="Register Face", command=register_face,
          **button_style).pack(pady=5)
tk.Button(root, text="Train Model", command=train_model,
          **button_style).pack(pady=5)
tk.Button(root, text="Recognize & Mark Attendance",
          command=recognize_and_mark, **button_style).pack(pady=5)
tk.Button(root, text="Convert CSV to Excel",
          command=convert_csv_to_excel, **button_style).pack(pady=5)
tk.Button(root, text="Exit", command=root.quit, fg="white",
          bg="red", **button_style).pack(pady=10)

root.mainloop()
