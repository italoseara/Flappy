import pygame
from pygame.locals import *

from itertools import chain
from pathlib import Path
from dataclasses import dataclass
from typing import Any
import math
import shelve

from core.input import InputHandler, BUTTON_LEFT, BUTTON_MIDDLE, BUTTON_RIGHT
from core.entity import SimpleEntity
from core.manager import GameManager
from core.data import *
from core.maths import *
from core.font import SpriteFont, FontManager

from .config import GameConfig
from .cache import GameCache
from .objects import ScrollingTile, Player, TBPipes
from .data import GameMode

@dataclass
class GameState:
    """Agrupa valores alteráveis durante o jogo."""
    player: Any
    front_tiles: Any
    back_tiles: Any
    pause_button: Any
    scoreboard_button: Any
    play_button: Any
    pipes: Any
    input_handler: Any
    debug_mode: Any

    game_timer: int = 0
    death_timer: int = 0

    current_score: int = 0

    game_mode: GameMode = GameMode.START
    is_running: bool = True
    is_paused: bool = False

    # kinda-cached variables, not in the cache though
    debug_text: str = None
    debug_used: bool = False
    previous_score: int = 0
    score_text_rendered: Any = None
    distance: int = 0

def main(data_path, audio_path):
    WSIZE = (960, 540)
    
    data = shelve.open(str(data_path/'data'))
    volume = 0.2
    for c in range(8):
        pygame.mixer.Channel(c).set_volume(volume)

    if "max_score" not in data:
        data["max_score"] = 0
    config = GameConfig(
        resources_dir=(Path(__file__) / "../../resources").resolve().absolute(),
        resources_to_load=[
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

        title="A strange flappy bird clone",
        debug_mode=False,

        win_size=WSIZE,
        blit_base_color=(115, 200, 215),

        scroll_speed=3,
        jump_speed=-8.0,
        gravity=0.5,
        framerate=60,

        score_text_font_name="Cascadia Code, Consolas, Tahoma",
        score_text_font_size=20,
        score_text_font_color="white",
        score_text_enabled=True,
        score_text_pos=(15, 10),

        hitbox_line_size=2,
        hitbox_line_color=(255, 0, 0),

        clouds_parallax_coeff=0.1,
        city_parallax_coeff=0.3,
        bush_parallax_coeff=0.4,
        floor_parallax_coeff=1,

        pipe_y_offset_range=(-210, -40),
        pipe_y_spacing=130,
        pipe_x_spacing=200,

        ground_line=(WSIZE[1]-64),
    )

    def pairs_to_dict(pairs_list):
        result = {}
        for (k, v) in pairs_list:
            result[k] = v
        return result

    # Sounds
    wing_sound = pygame.mixer.Sound(str(audio_path/'wing.wav'))
    hit_sound = pygame.mixer.Sound(str(audio_path/'hit.wav'))
    point_sound = pygame.mixer.Sound(str(audio_path/'point.wav'))
    death_sound = pygame.mixer.Sound(str(audio_path/'die.wav'))

    def get_state():
        pause_button_size = image_size(cache.get_resource("pause_normal"))
        scoreboard_button_size = image_size(cache.get_resource("scoreboard"))
        play_button_size = image_size(cache.get_resource("play"))

        pause_button = SimpleEntity(
            (config.win_size[0] - pause_button_size[0] - 10, 10),
            [cache.get_resource("pause_normal"), cache.get_resource("paused")],
        )

        scoreboard_button = SimpleEntity(
            (config.win_size[0] - scoreboard_button_size[0] - 280, 405),
            [cache.get_resource("scoreboard")],
        )

        play_button = SimpleEntity(
            (config.win_size[0] - play_button_size[0] - 520, 405),
            [cache.get_resource("play")],
        )

        player_frames = [cache.get_resource(f"bird_f{x}") for x in range(3)]
        player = Player(BIRD_INITIAL_POS, player_frames)

        return GameState(
            player=player,
            front_tiles=[],
            back_tiles=[],
            pipes=[],
            pause_button=pause_button,
            scoreboard_button=scoreboard_button,
            play_button=play_button,
            input_handler=InputHandler(),
            debug_mode=config.debug_mode,
        )

    def initialize_game():
        state.game_timer = 0
        state.game_mode = GameMode.START
        state.death_timer = 0
        state.current_score = 0
        state.debug_used = False

        state.player.reset()
        state.player.angle_target = 0
        state.player.angle = 0
        state.player.animation_id = 0
        state.player.animation_timer = 0
        state.player.animation_timer_limit = 0
        state.player.speed.y = 0
        state.player.pos.x, state.player.pos.y = BIRD_INITIAL_POS

        state.front_tiles, state.back_tiles = make_tiles()

        pipe_res = [cache.get_resource(x) for x in ["pipe_top", "pipe_bot"]]
        state.pipes = [
            TBPipes(
                win_size=config.win_size,
                resources=pipe_res,
                speed=(-config.scroll_speed),
                x_offset=(config.pipe_x_spacing * i),
                y_offset_range=config.pipe_y_offset_range,
                y_spacing=config.pipe_y_spacing,
            ) for i in range(math.floor(config.win_size[0] / config.pipe_x_spacing) + 1)
        ]

        player_center_x = state.player.pos.x - (34 * 1.5)
        state.distance = config.win_size[0] - (player_center_x +
            image_size(state.pipes[0].frames.frame_list[0])[0])
        state.distance += state.pipes[0]._size_x

    def amount_to_fill_container(container_size, object_size):
        """Calculates the minimum amount of objects (size `object_size`) needed
        to fill the container (size `container_size`).
        
        The returned amount might not fit inside the container - in this case,
        it will be one more than what would fit.
        """
        calculation = container_size / object_size
        if calculation % 1 > 0:
            calculation += (1 - calculation % 1)
        return int(calculation)

    def make_tiles():
        floor_resource = cache.get_resource("floor")
        clouds_resource = cache.get_resource("bg_clouds")
        bush_resource = cache.get_resource("bg_bush")
        city_resource = cache.get_resource("bg_city")

        floor_size_x = image_size(floor_resource)[0]
        # for now the size of clouds, bush and city are the same.
        bg_size_x, bg_size_y = image_size(clouds_resource)

        floor_amount = amount_to_fill_container(config.win_size[0], floor_size_x)
        bg_amount = amount_to_fill_container(config.win_size[0], bg_size_x)

        front_tiles = []
        back_tiles = []

        def move_bg(parallax_coeff, resource, back_tiles):
            back_tiles += [
            ScrollingTile(
                pos=(i * bg_size_x, config.ground_line - bg_size_y),
                wrap_pos=(bg_amount * bg_size_x),
                speed=(-config.scroll_speed * parallax_coeff),
                resource=resource,
            ) for i in range(bg_amount + 1)
            ]

        # floors
        front_tiles += [
            ScrollingTile(
                pos=(i * floor_size_x, config.ground_line),
                wrap_pos=(floor_amount * floor_size_x),
                speed=(-config.scroll_speed * config.floor_parallax_coeff),
                resource=floor_resource,
            ) for i in range(floor_amount + 1)
        ]
        # clouds
        move_bg(config.clouds_parallax_coeff, clouds_resource, back_tiles)
        # city
        move_bg(config.city_parallax_coeff, city_resource, back_tiles)
        # bushes
        move_bg(config.bush_parallax_coeff, bush_resource, back_tiles)

        return (front_tiles, back_tiles)

    cache = GameCache(config)

    font = SpriteFont(
        font_dict=pairs_to_dict([(str(n), cache.get_resource(f"font_{n}")) for n in range(10)]),
    )
    font_manager = FontManager(
        pos=(0, 0),
        sprite_font=font,
        padding_px=5,
    )

    bird_f0_size = image_size(cache.get_resource("bird_f0"))
    BIRD_INITIAL_POS = (
        config.win_size[0] / 2 - bird_f0_size[0] / 2 - 50,
        config.win_size[1] / 2 - bird_f0_size[1] / 2,
    )
    restart_game = initialize_game # temp alias

    clock = pygame.time.Clock()
    state = get_state()
    was_debug_mode = state.debug_mode
    ih = state.input_handler
    manager = GameManager(
        title=f"({config.win_size[0]}x{config.win_size[1]}) {config.title}",
        win_size=config.win_size,
        icon=cache.get_resource("icon"),
    )

    r_menu = cache.get_resource("menu")
    r_flappy = cache.get_resource("flappy")
    r_game_over = cache.get_resource("game_over")
    r_over_menu = cache.get_resource("over_menu")
    r_play = cache.get_resource("play")
    r_scoreboard = cache.get_resource("scoreboard")

    initialize_game()

    while state.is_running:
        # force framerate
        clock.tick(config.framerate)

        # get keypresses
        ih.update_keys()
        
        if not state.is_paused:
            state.player.process_extra(state, config)

            # when pressing the up key
            if ih.keymap[pygame.K_UP].first:
                # start the game if it hasn't started yet
                if state.game_mode == GameMode.START:
                    state.game_mode = GameMode.PLAYING

                # jump
                if state.game_mode == GameMode.PLAYING:
                    pygame.mixer.Channel(0).play(wing_sound)
                    state.player.speed.y = -8
                    state.player.jump_counter = 0

        if not state.is_paused:
            if state.game_mode == GameMode.PLAYING:
                for pipe in state.pipes:
                    pipe.process()

                    # die if colliding with the pipe
                    if pipe.is_colliding(gameobject_hitbox(state.player)):
                        if not state.debug_mode:
                            state.game_mode = GameMode.DEAD
                            state.player.speed.y = config.jump_speed
                            break

                # update distance
                state.distance -= config.scroll_speed
                if state.distance <= 0:
                    state.distance += config.pipe_x_spacing
                    pygame.mixer.Channel(1).play(point_sound)
                    state.current_score += 1

            if state.game_mode != GameMode.DEAD:
                for tile in chain(state.front_tiles, state.back_tiles):
                    tile.process()

            # game initialization on first frame
            if state.game_timer == 0:
                initialize_game()

        # enable or disable debug mode
        # debug mode includes being able to see hitboxes and other small features.
        if ih.keymap[K_h].first:
            state.debug_mode = not state.debug_mode

        # |= is to `or` what += is to `+`
        # yeah, it's bitwise, but it doesn't matter here, does it?
        should_pause = (ih.keymap[K_ESCAPE].first
                        and state.game_mode != GameMode.DEAD)
        should_pause |= (
            gameobject_hitbox(state.pause_button).collidepoint(ih.mouse_pos)
            and state.game_mode != GameMode.DEAD
            and ih.keymap[BUTTON_LEFT].first
        )

        # pause the game
        # (can't pause if the game hasn't started, though)
        if should_pause and state.game_mode != GameMode.START:
            state.is_paused = not state.is_paused

        # change pause button sprite depending on whether the game is paused or not
        if state.is_paused:
            state.pause_button.frames.current_index = 1
        else:
            state.pause_button.frames.current_index = 0

        # restart after death
        if state.game_mode == GameMode.DEAD:
            if state.death_timer == 0:
                pygame.mixer.Channel(2).play(hit_sound)
                pygame.mixer.Channel(3).play(death_sound)
            elif (state.death_timer >= 70
                and (gameobject_hitbox(state.play_button).collidepoint(ih.mouse_pos)
                    and ih.keymap[BUTTON_LEFT].first)):
                restart_game()

        # fill screen with sky color
        manager.fill_screen(cache.blit_base_color)

        # render back tiles
        for obj in state.back_tiles:
            manager.render(obj)

        # render pipes
        for obj in state.pipes:
            manager.render(obj)

        # render the player
        manager.render(state.player)

        # render pipe hitboxes
        if state.debug_mode:
            for tb_pipe in state.pipes:
                for hitbox in tb_pipe.get_hitboxes():
                    manager.render_rect(
                        rect=hitbox,
                        line_color=config.hitbox_line_color,
                        line_size=config.hitbox_line_size,
                    )

        # render player hitboxes
        if state.debug_mode:
            manager.render_rect(
                rect=gameobject_hitbox(state.player),
                line_color=config.hitbox_line_color,
                line_size=config.hitbox_line_size,
            )

        # to know if the debug was used
        if state.game_mode == GameMode.PLAYING:
            state.debug_used = state.debug_used or state.debug_mode

        # render front tiles
        for obj in state.front_tiles:
            manager.render(obj)

        # render ground hitbox
        if state.debug_mode:
            manager.render_rect(
                rect=(0, config.ground_line, *config.win_size),
                line_color=config.hitbox_line_color,
                line_size=config.hitbox_line_size,
            )
            
        # show initial tip
        if state.game_mode == GameMode.START and not state.is_paused:
            manager.blit(cache.get_resource("ready"), (222, 20))
            manager.blit(cache.get_resource("starter_tip"), (450, 200))

        # show pause button
        if state.game_mode == GameMode.PLAYING:
            manager.render(state.pause_button)

        # show score text on the top-left corner
        if (config.score_text_enabled
            and True
            and state.game_mode == GameMode.PLAYING
            and (state.game_timer % 60 == 0
                 or state.previous_score < state.current_score
                 or was_debug_mode != state.debug_mode
                 or state.score_text_rendered is None)):
            state.debug_text = "{}Score: {}".format(
                "[DEBUG] FPS: {} | MaxScore: {} ".format(
                    int(clock.get_fps()),
                    data["max_score"],
                ) if state.debug_mode else "",
                state.current_score,
            )
            state.score_text_rendered = cache.score_text_font.render(
                state.debug_text,
                True,
                cache.score_text_font_color
            )

        if config.score_text_enabled and state.game_mode == GameMode.PLAYING:
            manager.blit(state.score_text_rendered, config.score_text_pos)

        font_manager.update_string("50030")
        manager.render(font_manager)

        # pause menu
        if state.is_paused:
            manager.blit(r_menu, (258, 155))
            manager.blit(r_flappy, (222, 20))

        # game over
        if state.game_mode == GameMode.DEAD:
            state.player.animation_timer = 0
            if (state.death_timer == 0
            and state.current_score > data['max_score']
            and not state.debug_used):
                data['max_score'] = state.current_score
            state.death_timer += 1
            if state.death_timer >= 70: # wait some time for showing the death screen
                manager.blit(r_game_over, (222, 20))
                manager.blit(r_over_menu, (258, 145))
                manager.blit(r_play, (280, 405))
                manager.blit(r_scoreboard, (520, 405))

        # update screen
        pygame.display.update()

        for event in pygame.event.get():
            # exit via the QUIT event (window manager-specific)
            if event.type == QUIT:
                state.is_running = False

        # add 1 to the game timer
        state.game_timer += 1
