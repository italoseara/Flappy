import state
from constants import GameMode, Graphics
from gameengine import resources
from gameengine.graphicnode import GraphicNode


class StarterTip(GraphicNode):
    def __init__(self):
        super().__init__(resources.surface.get(Graphics.STARTER_TIP))
        self.rect.x = 450
        self.rect.y = 200

    def update(self):
        self.active = state.game_mode == GameMode.START

        super().update()


class Medal(GraphicNode):
    def __init__(self):
        self.default_surface = resources.surface.new((88, 88))

        super().__init__(self.default_surface)
        self.rect.x = 308
        self.rect.y = 225

    def update(self):
        super().update()

        if self.surface is self.default_surface:
            if (score_value := self.program.scene.score.current_score_value) >= 60:
                self.surface = resources.surface.get(Graphics.MEDAL_GOLD)
            elif score_value >= 30:
                self.surface = resources.surface.get(Graphics.MEDAL_SILVER)
            elif score_value >= 15:
                self.surface = resources.surface.get(Graphics.MEDAL_BRONZE)
