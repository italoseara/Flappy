from gameengine.basescene import BaseScene
from gameengine.engine import Engine
from objects.background.bush import Bush
from objects.background.city import City
from objects.background.clouds import Clouds
from objects.background.floor import Floor
from objects.bird import Bird
from objects.ui.message.msg_ready import MsgReady
from objects.ui.pausebutton import PauseButton


class MainScene(BaseScene):
    def __init__(self):
        super().__init__()

        self.bg = (11, 200, 215)

        bg = [Clouds(), City(), Bush()]
        ui = [PauseButton(), MsgReady()]

        self.add_children(*bg, Bird(), Floor(), *ui)

    def update(self):
        if Engine.request_quit:
            Engine.system_exit()

        super().update()
