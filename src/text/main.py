
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
    # stroke_color = BLACK
    # stroke_width = 1
    # stroke_opacity = 1
    # background_stroke_opacity: float = 1.0
    # background_stroke_width: float = 0.6


class TextKwargs(Kwargs):
    font = 'DengXian'
    font_size = 30
    weight = BOLD
    line_spacing=5


def get_kwargs(cls: Kwargs):
    kwargs = {}
    for name, val in inspect.getmembers(cls):
        if callable(val):
            continue
        if name.startswith('__'):
            continue
        kwargs[name] = val

    return kwargs


class Video(VoiceoverScene):

    def construct(self):
        # self.camera.background_color = '#00ff00'

        self.set_speech_service(speech_service=RedTTSService())

        kwargs = get_kwargs(TextKwargs)
        # with self.voiceover('木质的船体经风吹雨打变成斑驳的灰色'):
        #     text = Text('木质的船体经风吹雨打变成斑驳的灰色', **kwargs)
        #     text.arrange(RIGHT, buff=0.03)
        #     self.play(Create(text), run_time=2)

        formula1 = Tex("$x = {-b \pm \sqrt{b^2 - 4ac} \over 2a}$")
        # formula2 = Tex(r"$\begin{bmatrix} a & b \\ c & d \end{bmatrix}$")
        group = VGroup(formula1)
        # self.play(ReplacementTransform(text, fomula), run_time=2)
        self.play(Create(group))
        self.play(ScaleInPlace(group, 2), rate_func=smooth, run_time=2)
        self.play(ScaleInPlace(group, 0.5), rate_func=smooth, run_time=2)

        self.wait(1)
