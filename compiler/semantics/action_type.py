from enum import Enum


class ActionType(Enum):
    GOTO = 0
    REDUCE = 1
    SHIFT = 2
    ACCEPT = 3
