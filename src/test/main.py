
import os
import sys
import inspect
from manim import *
from manim_voiceover import VoiceoverScene

dirname = os.path.dirname(os.path.abspath(__file__))
srcname = os.path.dirname(dirname)
sys.path.insert(0, srcname)

from tts.redtts import RedTTSService  # noqa


class Kwargs(object):

    color = WHITE
    stroke_color = BLACK
    stroke_width = 1
    stroke_opacity = 0.6
    background_stroke_opacity: float = 1.0
    background_stroke_width: float = 0.6


def get_kwargs():
    kwargs = {}
    for name, val in inspect.getmembers(Kwargs):
        if callable(val):
            continue
        if name.startswith('__'):
            continue
        kwargs[name] = val

    return kwargs


class Video(VoiceoverScene):

    def construct(self):
        self.camera.background_color = WHITE

        self.set_speech_service(speech_service=RedTTSService())

        kwargs = get_kwargs()

        text = []
        stack = []

        text.append('hello 大家好，这里容我狡辩一下，我想说的事情')
        stack.append(Text(text[-1], font='DengXian', **kwargs))
        with self.voiceover(text[-1]) as v:
            self.play(Create(stack[-1]), run_time=2)

        text.append('我看到我的爱恋 我飞到她的身边')
        stack.append(Text(text[-1], font='DengXian', **kwargs))
        with self.voiceover(text[-1]) as v:
            self.play(ReplacementTransform(stack[-2], stack[-1]), run_time=2)

        text.append('我捧出给她的礼物 那是一小块凝固的时间')
        stack.append(Text(text[-1], font='DengXian', **kwargs))
        with self.voiceover(text[-1]) as v:
            self.play(ReplacementTransform(stack[-2], stack[-1]), run_time=2)

        text.append('This also means that if you are inside a utility function')
        stack.append(Text(text[-1], font='DengXian', **kwargs))
        with self.voiceover(text[-1]) as v:
            self.play(ReplacementTransform(stack[-2], stack[-1]), run_time=2)

        text.append(
            'that you are calling inside of your path operation function.')
        stack.append(Text(text[-1], font='DengXian', **kwargs))
        with self.voiceover(text[-1]) as v:
            self.play(ReplacementTransform(stack[-2], stack[-1]), run_time=2)
