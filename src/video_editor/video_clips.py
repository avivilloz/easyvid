import multiprocessing
from typing import List
from moviepy.editor import (
    ImageClip,
    VideoClip,
    VideoFileClip,
    CompositeVideoClip,
    TextClip,
)

from .video_animations import Animation, ExitTransition, EnterTransition
from .video_animator import AutoVideoClipsAnimator

num_cores = multiprocessing.cpu_count()


__all__ = [
    "auto_animate_video_clips",
    "merge_video_clips",
    "extract_video_and_audio_clips",
    "write_video",
]


def auto_animate_video_clips(
    clips: List[VideoClip],
    last_animation: Animation = Animation.NONE,
    only_transitions: bool = False,
    transition_duration: float = 0.3,
    zoom_factor: float = 1.4,
    zoom_smoothness: float = 1.4,
    exclude_exit_transitions: List[ExitTransition] = None,
    exclude_enter_transitions: List[EnterTransition] = None,
    exclude_animations: List[Animation] = None,
):
    return AutoVideoClipsAnimator(
        clips=clips,
        transition_duration=transition_duration,
        animation=last_animation,
        only_transitions=only_transitions,
        zoom_factor=zoom_factor,
        zoom_smoothness=zoom_smoothness,
        exclude_exit_transitions=exclude_exit_transitions,
        exclude_enter_transitions=exclude_enter_transitions,
        exclude_animations=exclude_animations,
    ).animate()


def merge_video_clips(
    clips: list, watermark_clip: ImageClip = None, subtitle_clips: List[TextClip] = None
):
    if watermark_clip:
        clips = [*clips, watermark_clip]

    if subtitle_clips:
        clips = [*clips, *subtitle_clips]

    return CompositeVideoClip(clips)


def extract_video_and_audio_clips(video_path: str):
    video_clip = VideoFileClip(video_path)
    audio_clip = video_clip.audio
    video_clip.audio = None
    return video_clip, audio_clip


def write_video(clip, output_path, max_duration=None):
    if max_duration and clip.duration > max_duration:
        clip = clip.subclip(0, max_duration)
    clip.write_videofile(
        output_path,
        fps=30,
        codec="libx264",
        preset="ultrafast",
        threads=num_cores,
    )
