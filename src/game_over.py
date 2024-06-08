import pygame

import src.utils as utils


class GameOver:
    """
    A class to represent the game over screen.

    Attributes
    ----------
    game : Game
        The game instance.
    text : str
        The text to display on the game over screen.
    counter : int
        A counter to keep track of time.
    image_size : tuple
        The size of the game over image.
    image : pygame.Surface
        The image for the game over screen.
    rect : pygame.Rect
        The rectangle of the game over image.
    position : list
        The position of the game over image.
    hover_value : int
        The value by which the game over image moves up and down.
    game_over : bool
        Indicates whether the game over screen is displayed.
    played : bool
        Indicates whether the game over sound has been played.

    Methods
    -------
    input():
        Handles input events, such as quitting the game.
    update():
        Updates the game over screen, moving it into position and triggering hover effect.
    draw():
        Draws the game over screen on the game display.
    hover():
        Implements the hover effect for the game over screen.
    """
    def __init__(self, game):
        """
        Initializes the GameOver instance with the given game instance.

        Parameters
        ----------
        game : Game
            The game instance.
        """
        self.game = game
        self.text = 'GAME OVER'
        self.counter = 0
        self.image_size = (360, 360)
        self.image = pygame.transform.scale(pygame.image.load('./assets/misc/game_over.png'), self.image_size)
        self.rect = self.image.get_rect()
        self.rect.center = (utils.world_size[0] / 2, utils.world_size[1] / 2)
        self.position = [utils.world_size[0] / 2 - 180, - 800]
        self.hover_value = -5
        self.game_over = False
        self.played = False

    @staticmethod
    def input():
        """
        Handles input events, such as quitting the game.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

    def update(self):
        """
        Updates the game over screen, moving it into position and triggering hover effect.
        """
        if self.game.player.dead:
            self.input()
            self.counter += 1
            if self.position[1] <= self.rect.midtop[1]:
                self.position[1] += 15
            else:
                self.game_over = True
                self.hover()

    def draw(self):
        """
        Draws the game over screen on the game display.
        """
        if self.game.player.dead:
            self.game.screen.blit(self.image, self.position)
            # pygame.draw.rect(self.game.screen, (255, 255, 255), self.rect, 1)

    def hover(self):
        """
        Implements the hover effect for the game over screen.
        """
        if self.counter % 30 == 0:
            self.position[1] += self.hover_value
        if pygame.time.get_ticks() % 1000 < 500:
            self.hover_value = -5
        elif pygame.time.get_ticks() % 1000 > 500:
            self.hover_value = 5
