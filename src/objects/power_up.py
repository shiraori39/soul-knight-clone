import pygame
from .object import Object
import random

class PowerUp(Object):
    """
    Class representing a power-up object.

    Attributes:
        type (str): The type of the power-up.
        size (tuple): The size of the power-up image.
        name (str): The name of the power-up.
        position (tuple): The position of the power-up.
        interaction (bool): Flag indicating whether the power-up is interactable.
        counter (int): Counter for tracking interactions.
        elevated (bool): Flag indicating whether the power-up is elevated.
        particles (list): List of particles associated with the power-up.
    """

    type = 'flask'
    size = (64, 64)

    def __init__(self, game, room, name, position=None):
        """
        Initializes a PowerUp object.

        Args:
            game (Game): The main game object.
            room (Room): The room containing the power-up.
            name (str): The name of the power-up.
            position (tuple, optional): The position of the power-up. Defaults to None.
        """
        self.name = name
        self.position = [644, 400]
        if position is not None:
            self.position = position
        Object.__init__(self, game, self.name, self.type, self.size, room, self.position)
        self.interaction = False
        self.counter = 0
        self.elevated = False
        self.particles = []

    def load_image(self):
        """Load the image for the power-up."""
        image = pygame.image.load(f'./assets/objects/power_ups/{self.name}/{self.name}.png').convert_alpha()
        image = pygame.transform.scale(image, self.size)
        self.image = image

    def detect_collision(self):
        """Detect collision with the player."""
        if self.game.player.rect.colliderect(self.rect):
            self.image = pygame.image.load(
                f'./assets/objects/power_ups/{self.name}/{self.name}_picked.png').convert_alpha()
            self.interaction = True
        else:
            self.image = pygame.image.load(
                f'./assets/objects/power_ups/{self.name}/{self.name}.png').convert_alpha()
            self.interaction = False
            self.show_name.reset_line_length()

    def interact(self):
        """Interact with the power-up."""
        pass

    def update(self):
        """Update the power-up."""
        self.hovering.hovering()
        self.show_price.update()
        self.update_hitbox()
        self.update_bounce()

    def draw(self):
        """Draw the power-up on the screen."""
        surface = self.room.tile_map.map_surface
        surface.blit(self.image, (self.rect.x, self.rect.y))
        self.beautify(surface)
        if self.interaction:
            self.show_name.draw(surface, self.rect)
        self.show_price.draw(surface)

    def beautify(self, surface):
        """Beautify the power-up."""
        pass


class AttackPowerUp(PowerUp):
    """
    Class representing an attack power-up.

    Attributes:
        name (str): The name of the power-up.
        value (int): The value associated with the power-up.
    """

    name = 'attack'

    def __init__(self, game, room, position=None):
        """
        Initializes an AttackPowerUp object.

        Args:
            game (Game): The main game object.
            room (Room): The room containing the power-up.
            position (tuple, optional): The position of the power-up. Defaults to None.
        """
        super().__init__(game, room, self.name, position)
        self.value = 250

    def interact(self):
        """Interact with the attack power-up."""
        self.game.player.strength *= 1.1
        self.room.objects.remove(self)

    def beautify(self, surface):
        """Beautify the attack power-up."""
        if random.randint(1, 20) == 1:
            x = random.randint(self.rect.midtop[0] - 30, self.rect.midtop[0] + 30)
            y = random.randint(self.rect.midtop[1] - 30, self.rect.midtop[1] + 30)


class ShieldPowerUp(PowerUp):
    """
    Class representing a shield power-up.

    Attributes:
        name (str): The name of the power-up.
        value (int): The value associated with the power-up.
    """

    name = 'armor'

    def __init__(self, game, room, position=None):
        """
        Initializes a ShieldPowerUp object.

        Args:
            game (Game): The main game object.
            room (Room): The room containing the power-up.
            position (tuple, optional): The position of the power-up. Defaults to None.
        """
        super().__init__(game, room, self.name, position)
        self.value = 150

    def interact(self):
        """Interact with the shield power-up."""
        self.game.player.shield += 1
        self.room.objects.remove(self)

    def beautify(self, surface):
        """Beautify the shield power-up."""
        if random.randint(1, 10) == 1:
            x = random.randint(self.hitbox.midtop[0] - 10, self.rect.midtop[0] + 10)
            y = random.randint(self.hitbox.midtop[1] - 10, self.rect.midtop[1] + 10)
