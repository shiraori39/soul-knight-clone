from .object import Object
from pygame import Vector2
import math
import random

class Flask(Object):
    """
    Base class for health potion inherited from object class.

    Attributes:
        name (str): The name of the flask.
        type (str): The type of the flask.
        size (tuple): The size of the flask.
    """

    name = 'flask'
    type = 'flask'
    size = (48, 48)

    def __init__(self, game, room, position=None):
        """
        Initializes a Flask object.

        Args:
            game (Game): The game instance.
            room (Room): The room where the flask is located.
            position (tuple, optional): The position of the flask. Defaults to None.
        """
        Object.__init__(self, game, self.name, self.type, self.size, room, position)
        self.dropped = False
        self.bounce = None

    def activate_bounce(self):
        """
        Activate bouncing behavior when the flask is dropped.
        """
        self.bounce = Bounce(self.rect.x, self.rect.y, self.rect.y + 20)

    def interact(self):
        """
        Interact with the flask (pick up).
        """
        self.interaction = False
        self.show_name.reset_line_length()
        self.image = self.original_image
        self.apply_effect()

    def draw(self):
        """
        Draw the flask on the game surface.
        """
        surface = self.room.tile_map.map_surface
        surface.blit(self.image, (self.rect.x, self.rect.y))
        if self.interaction:
            self.show_name.draw(surface, self.rect)
        self.show_price.draw(surface)
        self.show_price.update()

    def apply_effect(self):
        """
        Apply the effect of the flask.
        """
        pass

    def update(self):
        """
        Update the flask's position and behavior.
        """
        self.hovering.hovering()
        self.update_bounce()
        self.update_hitbox()
        if self in self.game.player.items:
            self.bounce.reset()
            self.rect.bottomright = self.game.player.hitbox.topleft

class GreenFlask(Flask):
    """
    A green health potion heals for 20hp.
    """

    name = 'green_flask'
    type = 'flask'
    size = (48, 48)

    def __init__(self, game, room, position=None):
        """
        Initializes a GreenFlask object.

        Args:
            game (Game): The game instance.
            room (Room): The room where the flask is located.
            position (tuple, optional): The position of the flask. Defaults to None.
        """
        Object.__init__(self, game, self.name, self.type, self.size, room, position)
        self.dropped = False
        self.bounce = None
        self.value = 100

    def apply_effect(self):
        """
        Apply the healing effect to the player.
        """
        if self.game.player.hp <= self.game.player.max_hp - 20:
            self.game.player.hp += 20
        else:
            self.game.player.hp = self.game.player.max_hp
        if self.room == self.game.world_manager.current_room:
            self.room.objects.remove(self)

class RedFlask(Flask):
    """
    A red health potion heals for 20hp and adds 20 max hp.
    """

    name = 'red_flask'
    type = 'flask'
    size = (48, 48)

    def __init__(self, game, room, position=None):
        """
        Initializes a RedFlask object.

        Args:
            game (Game): The game instance.
            room (Room): The room where the flask is located.
            position (tuple, optional): The position of the flask. Defaults to None.
        """
        Object.__init__(self, game, self.name, self.type, self.size, room, position)
        self.dropped = False
        self.bounce = None
        self.value = 400

    def apply_effect(self):
        """
        Apply the healing and max hp increase effect to the player.
        """
        self.game.player.hp += 20
        self.game.player.max_hp += 20
        if self.room == self.game.world_manager.current_room:
            self.room.objects.remove(self)

class Bounce:
    """
    Class to handle the bouncing behavior of objects.

    Attributes:
        speed (float): The initial speed of the object.
        angle (float): The initial angle of movement in radians.
        drag (float): The drag coefficient affecting speed decay over time.
        elasticity (float): The elasticity coefficient affecting the bounce.
        gravity (tuple): The gravitational force acting on the object represented as (angle, strength).
        limit (float): The maximum height to which the object can bounce.
        x (float): The x-coordinate of the object's position.
        y (float): The y-coordinate of the object's position.
    """

    def __init__(self, x, y, limit):
        """
        Initializes a Bounce object.

        Args:
            x (float): The x-coordinate of the object.
            y (float): The y-coordinate of the object.
            limit (float): The limit of the object's bounce height.
        """
        self.speed = random.uniform(0.5, 0.7)
        self.angle = random.randint(-5, 5) / 10
        self.drag = 0.999
        self.elasticity = random.uniform(0.75, 0.9)
        self.gravity = (math.pi, 0.002)
        self.limit = limit
        self.x, self.y = x, y

    @staticmethod
    def add_vectors(angle1, length1, angle2, length2):
        """
        Adds two vectors together.

        Args:
            angle1 (float): The angle of the first vector in radians.
            length1 (float): The length of the first vector.
            angle2 (float): The angle of the second vector in radians.
            length2 (float): The length of the second vector.

        Returns:
            tuple: A tuple containing the resulting angle and length.
        """
        x = math.sin(angle1) * length1 + math.sin(angle2) * length2
        y = math.cos(angle1) * length1 + math.cos(angle2) * length2
        angle = 0.5 * math.pi - math.atan2(y, x)
        length = math.hypot(x, y)
        return angle, length

    def move(self):
        """
        Move the object based on its angle and speed.
        """
        self.angle, self.speed = self.add_vectors(self.angle, self.speed, *self.gravity)
        self.x += math.sin(self.angle) * self.speed
        self.y -= math.cos(self.angle) * self.speed
        self.speed *= self.drag

    def bounce(self):
        """
        Make the object bounce when it reaches the limit.
        """
        if self.y > self.limit:
            self.y = 2 * (self.limit) - self.y
            self.angle = math.pi - self.angle
            self.speed *= self.elasticity

    def reset(self):
        """
        Reset the object's bounce parameters.
        """
        self.speed = 0.5
        self.angle = random.choice([10, -10])
        self.drag = 0.999
        self.elasticity = 0.75
