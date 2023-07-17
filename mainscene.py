import pygame

from new_gameengine.scene import BaseScene
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

        self.add_children(*bg, *ui, Bird(), Floor())

    def update(self):
        if self.program.request_quit:
            pygame.quit()
            raise SystemExit(0)

        super().update()

    def draw(self):
        super().draw()
        display = self.program.window.display
        pygame.draw.line(
            self.surface,
            (255, 0, 0),
            (0, GameState.Config.ground_line),
            (display.width, GameState.Config.ground_line),
        )
        pygame.draw.rect(display.surface, (255, 0, 0), self.children[-2].rect, 1)
        pygame.draw.rect(display.surface, (255, 0, 0), self.children[-2].hitbox.rect, 1)
