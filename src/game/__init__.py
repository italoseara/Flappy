import pygame
import shelve
import itertools
import math

from pathlib import Path
from typing import Any

from core import key
from core.entity import SimpleEntity
from core.maths import Vector2
from core.data import PygameSurface
from core.manager import GameManager
from core.font import SpriteFont, FontManager

from .data import GameMode, GameConfig, GameCache
from .utils import dict_from_pairs, amount_to_fill_container
from .objects import ScrollingTile, Player, TBPipes # TODO: rename to PipeGap

class GameCore:
    DEFAULT_WIN_SIZE = Vector2(960, 540)

    # TODO: document most variables inside this function
    # resources_path = Path(__file__) / "../../resources" .resolve() .absolute()
    def __init__(self, save_path, audio_path, resources_path):
        # paths
        self.save_path = Path(save_path)
        self.audio_path = Path(audio_path)
        self.resources_path = Path(resources_path)

        self.config = GameConfig(
            title = "Flappy Birb",
            debug_mode_default = False,

            win_size = GameCore.DEFAULT_WIN_SIZE,
            blit_base_color = (11, 200, 215),

            scroll_speed = 3,
            jump_speed = -8.0,
            gravity = 0.5,
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

            resources_dir = self.resources_path,
            resources_wrapper = PygameSurface,
            resources_to_load = [
                # general
                ("icon", "icon.bmp"),

                # font - numbers
                *[(f"font_{n}", f"numbers/{n}.png") for n in range(10)],

                # tiles
                ("floor", "tiles/floor.png"),
                ("bg_bush", "tiles/bush.png"),
                ("bg_city", "tiles/city.png"),
                ("bg_clouds", "tiles/clouds.png"),
                ("pipe_top", "tiles/pipe_top.png"),
                ("pipe_bot", "tiles/pipe_bot.png"),

                # bird
                ("bird_f0", "bird/bird_f0.png"),
                ("bird_f1", "bird/bird_f1.png"),
                ("bird_f2", "bird/bird_f2.png"),

                # text
                ("game_over", "text/msg_game_over.png"),
                ("flappy", "text/msg_flappy.png"),
                ("ready", "text/msg_ready.png"),

                # ui.buttons
                ("pause_normal", "ui/btn_pause_normal.png"),
                ("paused", "ui/btn_pause_paused.png"),
                ("play", "ui/btn_play.png"),
                ("scoreboard", "ui/btn_scoreboard.png"),

                # ui.boxes
                ("menu", "ui/box_menu.png"),
                ("over_menu", "ui/box_end.png"),

                # ui.etc
                ("starter_tip", "ui/starter_tip.png"),
            ],
        )

        self.cache = GameCache(self.config)
        self.clock = pygame.time.Clock()
        self.font = SpriteFont(dict_from_pairs(
            [(str(n), self.cache.get_resource(f"font_{n}")) for n in range(10)]
        ))

        self.debug_mode = self.config.debug_mode_default
        self.save_file = shelve.open(str(self.save_path / "data"))

        # save default value for scoreboard if it doesn't exist
        if "max_score" not in self.save_file:
            self.save_file["max_score"] = 0

        # fill in default values
        self.input_handler = key.KeyHandler()
        self.is_running = True
        self.is_paused = False
        self.game_mode = GameMode.START
        self.current_score = 0
        self.turn_timer = 0
        self.after_death_timer = 0
        self.turn_debug_used = False

        # values to be filled later
        self.distance_to_next_score = 0
        self.front_tiles = None
        self.back_tiles = None
        self.pipes = None
        self.player = Player(
            Vector2(0, 0),
            [self.cache.get_resource(f"bird_f{x}") for x in range(3)],
        )

        r_pause_button_normal = self.cache.get_resource("pause_normal")
        r_pause_button_paused = self.cache.get_resource("paused")
        r_scoreboard_button = self.cache.get_resource("scoreboard")
        r_play_button = self.cache.get_resource("play")

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

        # audio bank
        # TODO: move this somewhere else
        self.ab_wing = pygame.mixer.Sound(str(audio_path / "wing.wav"))
        self.ab_hit = pygame.mixer.Sound(str(audio_path / "hit.wav"))
        self.ab_point = pygame.mixer.Sound(str(audio_path / "point.wav"))
        self.ab_death = pygame.mixer.Sound(str(audio_path / "die.wav"))

        # TODO: find a fast yet good way to do this (enum.IntEnum?)
        # also use @enum.unique
        # and https://stackoverflow.com/questions/29503339/how-to-get-all-values-from-python-enum-class
        # and https://stackoverflow.com/questions/5944708/python-forcing-a-list-to-a-fixed-size
        self.r_menu = self.cache.get_resource("menu")
        self.r_flappy = self.cache.get_resource("flappy")
        self.r_game_over = self.cache.get_resource("game_over")
        self.r_over_menu = self.cache.get_resource("over_menu")
        self.r_play = self.cache.get_resource("play")
        self.r_scoreboard = self.cache.get_resource("scoreboard")

        # TODO: remove these cached variables
        self.c_debug_text = None
        self.c_was_debug_mode = self.debug_mode
        self.c_previous_score = 0
        self.c_score_text_rendered = None

        self.manager = GameManager(
            title = "({}x{}) {}".format(
                self.config.win_size.x,
                self.config.win_size.y,
                self.config.title,
            ),
            win_size = self.config.win_size,
            icon = self.cache.get_resource("icon"),
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

        bird_f0_size = self.cache.get_resource("bird_f0").size
        
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

        r_pipes = [self.cache.get_resource(x) for x in ["pipe_top", "pipe_bot"]]
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
                                       - player_point_offset_x
                                       - self.pipes[0].frames.frame_list[0].size.x
                                       + self.pipes[0]._size.x)

    def pre_processing(self):
        self.clock.tick(self.config.framerate)
        self.input_handler.update_keys()

    def processing(self):
        if not self.is_paused:
            self.player.process_extra(self)

            if self.input_handler.keymap[pygame.K_UP].first:
                # start the game
                if self.game_mode == GameMode.START:
                    self.game_mode = GameMode.PLAYING

                # jump
                if self.game_mode == GameMode.PLAYING:
                    pygame.mixer.Channel(0).play(self.ab_wing)
                    # TODO: turn this into self.player.jump()
                    self.player.speed.y = -8
                    self.player.jump_counter = 0

            if self.game_mode == GameMode.PLAYING:
                for pipe in self.pipes:
                    pipe.process()

                    if pipe.is_colliding(self.player.hitbox):
                        if not self.debug_mode:
                            self.game_mode = GameMode.DEAD
                            # TODO: turn this into self.player.die()
                            self.player.speed.y = self.config.jump_speed
                            break

                self.distance_to_next_score -= self.config.scroll_speed
                if self.distance_to_next_score <= 0:
                    pygame.mixer.Channel(1).play(self.ab_point)
                    self.distance_to_next_score += self.config.pipe_x_spacing
                    self.current_score += 1

            if self.game_mode != GameMode.DEAD:
                for tile in itertools.chain(self.front_tiles, self.back_tiles):
                    tile.process()

        if self.input_handler.keymap[pygame.K_h].first:
            self.debug_mode = not self.debug_mode

        # |= is to `or` what += is to `+`
        # yeah, it's bitwise, but it doesn't matter here, does it?
        should_pause = (self.input_handler.keymap[pygame.K_ESCAPE].first
                        and self.game_mode != GameMode.DEAD)
        should_pause |= (
            self.pause_button.hitbox.collidepoint(self.input_handler.mouse_pos)
            and self.game_mode != GameMode.DEAD
            and self.input_handler.keymap[key.BUTTON_LEFT].first
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
                pygame.mixer.Channel(2).play(self.ab_hit)
                pygame.mixer.Channel(3).play(self.ab_death)
            elif (self.after_death_timer >= 70
                  and self.play_button.hitbox.collidepoint(self.input_handler.mouse_pos)
                  and self.input_handler.keymap[key.BUTTON_LEFT].first):
                # restart after death
                self.prepare_turn()

    def post_processing(self):
        # fill screen with sky color
        self.manager.fill_screen(self.cache.blit_base_color)

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
                self.cache.get_resource("ready"),
                (222, 20),
            )
            self.manager.blit(
                self.cache.get_resource("starter_tip"),
                (450, 200),
            )

        # show pause button
        if self.game_mode == GameMode.PLAYING:
            self.manager.render(self.pause_button)

        # show score text on the top-left corner
        if (self.config.score_text_enabled
            and self.game_mode == GameMode.PLAYING
            and (self.turn_timer % 60 == 0
                 or self.c_previous_score < self.current_score
                 or self.c_was_debug_mode != self.debug_mode
                 or self.c_score_text_rendered is None)):

            if self.debug_mode:
                self.c_debug_text = "[DEBUG] FPS: {} | MaxScore: {} ".format(
                    int(self.clock.get_fps()),
                    self.save_file["max_score"]
                )
            else:
                self.c_debug_text = ""

            self.c_score_text_rendered = self.cache.score_text_font.render(
                self.c_debug_text,
                True,
                self.cache.score_text_font_color
            )

        font_manager = FontManager(
            pos = (self.config.win_size.x / 2 - (15 * len(str(self.current_score))), 10),
            sprite_font = self.font,
            padding_px = 5,
        )

        if (self.config.score_text_enabled
            and self.game_mode == GameMode.PLAYING):
            font_manager.update_string(str(self.current_score))

            self.manager.render(font_manager)
            self.manager.blit(
                PygameSurface(self.c_score_text_rendered),
                self.config.score_text_pos
            )

        # pause menu
        if self.is_paused:
            self.manager.blit(self.r_menu, (258, 155))
            self.manager.blit(self.r_flappy, (222, 20))

        # game over
        if self.game_mode == GameMode.DEAD:
            self.player.animation_timer = 0

            if (self.after_death_timer == 0
                and self.current_score > self.save_file["max_score"]
                and not self.turn_debug_used):
                self.save_file["max_score"] = self.current_score

            if self.after_death_timer >= 70: # wait some time for showing the death screen
                self.manager.blit(self.r_game_over, (222, 20))
                self.manager.blit(self.r_over_menu, (258, 145))
                self.manager.blit(self.r_play, (280, 405))
                self.manager.blit(self.r_scoreboard, (520, 405))

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
        r_floor = self.cache.get_resource("floor")
        r_clouds = self.cache.get_resource("bg_clouds")
        r_bush = self.cache.get_resource("bg_bush")
        r_city = self.cache.get_resource("bg_city")

        front, back = [], []

        floor_amount = amount_to_fill_container(self.config.win_size.x, r_floor.size.x)
        bg_amount = amount_to_fill_container(self.config.win_size.x, r_clouds.size.x)

        def make_back_tile(parallax_coeff, resource):
            return [ScrollingTile(
                pos=(i * r_clouds.size.x, self.config.ground_line - r_clouds.size.y),
                wrap_pos=(bg_amount * r_clouds.size.x),
                speed=(-self.config.scroll_speed * parallax_coeff),
                resource=resource,
            ) for i in range(bg_amount + 1)]

        back += make_back_tile(self.config.clouds_parallax_coeff, r_clouds)
        back += make_back_tile(self.config.city_parallax_coeff, r_city)
        back += make_back_tile(self.config.bush_parallax_coeff, r_bush)

        front += [ScrollingTile(
            pos=(i * r_floor.size.x, self.config.ground_line),
            wrap_pos=(floor_amount * r_floor.size.x),
            speed=(-self.config.scroll_speed * self.config.floor_parallax_coeff),
            resource=r_floor,
        ) for i in range(floor_amount + 1)]

        return (front, back)
