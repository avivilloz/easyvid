from enum import Enum


class Direction(Enum):
    LEFT = "left"
    RIGHT = "right"
    TOP = "top"
    BOTTOM = "bottom"


class EnterTransition(Enum):
    NONE = "none"
    FADEIN = "fadein"
    SLIDEIN = "slidein"


class ExitTransition(Enum):
    NONE = "none"
    FADEOUT = "fadeout"
    SLIDEOUT = "slideout"


class Animation(Enum):
    NONE = "none"
    ZOOM = "zoom"
    ZOOMIN = "zoomin"
    ZOOMOUT = "zoomout"


class TextAnimation(Enum):
    SLIDE_UP_FADE_IN = 1
    NONE = 2
