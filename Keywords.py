from enum import Enum


class Elements (Enum):
    VERTEX = 'vertex'
    FACE = 'face'


class Properties (Enum):
    X = 'x'
    Y = 'y'
    Z = 'z'
    RED = 'red'
    GREEN = 'green'
    BLUE = 'blue'


class Channel (Enum):
    RED = 0
    GREEN = 1
    BLUE = 2
    ALPHA = 3


class PixelPosition (Enum):
    NOT_MATCHED = -1
