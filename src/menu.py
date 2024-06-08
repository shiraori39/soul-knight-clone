import pygame

class Button:
    """
    A class to represent a generic button in the game menu.

    Attributes
    ----------
    name : str
        The name of the button, used to load its images.
    menu : MainMenu
        The menu instance this button belongs to.
    images : list
        A list of images representing different button states.
    path : str
        The path to the button image assets.
    image : pygame.Surface
        The current image of the button.
    rect : pygame.Rect
        The rectangle representing the button's position and size.
    clicked : bool
        Indicates if the button has been clicked.
    played : bool
        Indicates if the hover sound has been played.

    Methods
    -------
    __init__(menu, x, y, name):
        Initializes the button with its position and name.
    load_images():
        Loads the button images.
    detect_action(pos):
        Placeholder for actions to perform when the button is clicked.
    update():
        Updates the button state based on mouse position and clicks.
    draw(surface):
        Draws the button on the given surface.
    """
    def __init__(self, menu, x, y, name):
        """
        Initializes the button with its position and name.

        Parameters
        ----------
        menu : MainMenu
            The menu instance this button belongs to.
        x : int
            The x-coordinate of the button's position.
        y : int
            The y-coordinate of the button's position.
        name : str
            The name of the button, used to load its images.
        """
        self.name = name
        self.menu = menu
        self.images = []
        self.path = './assets/misc/buttons'
        self.load_images()
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.midtop = (x, y)
        self.clicked = False
        self.played = False

    def load_images(self):
        """
        Loads the button images.
        """
        self.images.append(pygame.image.load(f'{self.path}/{self.name}1.png').convert_alpha())
        self.images.append(pygame.image.load(f'{self.path}/{self.name}2.png').convert_alpha())
    
    def detect_action(self, pos):
        """
        Placeholder for actions to perform when the button is clicked.

        Parameters
        ----------
        pos : tuple
            The current mouse position.
        """
        pass
    

    def update(self):
        """
        Updates the button state based on mouse position and clicks.
        """
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            self.image = self.images[1]
        else:
            self.image = self.images[0]
            self.played = False
        #check if clicked
        self.detect_action(pos)

    def draw(self, surface):
        """
        Draws the button on the given surface.

        Parameters
        ----------
        surface : pygame.Surface
            The surface to draw the button on.
        """
        surface.blit(self.image, self.rect)

class PlayButton(Button):
    """
    A class to represent the play button in the game menu.

    Methods
    -------
    __init__(menu, x, y):
        Initializes the play button with its position.
    detect_action(pos):
        Closes the menu and starts the game when the button is clicked.
    """
    def __init__(self, menu, x, y):
        """
        Initializes the play button with its position.

        Parameters
        ----------
        menu : MainMenu
            The menu instance this button belongs to.
        x : int
            The x-coordinate of the button's position.
        y : int
            The y-coordinate of the button's position.
        """
        super().__init__(menu, x, y, 'play')

    def detect_action(self, pos):
        """
        Closes the menu and starts the game when the button is clicked.

        Parameters
        ----------
        pos : tuple
            The current mouse position.
        """
        if self.rect.collidepoint(pos) and pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
            self.menu.running = False
            self.menu.game.running = True
            self.clicked = True

class ExitButton(Button):
    """
    A class to represent the exit button in the game menu.

    Methods
    -------
    __init__(menu, x, y):
        Initializes the exit button with its position.
    detect_action(pos):
        Exits the game when the button is clicked.
    """
    def __init__(self, menu, x, y):
        """
        Initializes the exit button with its position.

        Parameters
        ----------
        menu : MainMenu
            The menu instance this button belongs to.
        x : int
            The x-coordinate of the button's position.
        y : int
            The y-coordinate of the button's position.
        """
        super().__init__(menu, x, y, 'exit')

    def detect_action(self, pos):
        """
        Exits the game when the button is clicked.

        Parameters
        ----------
        pos : tuple
            The current mouse position.
        """
        if self.rect.collidepoint(pos) and pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
            self.menu.game.running = False
            self.menu.running = False
            self.clicked = True


class MainMenu:
    """
    A class to represent the main menu of the game.

    Attributes
    ----------
    game : Game
        The main game instance.
    running : bool
        Indicates if the menu loop is running.
    play_button : PlayButton
        The play button in the menu.
    exit_button : ExitButton
        The exit button in the menu.

    Methods
    -------
    __init__(game):
        Initializes the main menu with the given game instance.
    input():
        Handles input actions from the keyboard or mouse.
    update():
        Updates the state of the menu buttons.
    draw():
        Draws the menu and its buttons.
    show():
        Runs the main menu loop.
    """
    def __init__(self, game):
        """
        Initializes the main menu with the given game instance.

        Parameters
        ----------
        game : Game
            The main game instance.
        """
        self.game = game
        self.running = True
        self.play_button = PlayButton(self, 21 * 64 / 2, 8 * 64 / 2)
        self.exit_button = ExitButton(self, 21 * 64 / 2, 7 * 64 / 2 + 240)

    def input(self):
        """
        Handles input actions from the keyboard or mouse.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_ESCAPE]:
            self.game.running = False

    def update(self):
        """
        Checks if any buttons are pressed and updates their states.
        """
        self.play_button.update()
        self.exit_button.update()

    def draw(self):
        """
        Draws the menu and its buttons.
        """
        self.game.screen.fill((0, 0, 0))
        self.play_button.draw(self.game.screen)
        self.exit_button.draw(self.game.screen)

    def show(self):
        """
        Runs the main menu loop.
        """
        while self.running:
            self.input()
            self.update()
            self.draw()
            self.play_button.detect_action(pygame.mouse.get_pos())
            self.game.clock.tick(self.game.fps)
            self.game.display.blit(self.game.screen, (0, 0))
            pygame.display.flip()
