from typing import List
from dataclasses import dataclass
from moviepy.editor import TextClip

from .enums import TextAnimation
from .text_animations import animate_text_clip


__all__ = ["SubtitleWord", "SubtitleLine", "get_subtitle_clips"]


@dataclass
class SubtitleWord:
    text: str
    start: float
    end: float


@dataclass
class SubtitleLine:
    words: List[SubtitleWord]
    start: float
    end: float

    @property
    def text(self) -> str:
        return " ".join(word.text for word in self.words)


def get_subtitle_clips(
    subtitle_lines: List[SubtitleLine],
    screen_width: int,
    font_path: str,
    font_size: int,
    color: str = "white",
    stroke_color: str = "black",
    stroke_width: int = 3,
    kerning: int = -1,
    spacing: int = 0,
    offset_time: float = 0,
    y_position: float = 0.45,
    animation_duration: float = 0.05,
    move_distance: float = 0.05,
    animation: TextAnimation = TextAnimation.NONE,
):
    subtitle_clips = []
    for subtitle_line in subtitle_lines:
        subtitle_clips += get_subtitle_line_clips(
            subtitle_line=subtitle_line,
            screen_width=screen_width,
            font_path=font_path,
            font_size=font_size,
            color=color,
            stroke_color=stroke_color,
            stroke_width=stroke_width,
            kerning=kerning,
            spacing=spacing,
            offset_time=offset_time,
            y_position=y_position,
            animation_duration=animation_duration,
            move_distance=move_distance,
            animation=animation,
        )
    return subtitle_clips


def get_subtitle_line_clips(
    subtitle_line: SubtitleLine,
    screen_width: int,
    font_path: str,
    font_size: int,
    color: str = "white",
    stroke_color: str = "black",
    stroke_width: int = 3,
    kerning: int = -1,
    spacing: int = 0,
    offset_time: float = 0,
    y_position: float = 0.45,
    animation_duration: float = 0.05,
    move_distance: float = 0.05,
    animation: TextAnimation = TextAnimation.NONE,
):
    def get_text_width(text: str):
        clip = TextClip(
            txt=text,
            fontsize=font_size,
            font=font_path,
            color=color,
            stroke_color=stroke_color,
            stroke_width=stroke_width,
            kerning=kerning,
        )
        return clip.size[0]

    def get_start_x_position():
        total_width = 0
        for word in subtitle_line:
            text_width = get_text_width(text=word.text)
            total_width += text_width + spacing
        total_width -= spacing
        start_x_position = (screen_width - total_width) / 2
        return start_x_position

    current_x_position = get_start_x_position()
    x_position = current_x_position / screen_width

    clips = []
    for word in subtitle_line.words:
        clip = (
            TextClip(
                txt=word.text,
                fontsize=font_size,
                font=font_path,
                color=color,
                stroke_color=stroke_color,
                stroke_width=stroke_width,
                kerning=kerning,
            )
            .set_start(word.start + offset_time)
            .set_duration(word.end - word.start)
        )

        clip = animate_text_clip(
            clip=clip,
            x_position=x_position,
            y_position=y_position,
            move_distance=move_distance,
            animation_duration=animation_duration,
            animation=animation,
        )

        clips.append(clip)

        text_width = get_text_width(text=word.text)
        current_x_position += text_width + spacing
        x_position = current_x_position / screen_width

    return clips
