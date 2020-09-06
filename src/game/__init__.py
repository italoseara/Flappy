import pygame
from pygame.locals import *

from random import randint
from pathlib import Path
from dataclasses import dataclass

from core.input import InputHandler, BUTTON_LEFT, BUTTON_MIDDLE, BUTTON_RIGHT
from core.entity import Entity
from core.manager import GameManager
from core.data import *
from core.maths import *

from .config import GameConfig
from .cache import GameCache
from .objects import ScrollingTile, Player, Pipe

@dataclass
class GameState:
    """Agrupa valores alteráveis durante o jogo."""
    player: 'typing.Any'
    backgrounds: 'typing.Any'
    floors: 'typing.Any'
    pause_button: 'typing.Any'
    scoreboard_button: 'typing.Any'
    play_button: 'typing.Any'
    pipes: 'typing.Any'
    input_handler: 'typing.Any'
    debug_mode: 'typing.Any'

    game_timer: int = 0
    pipe_spawn_counter: int = 0
    death_timer: int = 0

    current_score: int = 0
    # max_score: int = 0 # TODO

    game_state: int = 0 # TODO: turn this into an enum
    is_running: bool = True
    is_paused: bool = False

def main():
    config = GameConfig(
        resources_dir=(Path(__file__) / "../../res").resolve().absolute(),
        resources_to_load=[
            ("icon", "icon.bmp"),
            ("floor", "floor.png"),
            ("bg", "background.png"),
            ("bird_f0", "bird_f0.png"),
            ("bird_f1", "bird_f1.png"),
            ("bird_f2", "bird_f2.png"),
            ("pipe_top", "pipe_top.png"),
            ("pipe_bot", "pipe_bot.png"),
            ("starter_tip", "starter_tip.png"),
            ("game_over", "game_over.png"),
            ("pause_normal", "pause_normal.png"),
            ("paused", "paused.png"),
            ("menu", "menu.png"),
            ("over_menu", "over_menu.png"),
            ("play", "play.png"),
            ("scoreboard", "scoreboard.png"),
            ("flappy", "flappy.png"),
            ("ready", "ready.png")
        ],

        title="A strange flappy bird clone",
        debug_mode=False,

        win_size = (960, 540),
        blit_base_color = (115, 200, 215),

        scroll_speed=3,
        jump_speed=-8.0,
        gravity=0.5,
        framerate=60,

        score_text_font_name="Cascadia Code, Consolas, Tahoma",
        score_text_font_size=20,
        score_text_font_color="white",
        score_text_enabled=True,
        score_text_pos=(15, 10),

        hitbox_line_size=2, # OLD: hitbox_width
        hitbox_line_color=(0, 255, 0),

        bg_parallax_coeff=0.5, # OLD: bg_parallax
        floor_parallax_coeff=1.0, # OLD: floor_parallax
        pipe_height_interval=(-210, -40),
        pipe_y_spacing=130,

        ground_pos=476,
    )

    def get_state():
        pause_button_size = image_size(cache.get_resource("pause_normal"))
        scoreboard_button_size = image_size(cache.get_resource("scoreboard"))
        play_button_size = image_size(cache.get_resource("play"))

        floors, backgrounds = make_tiles()
        pipes = []

        pause_button = Entity(
            (config.win_size[0] - pause_button_size[0] - 10, 10),
            [cache.get_resource("pause_normal"), cache.get_resource("paused")],
        )

        scoreboard_button = Entity(
            (config.win_size[0] - scoreboard_button_size[0] - 280, 405),
            [cache.get_resource("scoreboard")],
        )

        play_button = Entity(
            (config.win_size[0] - play_button_size[0] - 520, 405),
            [cache.get_resource("play")],
        )

        player_frames = [cache.get_resource(f"bird_f{x}") for x in range(3)]
        player = Player(BIRD_INITIAL_POS, player_frames)

        return GameState(
            player=player,
            pipes=pipes,
            floors=floors,
            backgrounds=backgrounds,
            pause_button=pause_button,
            scoreboard_button=scoreboard_button,
            play_button=play_button,
            input_handler=InputHandler(),
            debug_mode=config.debug_mode,
        )

    def initialize_game():
        state.game_timer = 0
        state.game_state = 0
        state.death_timer = 0
        state.current_score = 0

        state.pipe_spawn_delay = 200 / config.scroll_speed
        state.pipe_spawn_counter = state.pipe_spawn_delay

        state.player.reset()
        state.player.angle_target = state.player.angle = 0
        state.player.animation_id = state.player.animation_timer = state.player.animation_timer_limit = 0
        state.player.speed.y = 0
        state.player.pos.x, state.player.pos.y = BIRD_INITIAL_POS

        state.pipes.clear()
        state.floors, state.backgrounds = make_tiles()

    def make_tiles():
        floor_resource = cache.get_resource("floor")
        floor_size_x = image_size(floor_resource)[0]
        bg_resource = cache.get_resource("bg")
        bg_size_x = image_size(bg_resource)[0]

        floors = [
            ScrollingTile(
                pos=(x, config.ground_pos),
                resource=floor_resource,
                parallax_coeff=config.floor_parallax_coeff,
            ) for x in [0, floor_size_x]
        ]
        backgrounds = [
            ScrollingTile(
                pos=(x, 0),
                resource=bg_resource,
                parallax_coeff=config.bg_parallax_coeff,
            ) for x in [0, bg_size_x]
        ]
        return (floors, backgrounds)


    cache = GameCache(config)

    bird_f0_size = image_size(cache.get_resource("bird_f0"))
    BIRD_INITIAL_POS = (
        config.win_size[0] / 2 - bird_f0_size[0] / 2 - 50,
        config.win_size[1] / 2 - bird_f0_size[1] / 2,
    )
    restart_game = initialize_game # temp alias

    clock = pygame.time.Clock()
    state = get_state()
    ih = state.input_handler
    manager = GameManager(
        title=f"({config.win_size[0]}x{config.win_size[1]}) {config.title}",
        win_size=config.win_size,
        icon=cache.get_resource("icon"),
    )

    initialize_game()

    while state.is_running:
        # force framerate
        clock.tick(config.framerate)

        # get keypresses
        ih.update_keys()
        
        if not state.is_paused:
            state.player.process(state, config)

        if not state.is_paused:
            if state.game_state == 1:
                state.pipe_spawn_counter -= 1

                for (i, pipe) in enumerate(state.pipes):
                    pipe.process()
                    pipe_hitbox = gameobject_hitbox(pipe)

                    # get points when going through a pipe
                    # part of the code is in the pipe class.
                    if (not pipe.has_scored) and (state.player.pos.x >= pipe.pos.x + pipe_hitbox[3]):
                        state.current_score += 1
                        pipe.has_scored = True

                    # die if colliding with the pipe
                    if pipe_hitbox.colliderect(gameobject_hitbox(state.player)):
                        state.game_state = 2
                        state.player.speed.y = config.jump_speed
                        break

                    # delete the pipe if it goes offscreen (via left)
                    if pipe.pos.x < 0 - gameobject_size(pipe)[0]:
                        del state.pipes[i]

                # spawn two pipes (above and below) when the counter goes to zero
                # FIXME: this seems to be slow. Maybe simply moving the pipes to the right of the screen could work?
                if state.pipe_spawn_counter <= 0:
                    top_y = randint(*config.pipe_height_interval)
                    bot_y = top_y + image_size(cache.get_resource("pipe_top"))[1] + config.pipe_y_spacing

                    top_pipe = Pipe(
                        (config.win_size[0], top_y),
                        [cache.get_resource("pipe_top")],
                        -config.scroll_speed
                    )
                    bot_pipe = Pipe(
                        (config.win_size[0], bot_y),
                        [cache.get_resource("pipe_bot")],
                        -config.scroll_speed
                    )

                    state.pipes += [top_pipe, bot_pipe]
                    state.pipe_spawn_counter = state.pipe_spawn_delay

            # move tiles, I guess?
            # place this before the game initialization or the game will start with things already
            # moving a little.
            if state.game_state in {0, 1}:
                for tile in (state.floors + state.backgrounds):
                    # Atualizar a posição com base na velocidade
                    tile.pos.x -= config.scroll_speed * tile.parallax_coeff
                    # Mover o tile para a direita se ele saiu completamente da tela.
                    if tile.pos.x < 0 - gameobject_size(tile)[0]:
                        tile.pos.x = config.win_size[0]

            # game initialization on first frame
            if state.game_timer == 0:
                initialize_game()

        # enable or disable debug mode
        # debug mode includes being able to see hitboxes and other small features.
        if ih.keymap[K_h].first:
            state.debug_mode = not state.debug_mode

        # pause the game
        should_pause = ((ih.keymap[K_ESCAPE].first # on keypress
                         and state.game_state != 2)
                        or (gameobject_hitbox(state.pause_button).collidepoint(ih.mouse_pos) # on mouse click
                            and state.game_state != 2
                            and ih.keymap[BUTTON_LEFT].first))
        if should_pause and state.game_state != 0: # can't pause if the game hasn't started
            state.is_paused = not state.is_paused

        # change pause button sprite depending on whether the game is paused or not
        if state.is_paused:
            state.pause_button.frames.current_index = 1
        else:
            state.pause_button.frames.current_index = 0

        # restart after death
        # TODO: add keypress for this
        if (gameobject_hitbox(state.play_button).collidepoint(ih.mouse_pos)
            and state.game_state == 2
            and ih.keymap[BUTTON_LEFT].first):
            restart_game()

        # fill screen with sky color
        manager.fill_screen(cache.blit_base_color)

        # render background and pipes
        for obj in state.backgrounds + state.pipes:
            manager.render(obj)

        # render the player
        manager.render(state.player)

        # render pipe hitboxes
        if state.debug_mode:
            for pipe in state.pipes:
                pygame.draw.rect(state.screen, config.hitbox_color, gameobject_hitbox(pipe), config.HITBOX_WIDTH)
        
        # render player hitboxes
        if state.debug_mode:
            pygame.draw.rect(state.screen, config.player_hitbox_color, gameobject_hitbox(state.player), config.HITBOX_WIDTH)

        # render the ground
        for obj in state.floors:
            manager.render(obj)

        # render ground hitbox
        if state.debug_mode:
            pygame.draw.rect(state.screen, config.hitbox_color, (0, config.GROUND_POS, *config.win_size), config.HITBOX_WIDTH)
            
        # show initial tip
        if state.game_state == 0 and not state.is_paused:
            manager.blit(cache.get_resource("ready"), (222, 20))
            manager.blit(cache.get_resource("starter_tip"), (450, 200))

        # show pause button
        if state.game_state == 1:
            manager.render(state.pause_button)

        # show score text on the top-left corner
        if config.score_text_enabled and state.game_state == 1 or state.debug_mode:
            debug_text = "{debug_flag}Score: {score}".format(
                    debug_flag=f"[DEBUG] FPS: {int(state.clock.get_fps())} | " if state.debug_mode else "",
                    score=int(state.current_score),
            )
            fps_text = cache.score_text_font.render(debug_text, True, cache.score_text_font_color)
            manager.blit(fps_text, config.score_text_pos)

        # pause menu
        if state.is_paused:
            manager.blit(cache.get_resource("menu"), (258, 155))
            manager.blit(cache.get_resource("flappy"), (222, 20))

        # game over
        if state.game_state == 2:
            state.player.animation_timer = 0
            state.death_timer += 1
            if state.death_timer >= 70: # wait some time for showing the death screen
                manager.blit(cache.get_resource("game_over"), (222, 20))
                manager.blit(cache.get_resource("over_menu"), (258, 145))
                manager.blit(cache.get_resource("play"), (280, 405))
                manager.blit(cache.get_resource("scoreboard"), (520, 405))

        # update screen
        pygame.display.update()

        for event in pygame.event.get():
            # exit via the QUIT event (window manager-specific)
            if event.type == QUIT:
                state.is_running = False

        # add 1 to the game timer
        state.game_timer += 1
