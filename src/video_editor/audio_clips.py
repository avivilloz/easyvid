from moviepy.editor import AudioFileClip, CompositeAudioClip, concatenate_audioclips

__all__ = ["get_audio_clip", "merge_audio_clips"]


def get_audio_clip(audio_path, duration=None, volume=1, offset_time=0):
    audio = AudioFileClip(audio_path)
    audio = audio.volumex(volume)
    if duration:
        num_loops = int(duration / audio.duration) + 1
        audio = concatenate_audioclips([audio] * num_loops)
        audio = audio.subclip(0, duration)
    return audio.set_start(offset_time)


def merge_audio_clips(clips, bg_audio_clip=None):
    if bg_audio_clip:
        clips = [bg_audio_clip.set_start(0), *clips]
    return CompositeAudioClip(clips)
