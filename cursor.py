from pynput.mouse import Controller, Button

class CursorController:
    def __init__(self, screen_width, screen_height, smoothing=7, sensitivity=1.0, offset_x=0.0, offset_y=0.0, threshold=5):
        self.mouse = Controller()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.smoothing = smoothing
        self.sensitivity = sensitivity
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.threshold = threshold
        self.prev_x, self.prev_y = 0, 0
        self.clicking = False

    def move_cursor(self, x_norm, y_norm):
        # Apply sensitivity and offset, clamp between 0 and 1
        x_adj = min(max((x_norm - 0.5) * self.sensitivity + 0.5 + self.offset_x, 0), 1)
        y_adj = min(max((y_norm - 0.5) * self.sensitivity + 0.5 + self.offset_y, 0), 1)

        x = int(x_adj * self.screen_width)
        y = int(y_adj * self.screen_height)

        # Move only if movement exceeds threshold
        if abs(x - self.prev_x) < self.threshold and abs(y - self.prev_y) < self.threshold:
            return

        curr_x = self.prev_x + (x - self.prev_x) / self.smoothing
        curr_y = self.prev_y + (y - self.prev_y) / self.smoothing

        self.mouse.position = (curr_x, curr_y)

        self.prev_x, self.prev_y = curr_x, curr_y

    def click_down(self):
        if not self.clicking:
            self.mouse.press(Button.left)
            self.clicking = True

    def click_up(self):
        if self.clicking:
            self.mouse.release(Button.left)
            self.clicking = False
