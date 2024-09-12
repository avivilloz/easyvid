from moviepy.editor import TextClip

from .enums import TextAnimation

__all__ = ["animate_text_clip"]


def animate_text_clip(
    clip: TextClip,
    x_position: float,
    y_position: float,
    move_distance: float,
    animation_duration: float,
    animation: TextAnimation,
):
    match animation:
        case TextAnimation.SLIDE_UP_FADE_IN:
            clip = slide_up_fade_in(
                clip=clip,
                x_position=x_position,
                y_position=y_position,
                move_distance=move_distance,
                animation_duration=animation_duration,
            )
        case TextAnimation.NONE:
            set_relative_position(
                clip=clip,
                x_position=x_position,
                y_position=y_position,
            )


def set_relative_position(
    clip: TextClip,
    x_position: float,
    y_position: float,
):
    return clip.set_position((x_position, y_position), relative=True)


def slide_up_fade_in(
    clip: TextClip,
    x_position: float,
    y_position: float,
    move_distance: float,
    animation_duration: float,
):
    return clip.set_position(
        lambda t, x_position=x_position: (
            x_position,
            y_position + move_distance * (1 - min(t / animation_duration, 1)),
        ),
        relative=True,
    ).crossfadein(animation_duration)
