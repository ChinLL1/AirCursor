import cv2
import time
import json
from tracker import HandTracker
from gestures import GestureDetector
from cursor import CursorController

def load_config(path="config.json"):
    with open(path) as f:
        return json.load(f)

def main():
    config = load_config()
    
    cursor_finger_id = config.get("cursor_finger_id", 8)
    sensitivity = config.get("sensitivity", 1.0)
    offset_x = config.get("offset_x", 0.0)
    offset_y = config.get("offset_y", 0.0)
    smoothing = config.get("smoothing", 15)
    threshold = config.get("cursor_update_threshold", 5)

    cap = cv2.VideoCapture(0)
    tracker = HandTracker()
    detector = GestureDetector()

    screen_width = 1920
    screen_height = 1080

    cursor = CursorController(
        screen_width,
        screen_height,
        smoothing=smoothing,
        sensitivity=sensitivity,
        offset_x=offset_x,
        offset_y=offset_y,
        threshold=threshold
    )

    last_cursor_update = 0
    cursor_update_interval = 1 / 200  # 30 FPS max cursor update

    while True:
        ret, frame = cap.read()
        if not ret or frame is None:
            #time.sleep(0.01)
            continue

        frame = cv2.resize(frame, (640, 480))

        landmarks, annotated_frame = tracker.find_hands(frame)

        if landmarks:
            gesture = detector.update(landmarks)

            # Find the landmark corresponding to cursor_finger_id
            finger_landmark = next(((x, y, z) for (id, x, y, z) in landmarks if id == cursor_finger_id), None)
            if finger_landmark:
                x_norm, y_norm = finger_landmark[0], finger_landmark[1]
                now = time.time()
                if (now - last_cursor_update) > cursor_update_interval:
                    cursor.move_cursor(x_norm, y_norm)
                    last_cursor_update = now

            if gesture == 'pinch_start':
                cursor.click_down()
                print("Pinch started! Mouse down.")
            elif gesture == 'pinch_end':
                cursor.click_up()
                print("Pinch released! Mouse up.")

        cv2.imshow("AirCursor", annotated_frame)
        if cv2.waitKey(5) & 0xFF == ord('q'):
            break

    tracker.close()
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
