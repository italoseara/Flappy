import os
import pickle

import pygame

import state
from constants import GameMode, Sounds
from gameengine import resources
from gameengine.basenode import BaseNode
from gameengine.scene import BaseScene
from objects.background import Bush, City, Clouds, Floor
from objects.buttons import BtnPause
from objects.labels import BigScoreLabel
from objects.messages import MsgReady
from objects.others import StarterTip
from objects.pipes import Pipes
from objects.player import Player
from objects.ui.endscreen import Ending


class Background(BaseNode):
    def __init__(self):
        super().__init__(Clouds(), City(), Bush())


class Starting(BaseNode):
    def __init__(self):
        super().__init__(MsgReady(), StarterTip())


class Game(BaseNode):
    def __init__(self):
        self.player = Player()
        super().__init__(
            Background(), Pipes(), BtnPause(), self.player, Floor(), BigScoreLabel()
        )


class Score:
    def __init__(self):
        self.file_path = os.path.abspath("score.flappy")
        if not os.path.exists(self.file_path):
            self.registered = []
            self.sorted = []
        else:
            self.registered, self.sorted = pickle.load(open(self.file_path, "rb"))

        self.current_score_value = 0

    def increase(self):
        self.current_score_value += 1
        pygame.mixer.Channel(1).play(resources.sound.get(Sounds.POINT))

    def register(self, new_score):
        self.registered.append(new_score)

    def save(self):
        pickle.dump((self.registered, self.sorted), open(self.file_path, "wb"))


class MainScene(BaseScene):
    def __init__(self):
        super().__init__()
        self.bg = (11, 200, 215)

        self.reset()

    def reset(self):
        self.children.clear()

        state.game_mode = GameMode.START

        self.big_score_label = BigScoreLabel()
        self.score = Score()

        self.game = Game()

        self.add_children(self.game, Starting(), Ending())

    def update(self):
        super().update()

        if self.program.request_quit:
            self.score.save()
