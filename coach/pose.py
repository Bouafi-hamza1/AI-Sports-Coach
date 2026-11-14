"""Pose estimation with MediaPipe BlazePose (a convolutional neural network). Optional dependency."""
from __future__ import annotations

SIDES = {"left": ("LEFT_SHOULDER", "LEFT_ELBOW", "LEFT_WRIST", "LEFT_HIP", "LEFT_KNEE", "LEFT_ANKLE"),
         "right": ("RIGHT_SHOULDER", "RIGHT_ELBOW", "RIGHT_WRIST", "RIGHT_HIP", "RIGHT_KNEE", "RIGHT_ANKLE")}
NAMES = ("shoulder", "elbow", "wrist", "hip", "knee", "ankle")


class PoseEstimator:
    def __init__(self, side: str = "left", min_visibility: float = 0.5) -> None:
        if side not in SIDES:
            raise ValueError("side must be left or right")
        import mediapipe as mp  # lazy: only needed for live video
        self._mp = mp
        self._pose = mp.solutions.pose.Pose(model_complexity=1, min_detection_confidence=0.5,
                                            min_tracking_confidence=0.5)
        self.side, self.min_vis = side, min_visibility

    def landmarks(self, frame_rgb) -> dict | None:
        """Return {name: (x, y)} in normalised image coords, or None if the body is not visible."""
        res = self._pose.process(frame_rgb)
        if not res.pose_landmarks:
            return None
        P = self._mp.solutions.pose.PoseLandmark
        out = {}
        for name, key in zip(NAMES, SIDES[self.side]):
            lm = res.pose_landmarks.landmark[P[key]]
            if lm.visibility < self.min_vis:
                return None
            out[name] = (lm.x, lm.y)
        return out
