"""Exercise definitions: which joint drives the rep count and thresholds (degrees)."""
from __future__ import annotations

from dataclasses import dataclass

from .angles import joint_angle


@dataclass(frozen=True)
class Exercise:
    name: str
    joints: tuple[str, str, str]   # landmarks (a, vertex, c) of the driving angle
    down: float                    # angle below which the "down" phase is reached
    up: float                      # angle above which the "up" phase is reached
    tips: dict                     # rule name -> message


EXERCISES = {
    "squat": Exercise("squat", ("hip", "knee", "ankle"), down=100, up=160,
                      tips={"shallow": "Go deeper: aim for thighs parallel to the floor."}),
    "pushup": Exercise("pushup", ("shoulder", "elbow", "wrist"), down=90, up=160,
                       tips={"shallow": "Lower your chest closer to the floor."}),
    "curl": Exercise("curl", ("shoulder", "elbow", "wrist"), down=50, up=150,
                     tips={"shallow": "Curl higher for a full range of motion."}),
}


def driving_angle(ex: Exercise, lm: dict) -> float:
    a, b, c = (lm[j] for j in ex.joints)
    return joint_angle(a, b, c)
