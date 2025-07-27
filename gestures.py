import math

def distance(point1, point2):
    x1, y1, z1 = point1
    x2, y2, z2 = point2
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)

class GestureDetector:
    def __init__(self, pinch_threshold=0.05, hold_frames_threshold=15, fist_threshold=0.2):
        self.pinch_threshold = pinch_threshold
        self.hold_frames_threshold = hold_frames_threshold
        self.fist_threshold = fist_threshold

        self.pinch_active = False
        self.hold_frame_count = 0
        self.paused = False

    def is_pinch(self, landmarks):
        thumb_tip = next(((x,y,z) for (id,x,y,z) in landmarks if id == 4), None)
        index_tip = next(((x,y,z) for (id,x,y,z) in landmarks if id == 8), None)

        if thumb_tip is None or index_tip is None:
            return False

        return distance(thumb_tip, index_tip) < self.pinch_threshold

    def is_fist(self, landmarks):
        # Simple fist detection:
        # Calculate average distance from wrist (id 0) to fingertips (ids 4,8,12,16,20)
        wrist = next(((x,y,z) for (id,x,y,z) in landmarks if id == 0), None)
        if wrist is None:
            return False

        fingertip_ids = [4, 8, 12, 16, 20]
        dists = []
        for fid in fingertip_ids:
            tip = next(((x,y,z) for (id,x,y,z) in landmarks if id == fid), None)
            if tip:
                dists.append(distance(wrist, tip))
        if not dists:
            return False

        avg_dist = sum(dists) / len(dists)
        # If avg distance is less than fist_threshold, assume fist
        return avg_dist < self.fist_threshold

    def update(self, landmarks):
        if self.is_fist(landmarks):
            self.paused = True
            # Reset pinch/hold states when paused
            self.pinch_active = False
            self.hold_frame_count = 0
            return 'pause'

        self.paused = False

        pinch_now = self.is_pinch(landmarks)
        gesture = None

        if pinch_now and not self.pinch_active:
            gesture = 'pinch_start'
            self.pinch_active = True
            self.hold_frame_count = 0
        elif pinch_now and self.pinch_active:
            self.hold_frame_count += 1
            if self.hold_frame_count >= self.hold_frames_threshold:
                gesture = 'hold'
            else:
                gesture = 'pinching'
        elif not pinch_now and self.pinch_active:
            gesture = 'pinch_end'
            self.pinch_active = False
            self.hold_frame_count = 0

        return gesture
