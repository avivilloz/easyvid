import random
from typing import List
from moviepy.editor import ImageClip, VideoClip

from .enums import Animation, EnterTransition, ExitTransition
from .video_animations import *

__all__ = ["AutoVideoClipsAnimator"]


class AutoVideoClipsAnimator:
    def __init__(
        self,
        clips: List[VideoClip],
        last_animation: Animation = Animation.NONE,
        only_transitions: bool = False,
        transition_duration: float = 0.3,
        zoom_factor: float = 1.4,
        zoom_smoothness: float = 1.4,
        exclude_exit_transitions: List[ExitTransition] = None,
        exclude_enter_transitions: List[EnterTransition] = None,
        exclude_animations: List[Animation] = None,
    ) -> None:
        self.clips = clips
        self.transition_duration = transition_duration
        self.only_transitions = only_transitions
        self.zoom_factor = zoom_factor
        self.zoom_smoothness = zoom_smoothness

        self.animation = last_animation
        self.enter_transition = EnterTransition.NONE
        self.exit_transition = ExitTransition.NONE

        self.exit_transitions = [
            transition
            for transition in list(ExitTransition)
            if transition not in exclude_exit_transitions
        ]

        self.enter_transitions = [
            transition
            for transition in list(EnterTransition)
            if transition not in exclude_enter_transitions
        ]

        self.animations = [
            animation
            for animation in list(Animation)
            if animation not in exclude_animations
        ]

    def animate(self):
        """
        - Zoom animations are added to the existent duration of each clip.
        - Fade transitions happen within the existent duration of each clip.
        - Slide transitions are added to the overall duration of each clip and
          overlap with other clips.
        """
        first_clip = 0
        last_clip = len(self.clips) - 1

        z_ordered_clips = []
        total_duration = 0

        for i, clip in enumerate(self.clips):

            if not self.only_transitions:
                clip = self.add_animation(clip)

            if i > first_clip:
                clip = self.add_enter_transition(clip)

            if i < last_clip:
                clip = self.add_exit_transition(clip)

            offset = 0
            if total_duration and self.enter_transition not in [EnterTransition.FADEIN]:
                offset = self.transition_duration

            total_duration -= offset
            clip = clip.set_start(total_duration)

            total_duration += clip.duration

            if self.enter_transition in [EnterTransition.SLIDEIN]:
                z_ordered_clips.append(clip)
            else:
                z_ordered_clips.insert(0, clip)

        return z_ordered_clips, self.animation

    def add_animation(self, clip):
        final_clip = clip

        if not self.enter_transitions:
            self.animation = Animation.NONE
            return final_clip

        match self.animation:
            case Animation.ZOOM:
                choices = [Animation.ZOOMIN, Animation.NONE]
            case Animation.ZOOMIN:
                choices = [Animation.ZOOMOUT]
            case Animation.ZOOMOUT:
                choices = [Animation.ZOOM, Animation.ZOOMIN, Animation.NONE]
            case Animation.NONE:
                choices = self.animations

        animation = random.choice(choices)

        match animation:
            case Animation.ZOOM:
                final_clip = zoom_in_out(
                    clip=clip,
                    duration=clip.duration,
                    factor=self.zoom_factor,
                    smoothness=self.zoom_smoothness,
                )
            case Animation.ZOOMIN:
                final_clip = zoom_in(
                    clip=clip,
                    duration=clip.duration,
                    factor=self.zoom_factor,
                    smoothness=self.zoom_smoothness,
                )
            case Animation.ZOOMOUT:
                final_clip = zoom_out(
                    clip=clip,
                    duration=clip.duration,
                    factor=self.zoom_factor,
                    smoothness=self.zoom_smoothness,
                )

        self.animation = animation

        return final_clip

    def add_enter_transition(self, clip):
        final_clip = clip

        if not self.enter_transitions:
            self.enter_transition = EnterTransition.NONE
            return final_clip

        match self.exit_transition:
            case ExitTransition.FADEOUT:
                transition = EnterTransition.FADEIN
            case ExitTransition.SLIDEOUT:
                transition = EnterTransition.NONE
            case ExitTransition.NONE:
                transition = EnterTransition.SLIDEIN

        match transition:
            case EnterTransition.FADEIN:
                final_clip = crossfadein(clip, self.transition_duration / 2)
            case EnterTransition.SLIDEIN:
                frame = get_first_frame(clip=clip)
                scaled_clip = ImageClip(frame)
                slide_in_clip = slide_in(scaled_clip, self.transition_duration)
                final_clip = merge_two_clips(slide_in_clip, clip)
            case ExitTransition.NONE:
                final_clip = clip

        self.enter_transition = transition

        return final_clip

    def add_exit_transition(self, clip):
        final_clip = clip

        if not self.exit_transitions:
            self.exit_transition = ExitTransition.NONE
            return final_clip

        transition = random.choice(self.exit_transitions)

        match transition:
            case ExitTransition.FADEOUT:
                final_clip = crossfadeout(clip, self.transition_duration / 2)
            case ExitTransition.SLIDEOUT:
                frame = get_last_frame(clip=clip)
                scaled_clip = ImageClip(frame)
                slide_out_clip = slide_out(scaled_clip, self.transition_duration)
                final_clip = merge_two_clips(clip, slide_out_clip)
            case ExitTransition.NONE:
                final_clip = clip

        self.exit_transition = transition

        return final_clip
