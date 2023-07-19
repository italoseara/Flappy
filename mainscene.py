from constants import Graphics
from gameengine import resources
from gameengine.scene import BaseScene
from objects.background.bush import Bush
from objects.background.city import City
from objects.background.clouds import Clouds
from objects.background.floor import Floor
from objects.bird import Bird
from objects.font import BigFontScore
from objects.pipes import PipeGenerator
from objects.ui.endscreen import EndScreen
from objects.ui.message.msg_ready import MsgReady
from objects.ui.pausebutton import PauseButton
from objects.ui.startertip import StarterTip


class MainScene(BaseScene):
    def __init__(self):
        super().__init__()

        self.bg = (11, 200, 215)

        self.big_font = BigFontScore(
            font_dict={
                str(i): resources.surface.get(Graphics.__dict__[f"CHAR_B{i}"])
                for i in range(10)
            },
            padding_px=3,
        )
        self.big_font = BigFontScore(
            font_dict={
                str(i): resources.surface.get(Graphics.__dict__[f"CHAR_B{i}"])
                for i in range(10)
            },
            padding_px=3,
        )
        self.bird = Bird()
        self.pipe_generator = PipeGenerator()

        bg = [Clouds(), City(), Bush()]
        buttons = [PauseButton()]
        ui = [MsgReady(), StarterTip(), EndScreen()]
        labels = [self.big_font]

        self.add_children(
            *bg, self.pipe_generator, *buttons, self.bird, Floor(), *ui, *labels
        )
