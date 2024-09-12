import random
from scipy.ndimage import zoom as nd_zoom
from moviepy.editor import CompositeVideoClip
from moviepy.video.fx.all import resize
from .enums import Direction

__all__ = [
    "crossfadein",
    "crossfadeout",
    "get_first_frame",
    "get_last_frame",
    "merge_two_clips",
    "slide_in",
    "slide_out",
    "zoom_in",
    "zoom_out",
    "zoom_in_out",
]


def crossfadein(clip, duration):
    return clip.crossfadein(duration)


def crossfadeout(clip, duration):
    return clip.crossfadeout(duration)


def ease_in_out(t, smoothness=4):
    return t**smoothness / (t**smoothness + (1 - t) ** smoothness)


def get_crop_func(clip, zoom_func):
    def crop_func(get_frame, t):
        frame = get_frame(t)
        scale, x, y = zoom_func(t)

        resized_frame = nd_zoom(frame, (scale, scale, 1), order=1)

        crop_x1 = int((resized_frame.shape[1] - clip.w) / 2)
        crop_y1 = int((resized_frame.shape[0] - clip.h) / 2)
        crop_x2 = crop_x1 + clip.w
        crop_y2 = crop_y1 + clip.h

        return resized_frame[crop_y1:crop_y2, crop_x1:crop_x2]

    return crop_func


def zoom_in(clip, duration, factor=1.3, smoothness=4):
    def zoom(t):
        progress = ease_in_out(t=t / duration, smoothness=smoothness)
        scale = 1 + (factor - 1) * progress
        new_w = clip.w * scale
        new_h = clip.h * scale
        x = (new_w - clip.w) / 2
        y = (new_h - clip.h) / 2
        return scale, x, y

    zoomed = clip.fx(resize, lambda t: zoom(t)[0])
    crop_func = get_crop_func(clip=clip, zoom_func=zoom)

    return zoomed.fl(crop_func).set_duration(duration)


def zoom_out(clip, duration, factor=1.3, smoothness=4):
    def zoom(t):
        progress = ease_in_out(t=t / duration, smoothness=smoothness)
        scale = factor - (factor - 1) * progress
        new_w = clip.w * scale
        new_h = clip.h * scale
        x = (new_w - clip.w) / 2
        y = (new_h - clip.h) / 2
        return scale, x, y

    zoomed = clip.fx(resize, lambda t: zoom(t)[0])
    crop_func = get_crop_func(clip=clip, zoom_func=zoom)

    return zoomed.fl(crop_func).set_duration(duration)


def zoom_in_out(clip, factor=1.3, duration=None, smoothness=4):
    if duration is None:
        duration = clip.duration

    def zoom(t):
        half_duration = duration / 2
        if t <= half_duration:
            progress = ease_in_out(t=t / half_duration, smoothness=smoothness)
            scale = 1 + (factor - 1) * progress
        else:
            progress = ease_in_out(
                t=(t - half_duration) / half_duration, smoothness=smoothness
            )
            scale = factor - (factor - 1) * progress
        new_w = clip.w * scale
        new_h = clip.h * scale
        x = (new_w - clip.w) / 2
        y = (new_h - clip.h) / 2
        return scale, x, y

    zoomed = clip.fx(resize, lambda t: zoom(t)[0])
    crop_func = get_crop_func(clip=clip, zoom_func=zoom)

    return zoomed.fl(crop_func).set_duration(duration)


def slide_in(clip, duration):
    w, h = clip.size
    direction = random.choice(list(Direction))

    if direction == Direction.LEFT:
        slide_in_clip = clip.set_position(lambda t: (w * (-t / duration + 1), 0))
    elif direction == Direction.RIGHT:
        slide_in_clip = clip.set_position(lambda t: (-w * (-t / duration + 1), 0))
    elif direction == Direction.TOP:
        slide_in_clip = clip.set_position(lambda t: (0, h * (-t / duration + 1)))
    elif direction == Direction.BOTTOM:
        slide_in_clip = clip.set_position(lambda t: (0, -h * (-t / duration + 1)))

    return slide_in_clip.set_duration(duration)


def slide_out(clip, duration):
    w, h = clip.size
    direction = random.choice(list(Direction))

    if direction == Direction.LEFT:
        slide_out_clip = clip.set_position(lambda t: (-w * (t / duration), 0))
    elif direction == Direction.RIGHT:
        slide_out_clip = clip.set_position(lambda t: (w * (t / duration), 0))
    elif direction == Direction.TOP:
        slide_out_clip = clip.set_position(lambda t: (0, -h * (t / duration)))
    elif direction == Direction.BOTTOM:
        slide_out_clip = clip.set_position(lambda t: (0, h * (t / duration)))

    return slide_out_clip.set_duration(duration)


def merge_two_clips(clip1, clip2):
    return CompositeVideoClip([clip1.set_start(0), clip2.set_start(clip1.duration)])


def get_first_frame(clip):
    return clip.get_frame(0)


def get_last_frame(clip, initial_offset=0.01, step=0.01, max_attempts=10):
    offset = clip.duration - initial_offset

    for attempt in range(max_attempts):
        if offset < 0:
            raise RuntimeError("Offset went below zero, unable to read the frame.")

        try:
            frame = clip.get_frame(offset)
            return frame
        except Exception as e:
            print(
                f"Attempt {attempt + 1}: Failed to read frame at {offset:.3f} seconds. Error: {e}"
            )
            offset -= step

    raise RuntimeError(f"Failed to read frame after {max_attempts} attempts.")
