from typing import Tuple
from moviepy.editor import ImageClip

from .utils import list_file_paths

__all__ = ["get_image_clips", "get_watermark_clip"]


def get_image_clips(images_dir: str, total_duration: float, min_image_duration: float):
    image_files = list_file_paths(dir_path=images_dir)
    num_images = len(image_files)

    if num_images == 0:
        return []

    if total_duration < min_image_duration:
        return [ImageClip(image_files[0]).set_duration(total_duration)]

    max_images = total_duration // min_image_duration
    num_images_to_use = min(num_images, int(max_images))
    duration_per_image = total_duration / num_images_to_use

    clips = []
    for i in range(num_images_to_use):
        if i == num_images_to_use - 1:
            clip_duration = total_duration
        else:
            clip_duration = duration_per_image

        clips.append(ImageClip(image_files[i]).set_duration(clip_duration))
        total_duration -= clip_duration

    return clips


def get_watermark_clip(
    watermark_image_path: str,
    duration: float,
    resize: float = 0.2,
    opacity: float = 0.15,
    position: Tuple[str, str] = ("center", "center"),
):
    return (
        ImageClip(watermark_image_path)
        .resize(resize)
        .set_opacity(opacity)
        .set_position(position)
        .set_duration(duration)
    )
