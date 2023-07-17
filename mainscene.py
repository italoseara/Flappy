import pygame

from gameengine.scene import BaseScene
from objects.background.bush import Bush
from objects.background.city import City
from objects.background.clouds import Clouds
from objects.background.floor import Floor
from objects.bird import Bird
from objects.pipes import PipeGenerator
from objects.ui.message.msg_ready import MsgReady
from objects.ui.pausebutton import PauseButton
from objects.ui.startertip import StarterTip


class MainScene(BaseScene):
    def __init__(self):
        super().__init__()

        self.bg = (11, 200, 215)

        bg = [Clouds(), City(), Bush()]
        buttons = [PauseButton()]
        ui = [MsgReady(), StarterTip()]

        self.bird = Bird()
        self.pipe_generator = PipeGenerator()

        self.add_children(*bg, self.pipe_generator, *buttons, self.bird, Floor(), *ui)

    def update(self):
        if self.program.request_quit:
            pygame.quit()
            raise SystemExit(0)

        super().update()
