from .object import Object
import pygame
import random
import math

class Coin(Object):
    """
    A class representing a coin object in the game.
    
    Attributes:
        x (int): The x-coordinate of the coin.
        y (int): The y-coordinate of the coin.
        name (str): The name of the coin object.
        object_type (str): The type of the object, which is 'coin'.
        size (tuple): The size of the coin object, specified as (width, height).
        images (list): A list of images used for animation.
        dropped (bool): A flag indicating whether the coin is dropped on the map.
        bounce: An instance of the Bounce class for handling bouncing behavior.
        animation_frame (float): The current frame of the coin's animation.
        value (int): The value of the coin.
    """

    x = None
    y = None
    name = 'coin'
    object_type = 'coin'
    size = (16, 16)

    def __init__(self, game, room=None):
        """
        Initialize the Coin object.
        
        Args:
            game: The game instance.
            room: The room in which the coin is located.
        """
        self.images = []
        Object.__init__(self, game, self.name, self.object_type, self.size, room)
        self.dropped = False
        self.bounce = None
        self.animation_frame = 0
        self.value = 1

    def activate_bounce(self):
        """
        Activate bouncing behavior for the coin when on the map.
        """
        self.bounce = Bounce(self.rect.x, self.rect.y, self.rect.y + random.randint(0, 123), self.size)

    def load_image(self):
        """
        Load the image of the coin object.
        """
        for i in range(4):
            image = pygame.image.load(f'./assets/objects/coin/{self.name}/{self.name}{i}.png').convert_alpha()
            image = pygame.transform.scale(image, self.size)
            self.images.append(image)
        self.image = self.images[0]

    def update_animation_frame(self):
        """
        Update the animation frame of the coin.
        """
        self.animation_frame += (1.5 + (random.randint(1, 5) / 10)) / 15
        if self.animation_frame > 3:
            self.animation_frame = 0
        self.image = self.images[int(self.animation_frame)]

    def update(self):
        """
        Update the state of the coin object.
        """
        self.update_animation_frame()
        self.update_bounce()
        self.magnet()
        self.update_hitbox()
        self.rect.y += 0.1

    def detect_collision(self):
        """
        Detect collision between the player and the coin.
        """
        if self.game.player.hitbox.colliderect(self.rect):
            self.game.player.gold += self.value
            self.game.world_manager.current_room.objects.remove(self)

    def magnet(self):
        """
        Implement magnet behavior for the coin towards the player.
        """
        dir_vector = pygame.math.Vector2(self.game.player.hitbox.center[0] - self.rect.x,
                                         self.game.player.hitbox.center[1] - self.rect.y)
        if 0 < dir_vector.length() < 200:
            speed = 1 / dir_vector.length() * 250
            dir_vector.normalize_ip()
            dir_vector.scale_to_length(speed)
            if dir_vector[0] < 1:
                dir_vector[0] = math.ceil(dir_vector[0])
            if dir_vector[1] < 1:
                dir_vector[1] = math.ceil(dir_vector[1])
            self.rect.move_ip(*dir_vector)

    def draw(self):
        """
        Draw the coin object on the screen.
        """
        self.room.tile_map.map_surface.blit(self.image, self.rect)

class Emerald(Coin):
    """
    A class representing an emerald coin object in the game.
    Inherits from Coin class.
    """

    name = 'emerald'
    object_type = 'coin'
    size = (24, 24)

    def __init__(self, game, room=None):
        """
        Initialize the Emerald coin object.
        
        Args:
            game: The game instance.
            room: The room in which the coin is located.
        """
        super().__init__(game, room)
        self.value = 5



class Ruby(Coin):
    """
    Represents a special type of coin called Ruby.

    Attributes:
        name (str): The name of the coin.
        object_type (str): The type of object.
        size (tuple): The size of the coin.
    """

    name = 'ruby'
    object_type = 'coin'
    size = (24, 24)

    def __init__(self, game, room=None):
        """
        Initializes a Ruby coin object.

        Args:
            game (Game): The game instance.
            room (Room, optional): The room where the coin is located. Defaults to None.
        """
        super().__init__(game, room)
        self.value = 15


class Bounce:
    """
    Represents the bouncing behavior of objects.

    Attributes:
        speed (float): The initial speed of the bouncing object.
        angle (float): The initial angle of the bouncing object.
        drag (float): The drag coefficient affecting the bouncing object's speed.
        elasticity (float): The elasticity coefficient affecting the bouncing object's bounciness.
        gravity (tuple): The gravity vector affecting the bouncing object's movement.
        limit (float): The limit of the bouncing object's bounce height.
        x (float): The x-coordinate of the bouncing object's position.
        y (float): The y-coordinate of the bouncing object's position.
        size (tuple): The size of the bouncing object.
    """

    def __init__(self, x, y, limit, size):
        """
        Initializes a Bounce object.

        Args:
            x (float): The initial x-coordinate of the object.
            y (float): The initial y-coordinate of the object.
            limit (float): The limit of the object's bounce height.
            size (tuple): The size of the object.
        """
        self.speed = random.uniform(0.5, 0.6)
        self.angle = random.randint(-10, 10) / 10
        self.drag = 0.999
        self.elasticity = random.uniform(0.75, 0.9)
        self.gravity = (math.pi, 0.002)
        self.limit = limit
        self.limits = [limit, 654]
        self.x, self.y = x, y
        self.size = size

    def move(self):
        """
        Update the position of the bouncing object based on its speed and angle.
        """
        self.angle, self.speed = self.add_vectors(self.angle, self.speed, *self.gravity)
        self.x += math.sin(self.angle) * self.speed
        self.y -= math.cos(self.angle) * self.speed
        self.speed *= self.drag

    def bounce(self):
        """
        Simulate the bouncing behavior of the object.
        """
        if self.y > self.limit:
            self.y = 2 * self.limit - self.y
            self.angle = math.pi - self.angle
            self.speed *= self.elasticity

        elif self.y > 654 - self.size[0]:
            self.y = 2 * (654 - self.size[0]) - self.y
            self.angle = math.pi - self.angle
            self.speed *= self.elasticity

        if self.x < 198 + 10:
            self.x = 2 * (198 + 10) - self.x
            self.angle = - self.angle
            self.speed *= self.elasticity

        elif self.x > 1136 - self.size[0]:
            self.x = 2 * (1136 - self.size[0]) - self.x
            self.angle = - self.angle
            self.speed *= self.elasticity

    def reset(self):
        """
        Reset the properties of the bouncing object to their initial values.
        """
        self.speed = 0.5
        self.angle = random.choice([10, -10])
        self.drag = 0.999
        self.elasticity = 0.75

