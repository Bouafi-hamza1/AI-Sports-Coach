"""Repetition counter: hysteresis state machine with smoothing and partial-rep detection."""
from __future__ import annotations

from collections import deque

from .exercises import Exercise


class RepCounter:
    """A rep = angle goes below `down` then back above `up`.
    A movement that dips below `down + margin` but never reaches `down` is a partial rep:
    it is not counted and produces feedback."""

    def __init__(self, exercise: Exercise, smooth: int = 3, partial_margin: float = 25.0) -> None:
        self.ex, self.reps, self.partials = exercise, 0, 0
        self.stage = "up"
        self.window: deque[float] = deque(maxlen=smooth)
        self.margin = partial_margin
        self._dipped = False          # went below down+margin during this cycle
        self.feedback: str | None = None

    def update(self, angle: float) -> dict:
        self.window.append(angle)
        a = sum(self.window) / len(self.window)
        completed = False
        if self.stage == "up":
            if a < self.ex.down:
                self.stage, self._dipped, self.feedback = "down", False, None
            elif a < self.ex.down + self.margin:
                self._dipped = True
            elif a > self.ex.up and self._dipped:      # came back up without reaching depth
                self.partials += 1
                self.feedback, self._dipped = self.ex.tips["shallow"], False
        elif self.stage == "down" and a > self.ex.up:
            self.stage, completed = "up", True
            self.reps += 1
        return {"reps": self.reps, "stage": self.stage, "angle": round(a, 1),
                "completed": completed, "feedback": self.feedback}
