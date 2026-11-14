"""python run_coach.py --exercise squat --source 0            (webcam)
   python run_coach.py --exercise curl --source video.mp4 --side right"""
import argparse

import cv2

from coach.counter import RepCounter
from coach.exercises import EXERCISES, driving_angle
from coach.pose import PoseEstimator


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--exercise", choices=EXERCISES, required=True)
    ap.add_argument("--source", default="0")
    ap.add_argument("--side", default="left", choices=["left", "right"])
    a = ap.parse_args()
    cap = cv2.VideoCapture(int(a.source) if a.source.isdigit() else a.source)
    if not cap.isOpened():
        raise SystemExit(f"Cannot open source: {a.source}")
    ex, pose = EXERCISES[a.exercise], PoseEstimator(a.side)
    counter, state = RepCounter(ex), {"reps": 0, "angle": 0, "feedback": None}
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        lm = pose.landmarks(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        if lm:
            state = counter.update(driving_angle(ex, lm))
        label = f"{ex.name} reps: {state['reps']}  angle: {state['angle']}"
        cv2.putText(frame, label, (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        if state.get("feedback"):
            cv2.putText(frame, state["feedback"], (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 165, 255), 2)
        cv2.imshow("AI Sports Coach (q to quit)", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    cap.release(); cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
