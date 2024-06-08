import numpy.random
import pygame
import random
from numpy.random import choice as np
import src.utils as utils
from src.objects.weapon import Katana
from .object import Object
from .flask import RedFlask, GreenFlask
from .power_up import AttackPowerUp, ShieldPowerUp
from .coin import Coin, Emerald, Ruby

class Chest(Object):
    """
    A class representing a chest object in the game.

    Attributes:
        name (str): The name of the chest object.
        object_type (str): The type of the object, which is 'chest'.
        size (tuple): The size of the chest object, specified as (width, height).
        image: The image of the chest object.
        rect: The rectangular area occupied by the chest object.
        hitbox: The hitbox area used for collision detection.
        animation_frame (float): The current frame of the chest's animation.
        open (bool): A flag indicating whether the chest is open or closed.
        items (list): A list of items contained within the chest.
        interaction (bool): A flag indicating whether the player is interacting with the chest.
        counter (int): A counter variable used for various purposes.
    """

    name = 'chest'
    object_type = 'chest'
    size = (64, 64)

    def __init__(self, game, room):
        """
        Initialize the Chest object.

        Args:
            game: The game instance.
            room: The room in which the chest is located.
        """
        self.image = None
        Object.__init__(self, game, self.name, self.object_type, self.size, room)
        self.rect = self.image.get_rect()
        self.rect.midbottom = (21 * 64 / 2, 7.25 * 64)
        self.hitbox = utils.get_mask_rect(self.image, *self.rect.topleft)
        self.animation_frame = 0
        self.open = False
        self.items = []
        self.add_treasure()
        self.interaction = False
        self.counter = 0

    def add_treasure(self):
        """
        Add random items to the chest's inventory.
        """
        items = [RedFlask(self.game, self.room),
                 ShieldPowerUp(self.game, self.room), AttackPowerUp(self.game, self.room),
                 GreenFlask(self.game, self.room), ]
        items = numpy.random.choice(items, size=3, replace=False, p=[0.1, 0.2, 0.2, 0.5])
        for it in items:
            self.items.append(it)
        for _ in range(random.randint(20, 30)):
            self.items.append(Coin(self.game, self.room))
        for _ in range(random.randint(2, 7)):
            self.items.append(Emerald(self.game, self.room))
        for _ in range(random.randint(2, 7)):
            self.items.append(Ruby(self.game, self.room))

    def load_image(self):
        """
        Load the image of the chest object.
        """
        image = pygame.image.load('./assets/objects/chest/full/chest_full0.png').convert_alpha()
        image = pygame.transform.scale(image, self.size)
        self.image = image

    def change_chest_state(self):
        """
        Change the state of the chest based on its animation frame.
        """
        if self.open and self.animation_frame <= 2:
            self.animation_frame += 1 / 20
            self.image = pygame.image.load(
                f'./assets/objects/chest/full/chest_full{int(self.animation_frame)}.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, utils.basic_entity_size)
        elif 2 < self.animation_frame <= 3:
            self.animation_frame += 1 / 20
        elif self.open:
            self.image = pygame.image.load(
                './assets/objects/chest/empty/chest_empty2.png'
            ).convert_alpha()
            self.image = pygame.transform.scale(self.image, utils.basic_entity_size)
            self.drop_items()  # at the last frame of animation, drop items

    def update(self):
        """
        Update the state of the chest object.
        """
        self.chest_collision()
        self.change_chest_state()

    def draw(self):
        """
        Draw the chest object on the screen.
        """
        self.room.tile_map.map_surface.blit(self.image, self.rect)

    def detect_collision(self):
        """
        Detect collision between the player and the chest.
        """
        if self.game.player.hitbox.colliderect(self.rect):
            self.image = pygame.image.load('./assets/objects/chest/full/chest_picked.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (64, 64))
            self.interaction = True
        else:
            self.image = pygame.image.load('./assets/objects/chest/full/chest_full0.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, utils.basic_entity_size)
            self.interaction = False

    def chest_collision(self):
        """
        Check collision between the player and the chest.
        """
        test_rect = self.game.player.hitbox.move(*self.game.player.velocity)
        collide_points = (test_rect.midbottom, test_rect.bottomleft, test_rect.bottomright)
        if any(self.hitbox.collidepoint(point) for point in collide_points):
            self.game.player.velocity = [0, 0]

    def interact(self):
        """
        Perform interaction with the chest.
        """
        self.open = True
        self.interaction = False

        # self.drop_items()

    def drop_items(self):
        """
        Drop items from the chest.
        """
        for item in self.items:
            item.rect.midtop = self.rect.topleft
            item.dropped = True
            item.activate_bounce()
            item.bounce.x = self.hitbox.midtop[0]
            item.bounce.y = self.hitbox.midtop[1]
            self.room.objects.append(item)
            self.items.remove(item)

    def __repr__(self):
        """
        Return a string representation of the chest object.
        """
        return f'Chest in room {self.room}'

