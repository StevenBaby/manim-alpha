
import os
import sys
import inspect
import math as m
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
    # line_spacing = 5


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

    def text_section(self):
        contents = [
            '''
            那三艘怪船出现在印度海岸附近时 天色已晦
            但岸上的渔夫们还是能看清它们的形状
            两艘大船像鲸鱼一样大腹便便
            其两侧凸出向上收起 支撑着船头和船尾坚固的木塔
            木质的船体经风吹雨打变成斑驳的灰色
            船体两侧都伸出很多长长的铁炮 像巨型鲶鱼的触须
            庞大的横帆在浓重的暮色中翻滚 一块比一块壮阔
            每一块横帆上都有一面帽状的上桅帆
            使得整套帆具像一群幽灵巨人
            这些异域来客既有惊心动魄的现代感
            又带着一股粗俗鄙陋的原始气息
            但显然是当地人前所未见的
            ''',
            '''
            海滩上一片惊慌 男人们成群结队
            把四条又长又窄的小船拖进水里
            他们划着桨驶近大船
            看到每块绷紧的帆布上都装饰着巨大的绯红色十字架
            '''
        ]
        before = None

        for content in contents:
            for line in content.splitlines():
                line = line.strip()
                if not line:
                    continue
                if line.startswith("#"):
                    continue

                with self.voiceover(line) as v:
                    text = Text(line, **self.text_kwargs)
                    text.arrange(RIGHT, buff=0.04)
                    if before is None:
                        self.play(Create(text), run_time=2)
                    else:
                        self.play(ReplacementTransform(
                            before, text), run_time=0.5)

                before = text

            before = None
            self.play(FadeOut(text), run_time=0.5)
            self.wait(0.5)

    def axes_section(self):
        axes = Axes(
            #    [start,end,step]
            x_range=[-6, 6, ],
            y_range=[-3, 3, ],
            # Size of each axis
            x_length=13,
            y_length=7,
            # axis_config: the settings you make here
            # will apply to both axis, you have to use the
            # NumberLine options
            axis_config={
                # "include_numbers": True,
                'tip_width': 0.15,
                'include_ticks': False,
            },
            # While axis_config applies to both axis,
            # x_axis_config and y_axis_config only apply
            # to their respective axis.
            # x_axis_config={
            #     "color": RED,
            #     "numbers_to_exclude": [2,3],
            #     "decimal_number_config": {
            #         "color": TEAL,
            #         "unit": "\\rm m",
            #         "num_decimal_places": 0
            #     }
            # },
            # y_axis_config={
            #     "color": WHITE,
            #     "include_tip": False,
            #     "decimal_number_config": {
            #         "color": WHITE,
            #         "unit": "^\\circ",
            #         "num_decimal_places": 1,
            #         "include_sign": True
            #     }
            # },
        )
        axes.add_coordinates()
        plane = NumberPlane(background_line_style={
            'stroke_width': 0.5,
            'stroke_color': random_color(),
        })
        self.play(Create(axes), Create(plane), Create(
            MathTex("O").scale(0.5).move_to([-0.2, -0.2, 1])), run_time=1)

        def f(t): return np.sin(t)
        color = random_color()
        self.play(
            Create(FunctionGraph(
                f,
                stroke_width=2, x_range=[-6, 6, ], color=color,)),
            Create(MathTex(r"f(x) = \sin(x)", color=color,).scale(0.5).move_to(
                np.array([np.pi/2, np.sin(np.pi/2)+0.3, 1])))
        )
        def f(t): return t
        color = random_color()
        self.play(
            Create(FunctionGraph(
                f,
                stroke_width=2, x_range=[-6, 6, ], color=color,)),
            Create(MathTex(r"f(x) = x", color=color,)
                   .scale(0.5)
                   .move_to([-3, f(-3) + 0.3, 1])
                   )
        )
        def f(t): return t - (t**3 / m.factorial(3))
        color = random_color()
        self.play(
            Create(FunctionGraph(
                f,
                stroke_width=2, x_range=[-6, 6, ], color=color,)),
            Create(MathTex(r"f(x) = x - {x^3 \over 3!}", color=color)
                   .scale(0.5)
                   .move_to([-3, f(-3) + 0.5, 1]))
        ),
        def f(t): return t - (t**3 / m.factorial(3)) + (t**5 / m.factorial(5))
        color = random_color()
        self.play(
            Create(FunctionGraph(
                f,
                stroke_width=2, x_range=[-6, 6, ], color=color,)),
            Create(MathTex(r"f(x) = x - {x^3 \over 3!} + {x^5 \over 5!}", color=color,)
                   .scale(0.5)
                   .move_to([PI, f(PI) + 1.3, 1]))
        ),

    def construct(self):
        # self.camera.background_color = '#00ff00'

        self.set_speech_service(speech_service=RedTTSService())

        self.text_kwargs = get_kwargs(TextKwargs)
        self.text_section()
        self.axes_section()
        formula1 = Tex("$x = {-b \pm \sqrt{b^2 - 4ac} \over 2a}$")
        formula2 = Tex(r"$\begin{bmatrix} a & b \\ c & d \end{bmatrix}$")
        group = VGroup(formula1)

        # self.play(ReplacementTransform(text, fomula), run_time=2)
        self.play(Create(group))
        self.play(ScaleInPlace(group, 2), rate_func=smooth, run_time=2)
        self.play(ScaleInPlace(group, 0.5), rate_func=smooth, run_time=2)

        group = VGroup(
            *[
                Tex(rf'${var}$')
                for var in "y=f(x)"
            ]
        )
        group.arrange(RIGHT, buff=0.1)
        group = Tex("$y=f(x)$")
        group = MathTex("x = {-b \pm \sqrt{b^2 - 4ac} \over 2a}")
        self.play(Create(group))
        self.play(Indicate(VGroup(group[0][4], group[0][6])), run_time=1,
          rate_func=smooth,
          )
        self.play(Indicate(group[0][-1]), run_time=1,
                #   rate_func=smooth,
                  )
        self.play(FadeOut(group[0][-2]), rate_func=smooth, run_time=1)

    # It is important to omit the indentation
        code = \
'''from manim import *
"""

"""
def custom_mob(mob):
    mob.scale(3)
    mob.set_color(RED)

class MyScene(Scene):
    def construct(self):
        s = Square()
        self.play(FadeIn(s))
        self.play(s.animate.scale(2))
        self.play(ApplyFunc(custom_mob,s))
        self.wait()
'''
        rendered_code = Code(
                                code=code,
                                tab_width=4,
                                # background="window",
                                language="Python",
                                font="Fira Code",
                                # style="monokai",
                                line_spacing=0.5
        )
        self.add(rendered_code)

        self.wait(1)
