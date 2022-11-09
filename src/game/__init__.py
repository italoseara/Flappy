import pygame
import shelve
import itertools
import math
import time

from pathlib import Path
from typing import Any

from core.key import InputValue, KeyHandler
from core.entity import SimpleEntity
from core.maths import Vector2
from core.data import PygameSurface
from core.manager import GameManager
from core.font import SpriteFontManager, RegularFontManager
from core.resource import ResourceManager

from .data import GameMode, GameConfig, Gfx, Aud
from .utils import dict_from_pairs, make_color, amount_to_fill_container
from .objects import ScrollingTileH, Player, TBPipes

class GameCore:
    DEFAULT_WIN_SIZE = Vector2(960, 540)

    # TODO: document most variables inside this function
    def __init__(self, save_path, audio_path, resources_path):
        # preinitialize pygame's audio mixer
        pygame.mixer.pre_init(44100, -16, 2, 2048)

        # initialize pygame
        pygame.init()

        # paths
        self.save_path = Path(save_path)
        self.audio_path = Path(audio_path)
        self.resources_path = Path(resources_path)

        self._clock = pygame.time.Clock()
        self.wait_for_events = False

        framerate = 60

        self.config = GameConfig(
            title = "Flappy Bird Clone",
            debug_mode_default = False,

            win_size = GameCore.DEFAULT_WIN_SIZE,
            blit_base_color = (11, 200, 215),

            scroll_speed = 200,
            jump_speed = -400,
            gravity = 1410,
            framerate = framerate,

            debug_text_font = "Consolas, Cascadia Code, Tahoma",
            debug_text_font_size = 20,
            debug_text_font_color = (0, 0, 0),
            debug_text_enabled = True,
            debug_text_pos = (15, 510),

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

        self.manager = GameManager(
            title = "({}x{}) {}".format(
                self.config.win_size.x,
                self.config.win_size.y,
                self.config.title,
            ),
            win_size = self.config.win_size,
        )

        self.gfx = ResourceManager(
            load_gfx_resource,
            {
                # general
                Gfx.ICON: "icon.bmp",

                # font - numbers
                Gfx.CHAR_B0: "numbers/big/0.png",
                Gfx.CHAR_B1: "numbers/big/1.png",
                Gfx.CHAR_B2: "numbers/big/2.png",
                Gfx.CHAR_B3: "numbers/big/3.png",
                Gfx.CHAR_B4: "numbers/big/4.png",
                Gfx.CHAR_B5: "numbers/big/5.png",
                Gfx.CHAR_B6: "numbers/big/6.png",
                Gfx.CHAR_B7: "numbers/big/7.png",
                Gfx.CHAR_B8: "numbers/big/8.png",
                Gfx.CHAR_B9: "numbers/big/9.png",

                Gfx.CHAR_S0: "numbers/small/0.png",
                Gfx.CHAR_S1: "numbers/small/1.png",
                Gfx.CHAR_S2: "numbers/small/2.png",
                Gfx.CHAR_S3: "numbers/small/3.png",
                Gfx.CHAR_S4: "numbers/small/4.png",
                Gfx.CHAR_S5: "numbers/small/5.png",
                Gfx.CHAR_S6: "numbers/small/6.png",
                Gfx.CHAR_S7: "numbers/small/7.png",
                Gfx.CHAR_S8: "numbers/small/8.png",
                Gfx.CHAR_S9: "numbers/small/9.png",

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

                # text
                Gfx.MSG_GAME_OVER: "text/msg_game_over.png",
                Gfx.MSG_FLAPPY: "text/msg_flappy.png",
                Gfx.MSG_READY: "text/msg_ready.png",

                # ui.buttons
                Gfx.BTN_PAUSE_NORMAL: "ui/buttons/btn_pause_normal.png",
                Gfx.BTN_PAUSE_PAUSED: "ui/buttons/btn_pause_paused.png",
                Gfx.BTN_PLAY: "ui/buttons/btn_play.png",
                Gfx.BTN_SCOREBOARD: "ui/buttons/btn_scoreboard.png",

                # ui.boxes
                Gfx.BOX_MENU: "ui/boxes/box_menu.png",
                Gfx.BOX_END: "ui/boxes/box_end.png",

                # ui.etc
                Gfx.STARTER_TIP: "ui/etc/starter_tip.png",

                # ui.medals
                Gfx.MEDAL_BRONZE: "ui/medals/medal_bronze.png",
                Gfx.MEDAL_SILVER: "ui/medals/medal_silver.png",
                Gfx.MEDAL_GOLD: "ui/medals/medal_gold.png",
            }
        )

        self.manager.set_icon(self.gfx.get(Gfx.ICON))

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

        self.blit_base_color = make_color(self.config.blit_base_color)

        self.debug_fm = RegularFontManager(
            color = make_color(self.config.debug_text_font_color),
            font_name = self.config.debug_text_font,
            font_size = self.config.debug_text_font_size,
            initial_string = "",
        )

        self.score_big_fm = SpriteFontManager(
            font_dict = {
                str(i): self.gfx.get(eval(f"Gfx.CHAR_B{i}")) for i in range(10)
            },
            padding_px = 3,
        )
        self.score_small_fm = SpriteFontManager(
            font_dict = {
                str(i): self.gfx.get(eval(f"Gfx.CHAR_S{i}")) for i in range(10)
            },
            padding_px = 2,
        )
        self.max_score_fm = SpriteFontManager(
            font_dict = {
                str(i): self.gfx.get(eval(f"Gfx.CHAR_S{i}")) for i in range(10)
            },
            padding_px = 2,
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
            InputValue.W,
            InputValue.H,
            InputValue.MOUSE_BTN_LEFT,
            InputValue.ENTER,
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
        self.last_score = 0
        self.front_tiles = None
        self.back_tiles = None
        self.pipes = None
        self.player = Player(
            Vector2(0, 0),
            [
                self.gfx.get(Gfx.BIRD_F0),
                self.gfx.get(Gfx.BIRD_F1),
            ],
        )

        r_pause_button_normal = self.gfx.get(Gfx.BTN_PAUSE_NORMAL)
        r_pause_button_paused = self.gfx.get(Gfx.BTN_PAUSE_PAUSED)
        r_scoreboard_button = self.gfx.get(Gfx.BTN_SCOREBOARD)
        r_play_button = self.gfx.get(Gfx.BTN_PLAY)

        self.pause_button = SimpleEntity(
            Vector2(self.config.win_size.x - r_pause_button_normal.size.x - 10, 10),
            [r_pause_button_normal, r_pause_button_paused],
        )

        self.scoreboard_button = SimpleEntity(
            Vector2(self.config.win_size.x - r_scoreboard_button.size.x - 280, 405),
            [r_scoreboard_button],
        )

        self.play_button = SimpleEntity(
            Vector2(self.config.win_size.x - r_play_button.size.x - 520, 405),
            [r_play_button],
        )

        # setup audio
        for chid in range(8):
            pygame.mixer.Channel(chid).set_volume(0.2)

        # TODO: remove these cached variables
        self.c_debug_text = None
        self.c_previous_score = 0
        self.c_score_text_rendered = None

        # the time since last frame, in seconds
        self.delta_time = 0.0

        self._time_last_frame_ns = None # this is set in self.pre_processing()

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
        self.distance_to_next_score = 0
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

    def pre_processing(self):
        if self._clock is not None:
            self.delta_time = self._clock.tick(self.config.framerate) / 1_000
            self.pseudo_framerate = self._clock.get_fps()
        else:
            time_now_ns = time.time_ns()
            min_ns_per_frame = 1_000_000_000 // self.config.framerate

            if self._time_last_frame_ns is None:
                ns_since_last_frame = min_ns_per_frame
            else:
                ns_since_last_frame = time_now_ns - self._time_last_frame_ns

            if ns_since_last_frame < min_ns_per_frame:
                time.sleep((min_ns_per_frame - ns_since_last_frame) / 1_000_000_000)

            self.delta_time = ns_since_last_frame / 1_000_000_000
            self.pseudo_framerate = 1_000_000_000 / ns_since_last_frame
            self._time_last_frame_ns = time_now_ns

        self.input_handler.update_keys()
        self.turn_was_debug_mode = self.debug_mode

    def processing(self):
        if not self.is_paused:
            self.player.process_extra(self)
                
            if self.input_handler.upkeys_first():
                # start the game
                if self.game_mode == GameMode.START:
                    self.game_mode = GameMode.PLAYING

                # jump
                if self.game_mode == GameMode.PLAYING:
                    self.player.jump(state=self, sound_fx=self.aud.get(Aud.WING))

            if self.game_mode == GameMode.PLAYING:
                for pipe in self.pipes:
                    pipe.process(self)

                    if pipe.is_colliding(self.player.hitbox):
                        if not self.debug_mode:
                            self.player.die(state=self)
                            break

                pipe_distances = []
                for pipe in self.pipes:
                    distance = pipe.pos.x + pipe.size.x//2 - self.player.pos.x - self.player.size.x//2

                    if distance >= 0:
                        pipe_distances.append(distance)
                     
                self.distance_to_next_score = min(pipe_distances)

                if self.distance_to_next_score <= 10 and (time.time() - self.last_score > .5):
                    pygame.mixer.Channel(1).play(self.aud.get(Aud.POINT))
                    self.last_score = time.time()
                    self.current_score += 1

            if self.game_mode != GameMode.DEAD:
                for tile in itertools.chain(self.front_tiles, self.back_tiles):
                    tile.process(self)

        if self.input_handler.is_first(InputValue.H):
            self.debug_mode = not self.debug_mode

        should_pause = (
            self.input_handler.is_first(InputValue.ESC)
            and self.game_mode != GameMode.DEAD
            or (
                self.pause_button.hitbox.collidepoint(self.input_handler.mouse_pos.to_tuple())
                and self.input_handler.is_first(InputValue.MOUSE_BTN_LEFT)
                and self.game_mode != GameMode.DEAD
            )
        )

        # pause the game
        # (can't pause if the game hasn't started, though)
        if should_pause and self.game_mode != GameMode.START:
            self.is_paused = not self.is_paused
            self.wait_for_events = self.is_paused

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
            elif (
                    self.after_death_timer >= 70 and
                    # Wait for the player to click on restart button
                    (
                        self.play_button.hitbox.collidepoint(self.input_handler.mouse_pos.to_tuple())
                        and self.input_handler.is_first(InputValue.MOUSE_BTN_LEFT)
                    ) 
                    # or wait for the player to press "enter"
                    or self.input_handler.is_first(InputValue.ENTER)
                ):
                # restart after death
                self.prepare_turn()
                self.wait_for_events = False

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
                rect = (0, self.config.ground_line, *self.config.win_size.to_tuple()),
                line_size = self.config.hitbox_line_size,
                line_color = self.config.hitbox_line_color,
            )

            # draw line from player to next pipe
            pygame.draw.line(
                surface=self.manager.screen.into_pygame(), 
                color=(255, 0, 0), 
                start_pos=(
                    self.player.pos.x + self.player.size.x//2, 
                    self.player.pos.y + self.player.size.y//2
                ), 
                end_pos=(
                    self.player.pos.x + self.player.size.x//2 + self.distance_to_next_score, 
                    self.player.pos.y + self.player.size.y//2
                ), 
                width=2
            )

        # show initial tip
        if self.game_mode == GameMode.START and not self.is_paused:
            # TODO: center this properly
            self.manager.blit(
                self.gfx.get(Gfx.MSG_READY),
                Vector2(222, 20),
            )
            self.manager.blit(
                self.gfx.get(Gfx.STARTER_TIP),
                Vector2(450, 200),
            )

        # show pause button
        if self.game_mode == GameMode.PLAYING:
            self.manager.render(self.pause_button)

        # show score text on the top-left corner
        if (self.config.debug_text_enabled
            and self.debug_mode
            and self.game_mode == GameMode.PLAYING
            and (self.turn_timer % 60 == 0
                 or self.c_previous_score < self.current_score
                 or self.turn_was_debug_mode != self.debug_mode)):

            self.debug_fm.update_string(
                f':fps {int(self.pseudo_framerate)} ' + 
                f':max-score {self.save_file["max_score"]} ' +
                f':next-score {round(self.distance_to_next_score)}'
            )

        if (self.config.debug_text_enabled
            and self.game_mode == GameMode.PLAYING):

            self.score_big_fm.update_string(str(self.current_score))

            size = self.score_big_fm.size
            xpos = self.config.win_size.x / 2 - size.x / 2
            ypos = 15 + size.y

            self.manager.blit(
                self.score_big_fm,
                Vector2(xpos, ypos)
            )

        if self.debug_mode:
            self.manager.blit(
                self.debug_fm,
                Vector2.from_tuple(self.config.debug_text_pos),
            )

        #! Removed
        # pause menu
        # if self.is_paused:
            # self.manager.blit(self.gfx.get(Gfx.BOX_MENU), Vector2(258, 155))
            # self.manager.blit(self.gfx.get(Gfx.MSG_FLAPPY), Vector2(222, 20))

        # game over
        if self.game_mode == GameMode.DEAD:
            self.player.animation_timer = 0

            self.score_small_fm.update_string(str(self.current_score))
            self.max_score_fm.update_string(str(self.save_file["max_score"]))

            if (self.after_death_timer == 0
                and self.current_score > self.save_file["max_score"]
                and not self.turn_debug_used):
                self.save_file["max_score"] = self.current_score

            if self.after_death_timer >= 70: # wait some time for showing the death screen
                self.wait_for_events = True
                self.manager.blit(self.gfx.get(Gfx.MSG_GAME_OVER), Vector2(222, 20))
                self.manager.blit(self.gfx.get(Gfx.BOX_END), Vector2(258, 145))
                self.manager.blit(self.gfx.get(Gfx.BTN_PLAY), Vector2(280, 405))
                self.manager.blit(self.gfx.get(Gfx.BTN_SCOREBOARD), Vector2(520, 405))

                # show score
                score_x = 655 - self.score_small_fm.size.x
                self.manager.blit(self.score_small_fm, Vector2(score_x, 235))
                max_score_x = 655 - self.max_score_fm.size.x
                self.manager.blit(self.max_score_fm, Vector2(max_score_x, 320))

                # show medal
                medal = None
                
                if self.current_score >= 60:
                    medal = Gfx.MEDAL_GOLD
                elif self.current_score >= 30:
                    medal = Gfx.MEDAL_SILVER
                elif self.current_score >= 15:
                    medal = Gfx.MEDAL_BRONZE

                if medal:
                    self.manager.blit(self.gfx.get(medal), Vector2(308, 225))
                    
            self.after_death_timer += 1

        # update screen
        pygame.display.update()

        def process_event(event) -> None:
            # exit via the QUIT event (window manager-specific) or the Q key
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
                self.is_running = False

        if self.wait_for_events:
            if (event := pygame.event.wait()).type != pygame.NOEVENT:
                process_event(event)
                while (event := pygame.event.poll()).type != pygame.NOEVENT:
                    process_event(event)
        else:
            while (event := pygame.event.poll()).type != pygame.NOEVENT:
                process_event(event)

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
                speed = (-self.config.scroll_speed * parallax_coeff),
                resource = resource,
            )]

        back += make_back_tile(self.config.clouds_parallax_coeff, r_clouds)
        back += make_back_tile(self.config.city_parallax_coeff, r_city)
        back += make_back_tile(self.config.bush_parallax_coeff, r_bush)

        front += [ScrollingTileH(
            pos_y = self.config.ground_line,
            win_size = self.config.win_size,
            speed = (-self.config.scroll_speed * self.config.floor_parallax_coeff),
            resource = r_floor,
        ) for i in range(floor_amount + 1)]

        return (front, back)
