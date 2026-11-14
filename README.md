# AI Sports Coach

> **Note:** MediaPipe provides the pose network; this project builds the counting and coaching logic on top of it.

Real-time exercise coach: a convolutional pose-estimation network (MediaPipe BlazePose) extracts body landmarks, joint angles drive a repetition counter and the system gives form feedback.

## Problem statement
Practising alone, athletes get no feedback on repetition counts or range of motion. A camera and pose estimation can provide it.

## Objectives
- Estimate body landmarks from a webcam or a video.
- Compute joint angles for squats, push-ups and biceps curls.
- Count repetitions robustly (hysteresis + smoothing).
- Detect partial repetitions and give feedback.

## Technologies used
Python, OpenCV, MediaPipe Pose (CNN-based), NumPy, pytest

## System architecture
```
video frame ─► PoseEstimator (BlazePose CNN) ─► landmarks ─► joint angle ─► RepCounter (state machine) ─► overlay: reps + feedback
```

## Implementation methodology
Each exercise is declared by three landmarks and thresholds (`coach/exercises.py`). The counter uses a moving average and two thresholds, so jitter around a single threshold cannot double-count.

## Algorithms explained
- **Joint angle** from vectors (arccos of the normalised dot product).
- **Hysteresis state machine** (up -> down -> up = 1 rep).
- **Partial-rep detection**: dips close to, but not reaching, the depth threshold produce feedback.

## Installation guide
```bash
git clone https://github.com/Bouafi-hamza1/ai-sports-coach.git
cd ai-sports-coach
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## How to run
```bash
python run_coach.py --exercise squat --source 0              # webcam, press q to quit
python run_coach.py --exercise curl --source video.mp4 --side right
```

Run the tests with `python -m pytest -q`.

## Results and evaluation
4 unit tests pass for angle maths and the counter (full reps, partial reps, jitter). **The live pose-estimation loop was not executed in my test environment** (MediaPipe not installed there), so camera behaviour is untested. Thresholds are starting values to be tuned on real recordings.

## Future improvements
Train a custom CNN classifier for exercise recognition, form scoring across more joints, session summaries, mobile deployment.
