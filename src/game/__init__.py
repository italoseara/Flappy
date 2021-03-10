import pygame
import shelve
import itertools
import math

from pathlib import Path
from typing import Any

from core.key import InputValue, KeyHandler
from core.entity import SimpleEntity
from core.maths import Vector2
from core.data import PygameSurface
from core.manager import GameManager
from core.font import SpriteFontManager, RegularFontManager
from core.resource import ResourceManager
from core.time import DeltaTime

from .data import GameMode, GameConfig, Gfx, Aud
from .utils import dict_from_pairs, make_color, amount_to_fill_container
from .objects import ScrollingTileH, Player, TBPipes

class GameCore:
    DEFAULT_WIN_SIZE = Vector2(960, 540)

    # TODO: document most variables inside this function
    def __init__(self, save_path, audio_path, resources_path):
        pygame.display.set_mode((1, 1))
        self.deltatime = DeltaTime()
        # paths
        self.save_path = Path(save_path)
        self.audio_path = Path(audio_path)
        self.resources_path = Path(resources_path)

        self.config = GameConfig(
            title = "Flappy Birb",
            debug_mode_default = False,

            win_size = GameCore.DEFAULT_WIN_SIZE,
            blit_base_color = (11, 200, 215),

            scroll_speed = 180,
            jump_speed = -480,
            gravity = 30,
            framerate = 60,

            score_text_font_name = "Cascadia Code, Consolas, Tahoma",
            score_text_font_size = 20,
            score_text_font_color = (255, 255, 255),
            score_text_enabled = True,
            score_text_pos = (15, 10),

            hitbox_line_size = 2,
            hitbox_line_color = (255, 0, 0),

            clouds_parallax_coeff = 0.1,
            city_parallax_coeff = 0.3,
            bush_parallax_coeff = 0.4,
            floor_parallax_coeff = 1,

            pipe_y_offset_range = (-210, -40),
            pipe_y_spacing = 130,
            pipe_x_spacing = 200,

            ground_line = (GameCore.DEFAULT_WIN_SIZE.y - 64),
        )

        def load_gfx_resource(x):
            fpath = self.resources_path / x
            with open(fpath, "r") as f:
                return PygameSurface(pygame.image.load(f).convert_alpha())

        self.gfx = ResourceManager(
            load_gfx_resource,
            {
                # general
                Gfx.ICON: "icon.bmp",

                # font - numbers
                Gfx.CHAR_0: "numbers/0.png",
                Gfx.CHAR_1: "numbers/1.png",
                Gfx.CHAR_2: "numbers/2.png",
                Gfx.CHAR_3: "numbers/3.png",
                Gfx.CHAR_4: "numbers/4.png",
                Gfx.CHAR_5: "numbers/5.png",
                Gfx.CHAR_6: "numbers/6.png",
                Gfx.CHAR_7: "numbers/7.png",
                Gfx.CHAR_8: "numbers/8.png",
                Gfx.CHAR_9: "numbers/9.png",

                # tiles
                Gfx.FLOOR: "tiles/floor.png",
                Gfx.BG_BUSH: "tiles/bush.png",
                Gfx.BG_CITY: "tiles/city.png",
                Gfx.BG_CLOUDS: "tiles/clouds.png",
                Gfx.PIPE_TOP: "tiles/pipe_top.png",
                Gfx.PIPE_BOT: "tiles/pipe_bot.png",

                # bird
                Gfx.BIRD_F0: "bird/bird_f0.png",
                Gfx.BIRD_F1: "bird/bird_f1.png",
                Gfx.BIRD_F2: "bird/bird_f2.png",

                # text
                Gfx.MSG_GAME_OVER: "text/msg_game_over.png",
                Gfx.MSG_FLAPPY: "text/msg_flappy.png",
                Gfx.MSG_READY: "text/msg_ready.png",

                # ui.buttons
                Gfx.BTN_PAUSE_NORMAL: "ui/btn_pause_normal.png",
                Gfx.BTN_PAUSE_PAUSED: "ui/btn_pause_paused.png",
                Gfx.BTN_PLAY: "ui/btn_play.png",
                Gfx.BTN_SCOREBOARD: "ui/btn_scoreboard.png",

                # ui.boxes
                Gfx.BOX_MENU: "ui/box_menu.png",
                Gfx.BOX_END: "ui/box_end.png",

                # ui.etc
                Gfx.STARTER_TIP: "ui/starter_tip.png",
            }
        )

        def load_aud_resource(x):
            fpath = self.audio_path / x
            return pygame.mixer.Sound(str(fpath))

        self.aud = ResourceManager(
            load_aud_resource,
            {
                Aud.WING: "wing.wav",
                Aud.HIT: "hit.wav",
                Aud.POINT: "point.wav",
                Aud.DIE: "die.wav",
            }
        )

        self.clock = pygame.time.Clock()

        self.blit_base_color = make_color(self.config.blit_base_color)

        self.debug_fm = RegularFontManager(
            color = make_color(self.config.score_text_font_color),
            name = self.config.score_text_font_name,
            size = self.config.score_text_font_size,
        )
        self.debug_fm.update_string("")

        self.score_fm = SpriteFontManager(
            font_dict = {
                "0": self.gfx.get(Gfx.CHAR_0),
                "1": self.gfx.get(Gfx.CHAR_1),
                "2": self.gfx.get(Gfx.CHAR_2),
                "3": self.gfx.get(Gfx.CHAR_3),
                "4": self.gfx.get(Gfx.CHAR_4),
                "5": self.gfx.get(Gfx.CHAR_5),
                "6": self.gfx.get(Gfx.CHAR_6),
                "7": self.gfx.get(Gfx.CHAR_7),
                "8": self.gfx.get(Gfx.CHAR_8),
                "9": self.gfx.get(Gfx.CHAR_9),
            },
            padding_px = 0,
        )

        self.debug_mode = self.config.debug_mode_default
        self.save_file = shelve.open(str(self.save_path / "data"))

        # save default value for scoreboard if it doesn't exist
        if "max_score" not in self.save_file:
            self.save_file["max_score"] = 0

        # fill in default values
        self.input_handler = KeyHandler()
        self.input_handler.reserve_keys({
            InputValue.ARROW_UP,
            InputValue.K,
            InputValue.H,
            InputValue.MOUSE_BTN_LEFT,
            InputValue.SPACE,
            InputValue.ESC,
        })
        self.is_running = True
        self.is_paused = False
        self.game_mode = GameMode.START
        self.current_score = 0
        self.turn_timer = 0
        self.after_death_timer = 0
        self.turn_debug_used = False
        self.turn_was_debug_mode = self.debug_mode

        # values to be filled later
        self.distance_to_next_score = 0
        self.front_tiles = None
        self.back_tiles = None
        self.pipes = None
        self.player = Player(
            Vector2(0, 0),
            [
                self.gfx.get(Gfx.BIRD_F0),
                self.gfx.get(Gfx.BIRD_F1),
                self.gfx.get(Gfx.BIRD_F2),
            ],
        )

        r_pause_button_normal = self.gfx.get(Gfx.BTN_PAUSE_NORMAL)
        r_pause_button_paused = self.gfx.get(Gfx.BTN_PAUSE_PAUSED)
        r_scoreboard_button = self.gfx.get(Gfx.BTN_SCOREBOARD)
        r_play_button = self.gfx.get(Gfx.BTN_PLAY)

        self.pause_button = SimpleEntity(
            (self.config.win_size.x - r_pause_button_normal.size.x - 10, 10),
            [r_pause_button_normal, r_pause_button_paused],
        )

        self.scoreboard_button = SimpleEntity(
            (self.config.win_size.x - r_scoreboard_button.size.x - 280, 405),
            [r_scoreboard_button],
        )

        self.play_button = SimpleEntity(
            (self.config.win_size.x - r_play_button.size.x - 520, 405),
            [r_play_button],
        )

        # setup audio
        for chid in range(8):
            pygame.mixer.Channel(chid).set_volume(0.2)

        # TODO: remove these cached variables
        self.c_debug_text = None
        self.c_previous_score = 0
        self.c_score_text_rendered = None

        self.manager = GameManager(
            title = "({}x{}) {}".format(
                self.config.win_size.x,
                self.config.win_size.y,
                self.config.title,
            ),
            win_size = self.config.win_size,
            icon = self.gfx.get(Gfx.ICON),
        )

    def main_loop(self):
        self.prepare_turn()

        while self.is_running:
            self.pre_processing()
            self.processing()
            self.post_processing()

    def prepare_turn(self):
        """Initializes variables for every turn.
        
        A turn is a moment that lasts until a restart (after a death) is done.
        """

        bird_f0_size = self.gfx.get(Gfx.BIRD_F0).size
        
        BIRD_CENTER_OFFSET_X = 50
        BIRD_POS_X = (self.config.win_size.x / 2
                      - bird_f0_size.y / 2
                      - BIRD_CENTER_OFFSET_X)
        BIRD_POS_Y = (self.config.win_size.y / 2
                      - bird_f0_size.y / 2)

        self.player.reset()
        self.player.pos.x = BIRD_POS_X
        self.player.pos.y = BIRD_POS_Y

        self.turn_timer = 0
        self.turn_debug_used = self.debug_mode
        self.after_death_timer = 0
        self.current_score = 0
        self.game_mode = GameMode.START

        self.front_tiles, self.back_tiles = self.make_tiles()

        r_pipes = [
            self.gfx.get(Gfx.PIPE_TOP),
            self.gfx.get(Gfx.PIPE_BOT),
        ]
        self.pipes = [
            TBPipes(
                win_size = self.config.win_size,
                resources = r_pipes,
                speed = (-self.config.scroll_speed),
                x_offset = (self.config.pipe_x_spacing * i),
                y_offset_range = self.config.pipe_y_offset_range,
                y_spacing = self.config.pipe_y_spacing,
            ) for i in range(
                math.floor(self.config.win_size.x / self.config.pipe_x_spacing) + 1
            )
        ]

        player_point_offset_x = self.player.pos.x - (34 * 1.5)
        self.distance_to_next_score = (self.config.win_size.x
                                       - player_point_offset_x)

    def pre_processing(self):
        self.deltatime.process(
            self.clock.tick(self.config.framerate)
        )
        self.input_handler.update_keys()
        self.turn_was_debug_mode = self.debug_mode

    def processing(self):
        if not self.is_paused:
            self.player.process_extra(self.deltatime, self)

            if self.input_handler.upkeys_first():
                # start the game
                if self.game_mode == GameMode.START:
                    self.game_mode = GameMode.PLAYING

                # jump
                if self.game_mode == GameMode.PLAYING:
                    pygame.mixer.Channel(0).play(self.aud.get(Aud.WING))
                    # TODO: turn this into self.player.jump()
                    self.player.speed.y = -8
                    self.player.jump_counter = 0

            if self.game_mode == GameMode.PLAYING:
                for pipe in self.pipes:
                    pipe.process(self.deltatime)

                    if pipe.is_colliding(self.player.hitbox):
                        if not self.debug_mode:
                            self.game_mode = GameMode.DEAD
                            # TODO: turn this into self.player.die()
                            self.player.speed.y = self.config.jump_speed * self.deltatime.get()
                            break

                self.distance_to_next_score -= self.config.scroll_speed * self.deltatime.get()
                if self.distance_to_next_score <= 0:
                    pygame.mixer.Channel(1).play(self.aud.get(Aud.POINT))
                    self.distance_to_next_score += self.config.pipe_x_spacing
                    self.current_score += 1

            if self.game_mode != GameMode.DEAD:
                for tile in itertools.chain(self.front_tiles, self.back_tiles):
                    tile.process()

        if self.input_handler.is_first(InputValue.H):
            self.debug_mode = not self.debug_mode

        should_pause = (
            self.input_handler.is_first(InputValue.ESC)
            and self.game_mode != GameMode.DEAD
            or (
                self.pause_button.hitbox.collidepoint(tuple(self.input_handler.mouse_pos))
                and self.game_mode != GameMode.DEAD
                and self.input_handler.is_first(InputValue.MOUSE_BTN_LEFT)
            )
        )

        # pause the game
        # (can't pause if the game hasn't started, though)
        if should_pause and self.game_mode != GameMode.START:
            self.is_paused = not self.is_paused

        # change pause button sprite depending on whether the game is paused or not
        if self.is_paused:
            self.pause_button.frames.current_index = 1
        else:
            self.pause_button.frames.current_index = 0

        if self.game_mode == GameMode.DEAD:
            if self.after_death_timer == 0:
                # play sounds on death
                # TODO: use Channel(_).get_busy() to find free channels
                pygame.mixer.Channel(2).play(self.aud.get(Aud.HIT))
                pygame.mixer.Channel(3).play(self.aud.get(Aud.DIE))
            elif (self.after_death_timer >= 70
                  and self.play_button.hitbox.collidepoint(tuple(self.input_handler.mouse_pos))
                  and self.input_handler.is_first(InputValue.MOUSE_BTN_LEFT)):
                # restart after death
                self.prepare_turn()

    def post_processing(self):
        # fill screen with sky color
        self.manager.fill_screen(self.blit_base_color)

        # render back tiles
        for obj in self.back_tiles:
            self.manager.render(obj)

        # render pipes
        for obj in self.pipes:
            self.manager.render(obj)

            # render pipe hitboxes
            if self.debug_mode:
                for p in self.pipes:
                    for hitbox in p.get_hitboxes():
                        self.manager.render_rect(
                            rect = hitbox,
                            line_size = self.config.hitbox_line_size,
                            line_color = self.config.hitbox_line_color,
                        )

        self.manager.render(self.player)

        if self.debug_mode:
            self.manager.render_rect(
                rect = self.player.hitbox,
                line_size = self.config.hitbox_line_size,
                line_color = self.config.hitbox_line_color,
            )

        # check if the debug mode has been used on this turn
        if self.game_mode == GameMode.PLAYING:
            self.turn_debug_used |= self.debug_mode

        # render front tiles
        for obj in self.front_tiles:
            self.manager.render(obj)

        # render ground hitbox
        if self.debug_mode:
            self.manager.render_rect(
                rect = (0, self.config.ground_line, *self.config.win_size),
                line_size = self.config.hitbox_line_size,
                line_color = self.config.hitbox_line_color,
            )

        # show initial tip
        if self.game_mode == GameMode.START and not self.is_paused:
            # TODO: center this properly
            self.manager.blit(
                self.gfx.get(Gfx.MSG_READY),
                (222, 20),
            )
            self.manager.blit(
                self.gfx.get(Gfx.STARTER_TIP),
                (450, 200),
            )

        # show pause button
        if self.game_mode == GameMode.PLAYING:
            self.manager.render(self.pause_button)

        # show score text on the top-left corner
        if (self.config.score_text_enabled
            and self.debug_mode
            and self.game_mode == GameMode.PLAYING
            and (self.turn_timer % 60 == 0
                 or self.c_previous_score < self.current_score
                 or self.turn_was_debug_mode != self.debug_mode)):

            self.debug_fm.update_string(
                "(:fps {:.2f} :max-score {})".format(
                    self.clock.get_fps(),
                    self.save_file["max_score"],
                )
            )

        if (self.config.score_text_enabled
            and self.game_mode == GameMode.PLAYING):

            xpos = self.config.win_size.x / 2 - 15 * len(str(self.current_score))
            ypos = 10

            self.score_fm.update_string(str(self.current_score))
            self.manager.blit(
                self.score_fm,
                (xpos, ypos),
            )

        if self.debug_mode:
            self.manager.blit(
                self.debug_fm,
                self.config.score_text_pos,
            )

        # pause menu
        if self.is_paused:
            self.manager.blit(self.gfx.get(Gfx.BOX_MENU), (258, 155))
            self.manager.blit(self.gfx.get(Gfx.MSG_FLAPPY), (222, 20))

        # game over
        if self.game_mode == GameMode.DEAD:
            self.player.animation_timer = 0

            if (self.after_death_timer == 0
                and self.current_score > self.save_file["max_score"]
                and not self.turn_debug_used):
                self.save_file["max_score"] = self.current_score

            if self.after_death_timer >= 70: # wait some time for showing the death screen
                self.manager.blit(self.gfx.get(Gfx.MSG_GAME_OVER), (222, 20))
                self.manager.blit(self.gfx.get(Gfx.BOX_END), (258, 145))
                self.manager.blit(self.gfx.get(Gfx.BTN_PLAY), (280, 405))
                self.manager.blit(self.gfx.get(Gfx.BTN_SCOREBOARD), (520, 405))

            self.after_death_timer += 1

        # update screen
        pygame.display.update()

        for event in pygame.event.get():
            # exit via the QUIT event (window manager-specific)
            if event.type == pygame.QUIT:
                self.is_running = False

        # increase timer
        self.turn_timer += 1

    def make_tiles(self):
        r_floor = self.gfx.get(Gfx.FLOOR)
        r_clouds = self.gfx.get(Gfx.BG_CLOUDS)
        r_bush = self.gfx.get(Gfx.BG_BUSH)
        r_city = self.gfx.get(Gfx.BG_CITY)

        front, back = [], []

        floor_amount = amount_to_fill_container(self.config.win_size.x, r_floor.size.x)
        bg_amount = amount_to_fill_container(self.config.win_size.x, r_clouds.size.x)

        def make_back_tile(parallax_coeff, resource):
            return [ScrollingTileH(
                pos_y = (self.config.ground_line - r_clouds.size.y),
                win_size = self.config.win_size,
                speed = (-self.config.scroll_speed * parallax_coeff * self.deltatime.get()),
                resource = resource,
            )]

        back += make_back_tile(self.config.clouds_parallax_coeff, r_clouds)
        back += make_back_tile(self.config.city_parallax_coeff, r_city)
        back += make_back_tile(self.config.bush_parallax_coeff, r_bush)

        front += [ScrollingTileH(
            pos_y = self.config.ground_line,
            win_size = self.config.win_size,
            speed = (-self.config.scroll_speed * self.config.floor_parallax_coeff * self.deltatime.get()),
            resource = r_floor,
        ) for i in range(floor_amount + 1)]

        return (front, back)
