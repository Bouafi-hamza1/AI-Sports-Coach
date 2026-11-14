import math
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from coach.angles import joint_angle  # noqa: E402
from coach.counter import RepCounter  # noqa: E402
from coach.exercises import EXERCISES  # noqa: E402


def test_joint_angle_known_values():
    assert joint_angle((1, 0), (0, 0), (0, 1)) == pytest.approx(90)
    assert joint_angle((1, 0), (0, 0), (-1, 0)) == pytest.approx(180)
    assert joint_angle((1, 0), (0, 0), (1, 0)) == pytest.approx(0)
    with pytest.raises(ValueError):
        joint_angle((0, 0), (0, 0), (1, 1))


def wave(lo, hi, n=30):
    """One smooth cycle hi -> lo -> hi."""
    return [hi - (hi - lo) * (0.5 - 0.5 * math.cos(2 * math.pi * i / n)) for i in range(n + 1)]


def test_counts_full_reps():
    c = RepCounter(EXERCISES["squat"], smooth=1)
    for _ in range(5):
        for a in wave(80, 175):
            c.update(a)
    assert c.reps == 5 and c.partials == 0


def test_partial_rep_not_counted_and_gives_feedback():
    c = RepCounter(EXERCISES["squat"], smooth=1)
    last = None
    for a in wave(115, 175):           # dips to 115: above `down` (100), below down+margin (125)
        last = c.update(a)
    assert c.reps == 0 and c.partials == 1
    assert "deeper" in c.feedback


def test_jitter_near_threshold_does_not_double_count():
    c = RepCounter(EXERCISES["curl"], smooth=1)
    seq = [170, 40, 55, 45, 60, 40, 170, 172, 169]
    for a in seq:
        c.update(a)
    assert c.reps == 1
