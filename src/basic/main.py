# https://docs.devtaoism.com/docs/html/contents/_1_basic_elements.html

# Import manim library
from manim import *

class SceneName(Scene):
    """
    By convention, the structure of your animation
    is defined in the construct method, but later
    we will learn how to do it in different ways.
    """
    def construct(self):
        # Create a text using Text class
        text = Text("Hello world")

        # Text animation
        self.play(Write(text))

        # Pause
        self.wait()


class SceneWithoutDuration(Scene):
    def construct(self):
        sq = Square()
        self.add(sq)
        # self.wait()

class MoreAnimations(Scene):
    def construct(self):
        text = Text("Hello world")
        self.play(Write(text))
        self.wait()
        self.play(Rotate(text,PI/2))
        self.wait()
        self.play(Indicate(text))
        self.wait()
        self.play(FocusOn(text))
        self.wait()
        # self.play(ShowCreationThenDestructionAround(text))
        # self.wait()
        self.play(FadeOut(text))
        self.wait()
