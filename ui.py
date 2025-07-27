import tkinter as tk
from tkinter import ttk, messagebox
import json

CONFIG_PATH = "config.json"

# Finger IDs & names for dropdown
FINGER_OPTIONS = {
    0: "wrist",
    1: "thumb_cmc",
    2: "thumb_mcp",
    3: "thumb_ip",
    4: "thumb_tip",
    5: "index_finger_mcp",
    6: "index_finger_pip",
    7: "index_finger_dip",
    8: "index_finger_tip",
    9: "middle_finger_mcp",
    10: "middle_finger_pip",
    11: "middle_finger_dip",
    12: "middle_finger_tip",
    13: "ring_finger_mcp",
    14: "ring_finger_pip",
    15: "ring_finger_dip",
    16: "ring_finger_tip",
    17: "pinky_finger_mcp",
    18: "pinky_finger_pip",
    19: "pinky_finger_dip",
    20: "pinky_finger_tip",
}

def load_config():
    try:
        with open(CONFIG_PATH, "r") as f:
            return json.load(f)
    except Exception:
        # Return some sane defaults if file missing or broken
        return {
            "cursor_finger_id": 8,
            "sensitivity": 20,
            "offset_x": 0.0,
            "offset_y": 0.0,
            "smoothing": 15,
            "cursor_update_threshold": 10
        }

def save_config(config):
    try:
        with open(CONFIG_PATH, "w") as f:
            json.dump(config, f, indent=4)
        messagebox.showinfo("Success", "Configuration saved successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save config:\n{e}")

class ConfigApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("AirCursor Configuration")
        self.geometry("400x500")
        self.config = load_config()
        self.create_widgets()

    def create_widgets(self):
        # Cursor Finger dropdown
        tk.Label(self, text="Cursor Finger:").pack(pady=(10, 0))
        self.finger_var = tk.IntVar(value=self.config.get("cursor_finger_id", 8))
        finger_names = [f"{k}: {v}" for k, v in FINGER_OPTIONS.items()]
        self.finger_dropdown = ttk.Combobox(self, values=finger_names, state="readonly")
        # Set current selection index based on value
        current_index = list(FINGER_OPTIONS.keys()).index(self.finger_var.get())
        self.finger_dropdown.current(current_index)
        self.finger_dropdown.pack(pady=5)

        # Sensitivity slider
        tk.Label(self, text="Sensitivity:").pack(pady=(10, 0))
        self.sensitivity_var = tk.DoubleVar(value=self.config.get("sensitivity", 20))
        tk.Scale(self, variable=self.sensitivity_var, from_=1, to=50, orient="horizontal").pack(pady=5)

        # Smoothing slider
        tk.Label(self, text="Smoothing:").pack(pady=(10, 0))
        self.smoothing_var = tk.IntVar(value=self.config.get("smoothing", 15))
        tk.Scale(self, variable=self.smoothing_var, from_=0, to=30, orient="horizontal").pack(pady=5)

        # Offset X
        tk.Label(self, text="Offset X:").pack(pady=(10, 0))
        self.offset_x_var = tk.DoubleVar(value=self.config.get("offset_x", 0.0))
        tk.Entry(self, textvariable=self.offset_x_var).pack(pady=5)

        # Offset Y
        tk.Label(self, text="Offset Y:").pack(pady=(10, 0))
        self.offset_y_var = tk.DoubleVar(value=self.config.get("offset_y", 0.0))
        tk.Entry(self, textvariable=self.offset_y_var).pack(pady=5)

        # Cursor update threshold slider
        tk.Label(self, text="Cursor Update Threshold:").pack(pady=(10, 0))
        self.threshold_var = tk.IntVar(value=self.config.get("cursor_update_threshold", 120))
        tk.Scale(self, variable=self.threshold_var, from_=1, to=300, orient="horizontal").pack(pady=5)

        # Save button
        save_button = tk.Button(self, text="Save Configuration", command=self.save)
        save_button.pack(pady=20)

    def save(self):
        # Parse finger id from dropdown text like "8: index_finger_tip"
        finger_str = self.finger_dropdown.get()
        finger_id = int(finger_str.split(":")[0])

        config = {
            "cursor_finger_id": finger_id,
            "sensitivity": self.sensitivity_var.get(),
            "offset_x": self.offset_x_var.get(),
            "offset_y": self.offset_y_var.get(),
            "smoothing": self.smoothing_var.get(),
            "cursor_update_threshold": self.threshold_var.get()
        }
        save_config(config)

if __name__ == "__main__":
    app = ConfigApp()
    app.mainloop()
