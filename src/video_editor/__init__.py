import moviepy.config as cfg

cfg.change_settings({"IMAGEMAGICK_BINARY": "magick"})

from .image_clips import *
from .video_clips import *
from .audio_clips import *
from .text_clips import *
from .enums import *
