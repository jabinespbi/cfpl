from enum import Enum


class TransitionType(Enum):
    SHIFT = 1
    REDUCE = 2
    GOTO = 3
    ACCEPT = 4
