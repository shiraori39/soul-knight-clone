import pygame
import time

from .menu import MainMenu
from .game_over import GameOver
from .hud import Hud
from .mini_map import MiniMap
from .entities.player import Player
from .objects.object_manager import ObjectManager
from .entities.enemy_manager import EnemyManager
from .map.world_manager import WorldManager
from .objects.object_manager import ObjectManager
from .bullet import BulletManager
pygame.init()
pygame.mixer.init()

world_size = (1280, 720)

class Game:
    """
    A class to represent the main game.

    Attributes
    ----------
    display : pygame.Surface
        The main display surface.
    screen : pygame.Surface
        The game screen surface.
    clock : pygame.time.Clock
        The game clock for managing frame rate.
    enemy_manager : EnemyManager
        Manages enemy entities.
    world_manager : WorldManager
        Manages the game world.
    object_manager : ObjectManager
        Manages game objects.
    bullet_manager : BulletManager
        Manages bullets in the game.
    player : Player
        The player entity.
    hud : Hud
        The heads-up display for the game.
    running : bool
        Indicates if the game loop is running.
    menu : MainMenu
        The main menu of the game.
    mini_map : MiniMap
        The mini-map display.
    game_time : int or None
        The game time in milliseconds.
    fps : int
        Frames per second setting.
    game_over : GameOver
        The game over screen.
    dt : float
        Delta time between frames.
    screen_position : tuple
        The position of the screen.

    Methods
    -------
    refresh():
        Resets and restarts the game.
    update_groups():
        Updates all game entities and objects.
    draw_groups():
        Draws all game entities and objects to the screen.
    input():
        Handles player input and events.
    run_game():
        Runs the main game loop.
    """
    def __init__(self):
        """
        Initializes all the game components and settings.
        """
        self.display = pygame.display.set_mode(world_size)
        self.screen = pygame.Surface(world_size).convert()
        self.clock = pygame.time.Clock()
        self.enemy_manager = EnemyManager(self)
        self.world_manager = WorldManager(self)
        self.object_manager = ObjectManager(self)
        self.bullet_manager = BulletManager(self)
        self.player = Player(self)
        self.hud = Hud(self)
        self.running = True
        self.menu = MainMenu(self)
        self.mini_map = MiniMap(self)
        self.game_time = None
        self.fps = 60
        self.game_over = GameOver(self)
        pygame.mixer.init()
        self.dt = 0
        self.screen_position = (0, 0)

    def refresh(self):
        """
        Resets and restarts the game, refreshing the game state and display.
        """
        self.__init__()
        pygame.display.flip()
        self.run_game()
    def update_groups(self):
        """
        Updates all game entities and objects.
        """
        self.enemy_manager.update_enemies()
        self.object_manager.update()
        self.player.update()
        self.bullet_manager.update()
        self.world_manager.update()
        self.game_over.update()
        self.mini_map.update()

    def draw_groups(self):
        """
        Draws all game entities and objects to the screen.
        """
        self.world_manager.draw_map(self.screen)
        if self.player:
            self.player.draw(self.screen)
        self.enemy_manager.draw_enemies(self.screen)
        self.object_manager.draw()
        self.bullet_manager.draw()
        self.mini_map.draw(self.screen)
        self.hud.draw()
        self.game_over.draw()

    def input(self):
        """
        Handles player input and events.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.USEREVENT:
                self.object_manager.up += 1
                self.object_manager.hover = True

        self.player.input()
        pressed = pygame.key.get_pressed()
        # if pressed[pygame.K_r]:
        #     self.refresh()

        if pressed[pygame.K_ESCAPE]:
            if self.game_over.game_over:
                self.refresh()
            self.menu.running = True
            self.menu.play_button.clicked = False

    def run_game(self):
        """
        Runs the main game loop, updating and drawing the game each frame.
        """
        self.enemy_manager.add_enemies()
        prev_time = time.time()
        while self.running:
            self.clock.tick(self.fps)
            now = time.time()
            self.dt = now - prev_time
            prev_time = now
            self.menu.show()
            self.screen.fill((0, 0, 0))
            self.input()
            self.update_groups()
            self.draw_groups()
            self.game_time = pygame.time.get_ticks()
            self.display.blit(self.screen, self.screen_position)
            if self.running:
                pygame.display.flip()
        pygame.quit()
