import tkinter as tk
from tkinter import ttk, messagebox
import cv2
import json
import os
import subprocess
import sys

CONFIG_FILE = "config.json"

def save_config(camera_index):
    config = {"camera_index": camera_index}
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f)

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {"camera_index": 0}

def detect_cameras(max_tested=5):
    available = []
    for i in range(max_tested):
        cap = cv2.VideoCapture(i)
        if cap.read()[0]:
            available.append(i)
        cap.release()
    return available

def on_select_camera():
    selected = camera_var.get()
    if selected == "":
        messagebox.showwarning("No selection", "Please select a camera.")
        return
    save_config(int(selected))
    messagebox.showinfo("Camera Selected", f"Camera {selected} saved to config.")

def on_start_app():
    try:
        subprocess.Popen([sys.executable, "main.py"])
    except Exception as e:
        messagebox.showerror("Error", f"Failed to start app: {e}")


def open_config():
    script_path = os.path.join(os.getcwd(), "ui.py")  # full path to ui.py
    subprocess.run([sys.executable, script_path])

# GUI setup
root = tk.Tk()
root.title("AirCursor Main Menu")
root.geometry("400x300")

title = ttk.Label(root, text="AirCursor", font=("Arial", 20))
title.pack(pady=10)

# Camera dropdown
camera_frame = ttk.Frame(root)
camera_frame.pack(pady=10)

ttk.Label(camera_frame, text="Select Camera:").pack(side="left", padx=5)

camera_var = tk.StringVar()
camera_dropdown = ttk.Combobox(camera_frame, textvariable=camera_var, state="readonly")

cameras = detect_cameras()
camera_dropdown["values"] = cameras
if cameras:
    camera_dropdown.set(cameras[0])
camera_dropdown.pack(side="left")

select_button = ttk.Button(root, text="Save Camera", command=on_select_camera)
select_button.pack(pady=5)

# Start app
start_button = ttk.Button(root, text="Start AirCursor", command=on_start_app)
start_button.pack(pady=10)

# Settings
settings_button = ttk.Button(root, text="Configurations", command=open_config)
settings_button.pack()

# Exit
exit_button = ttk.Button(root, text="Exit", command=root.destroy)
exit_button.pack(pady=20)

root.mainloop()