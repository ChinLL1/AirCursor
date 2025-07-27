# AirCursor

AirCursor is a hand-gesture-controlled cursor system using computer vision and MediaPipe. It replaces traditional mouse controls with intuitive hand movements, enabling hands-free navigation.

## Features

- Real-time hand tracking using MediaPipe
- Cursor movement based on index finger position (customisable)
- Virtual click detection based on finger distance
- Camera selection through a GUI
- Simple configuration management

## Installation

1. **Clone the repository:**

```bash
git clone https://github.com/ChinLL1/AirCursor.git
cd AirCursor
```

2. **Create and activate a virtual environment:**

```
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```
Python 3.10.0 is recommended.

3. **Install dependencies:**

```
pip install -r requirements.txt
```

If requirements.txt is not present, install manually:
```
pip install opencv-python opencv-contrib-python mediapipe pyautogui numpy
```

## Usage

1. **Launch the app:**

```
python app.py
```

2. **From the GUI:**

- Select your preferred camera index and save it.

- Click "Start AirCursor" to begin gesture tracking.

- Click "Configurations" to manually adjust or review config settings.

- Click "Exit" to close the application.

## File Structure

```
AirCursor/
├── main.py                # Core logic for hand tracking and cursor control
├── app.py                 # GUI for camera selection and launching the app
├── ui.py                  # Config UI logic
├── config.json            # Stores user configurations 
├── venv/                  # Virtual environment (excluded in .gitignore)
└── README.md
```

## Configuration

Camera selection is stored in config.json:

```
{
  "camera_index": 0
}
```
Modify this file manually or use the GUI to set it.

## Notes

- Make sure your webcam is accessible and not used by other applications.

- Virtual click functionality depends on precise finger detection; proper lighting is recommended.
