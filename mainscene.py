import pygame

from gameengine.basescene import BaseScene
from gameengine.display import Display
from gameengine.engine import Engine
from gamestate import GameState
from objects.background.bush import Bush
from objects.background.city import City
from objects.background.clouds import Clouds
from objects.background.floor import Floor
from objects.bird import Bird
from objects.ui.message.msg_ready import MsgReady
from objects.ui.pausebutton import PauseButton
from objects.ui.startertip import StarterTip


class MainScene(BaseScene):
    def __init__(self):
        super().__init__()

        self.bg = (11, 200, 215)

        bg = [Clouds(), City(), Bush()]
        ui = [PauseButton(), MsgReady(), StarterTip()]

        self.add_children(*bg, Bird(), Floor(), *ui)

    def update(self):
        if Engine.request_quit:
            Engine.system_exit()

        super().update()

    def draw(self):
        super().draw()
        pygame.draw.line(
            Display.surface,
            (255, 0, 0),
            (0, GameState.Config.ground_line),
            (Display.width, GameState.Config.ground_line),
        )
        pygame.draw.rect(Display.surface, (255, 0, 0), self.children[3].rect, 1)
        pygame.draw.rect(Display.surface, (255, 0, 0), self.children[3].hitbox.rect, 1)
