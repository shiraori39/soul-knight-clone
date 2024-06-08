import pygame
from src.utils import get_mask_rect
import src.utils as utils
import random
import math

class ShowName:
    """
    A class for displaying an animated name text above an object.

    Attributes:
        object: The object associated with the displayed name.
        line_length (int): The length of the line animation.
        time (int): The time the animation started.
        text (str): The formatted display name of the object.
        text_length (int): The length of the display name.
        text_position (tuple): The position of the text.
        counter (int): A counter for animation progress.

    Methods:
        time_passed(time, amount): Checks if a certain amount of time has passed.
        draw(surface, rect): Draws the animated name and line above the object.
        draw_text(surface): Draws the text portion of the name.
        draw_text_line(surface, rect): Draws the line decoration above the text.
        reset_line_length(): Resets the animation line length and counter.
    """
    def __init__(self, object):
        """
        Initializes a ShowName object.

        Args:
            object: The object associated with the displayed name.
        """
        self.object = object
        self.line_length = 0
        self.time = 0
        # Format weapon display name
        self.text = self.object.name.replace("_", " ").title()
        self.text_length = len(self.text)
        self.text_position = None
        self.counter = 0

    @staticmethod
    def time_passed(time, amount):
        """
        Checks if a certain amount of time has passed.

        Args:
            time (int): The starting time of the event.
            amount (int): The amount of time to wait.

        Returns:
            bool: True if the specified time has passed, False otherwise.
        """
        if pygame.time.get_ticks() - time > amount:
            return True

    def draw(self, surface, rect):
        """
        Draws the animated name and line above the object.

        Args:
            surface: The surface to draw on.
            rect: The rectangle representing the object's position.
        """
        self.draw_text_line(surface, rect)
        self.draw_text(surface)

    def draw_text(self, surface):
        """
        Draws the text portion of the name.

        Args:
            surface: The surface to draw on.
        """
        text_surface = pygame.font.Font(utils.font, 15).render(self.text[:self.counter], True, (255, 255, 255))
        surface.blit(text_surface, self.text_position)

    def draw_text_line(self, surface, rect):
        """
        Draws the line decoration above the text.

        Args:
            surface: The surface to draw on.
            rect: The rectangle representing the object's position.
        """
        starting_position = [rect.topleft[0], rect.topleft[1]]  # starting position of diagonal line
        for _ in range(5):  # we draw rectangles in diagonal line, so the line looks pixelated
            starting_position[0] -= 5
            starting_position[1] -= 5
            pygame.draw.rect(surface, (255, 255, 255), (starting_position[0], starting_position[1], 5, 5))

        starting_position[1] += 2  # adjustment of vertical position
        end_position = [starting_position[0] - self.line_length, starting_position[1]]
        pygame.draw.line(surface, (255, 255, 255), starting_position, end_position, 5)
        if self.line_length <= self.text_length * 8 and self.time_passed(self.time, 15):
            self.time = pygame.time.get_ticks()
            self.line_length += 8
            self.counter += 1
        self.text_position = (end_position[0], end_position[1] - 20)

    def reset_line_length(self):
        """Resets the animation line length and counter."""
        self.line_length = 0
        self.counter = 0

class ShowPrice(ShowName):
    """
    A class for displaying the price of an item.

    Inherits from ShowName.

    Attributes:
        object: The object associated with the displayed price.
        text (str): The formatted price of the object.
        text_length (int): The length of the price text.
        text_position (tuple): The position of the price text.
        counter (int): A counter for animation progress.
        image: The image of the coin animation.
        images (list): A list containing frames of the coin animation.
        image_size (tuple): The size of the coin animation frames.
        image_rect: The rectangle representing the position of the coin animation.
        animation_frame (int): The current frame of the coin animation.

    Methods:
        set_text_position(position): Sets the position of the price text.
        load_image(): Loads the coin animation frames from assets.
        update_animation_frame(): Updates the animation frame of the coin.
        update(): Updates the coin animation.
        draw_text(surface): Draws the price text on the surface.
        draw(surface): Draws the coin animation and price text on the surface.
    """
    def __init__(self, object):
        """
        Initializes a ShowPrice object.

        Args:
            object: The object associated with the displayed price.
        """
        super().__init__(object)
        # Format weapon display name
        self.text = str(self.object.value)
        self.text_length = len(self.text)
        self.text_position = None
        self.counter = 0
        self.image = None
        self.images = []
        self.image_size = (24, 24)
        self.load_image()
        self.image_rect = self.image.get_rect()
        self.text_position = (0, 0)
        self.animation_frame = 0

    def set_text_position(self, position):
        """
        Sets the position of the price text.

        Args:
            position (tuple): The position to set.
        """
        self.text_position = position
        self.image_rect = (position[0] - 25, position[1] - 8)

    def load_image(self):
        """Loads the coin animation frames from assets."""
        for i in range(4):
            image = pygame.image.load(f'./assets/objects/coin/coin/coin{i}.png').convert_alpha()
            image = pygame.transform.scale(image, self.image_size)
            self.images.append(image)
        self.image = self.images[0]

    def update_animation_frame(self):
        """Updates the animation frame of the coin."""
        self.animation_frame += 1.5 / 15  # random.randint(10, 20)/100
        if self.animation_frame > 3:
            self.animation_frame = 0
        self.image = self.images[int(self.animation_frame)]

    def update(self):
        """Updates the coin animation."""
        # self.image_rect.topleft = (self.object.hitbox.midbottom[0] - 15, self.object.hitbox.midbottom[1] + 10)
        # self.text_position = (self.image_rect.topleft[0] + 25, self.image_rect.topleft[1] + 8)
        self.update_animation_frame()

    def draw_text(self, surface):
        """
        Draws the price text on the surface.

        Args:
            surface: The surface to draw on.
        """
        text_surface = pygame.font.Font(utils.font, 18).render(self.text, True, (255, 255, 255))
        surface.blit(text_surface, self.text_position)

    def draw(self, surface):
        """
        Draws the coin animation and price text on the surface.

        Args:
            surface: The surface to draw on.
        """
        if self.object.for_sale:
            surface.blit(self.image, self.image_rect)
            self.draw_text(surface)


class Hovering:
    """
    A class to manage hovering behavior for objects.

    Attributes:
        game: The game instance.
        object: The object being hovered.
        hover_value (int): The value by which the object will move up or down.
        position (int): The position state of the object.

    Methods:
        set_hover_value(): Sets the hover value based on game conditions.
        hovering(): Moves the object up or down based on hover conditions.
    """
    def __init__(self, game, obj):
        """
        Initializes a Hovering object.

        Args:
            game: The game instance.
            obj: The object being hovered.
        """
        self.game = game
        self.object = obj
        self.hover_value = 0
        self.position = 1

    def set_hover_value(self):
        """Sets the hover value based on game conditions."""
        num = self.game.object_manager.up // 2
        if num % 2 == 0:
            self.hover_value = -5
        elif num % 2 == 1:
            self.hover_value = 5

    def hovering(self):
        """Moves the object up or down based on hover conditions."""
        if self.object.player is not None:
            return
        if self.object.game.object_manager.hover:
            self.object.rect.y += self.hover_value
        self.set_hover_value()

class Object:
    """
    Represents an object in the game.

    Attributes:
        game: The game instance.
        name (str): The name of the object.
        object_type (str): The type of the object.
        size (tuple): The size of the object.
        room: The room where the object is located.
        position (tuple): The position of the object.
        player: The player associated with the object.
        original_image: The original image of the object.
        image_picked: The image of the object when picked.
        hud_image: The image of the object for the heads-up display.
        image: The current image of the object.
        path: The path to the object's image assets.
        show_name: An instance of ShowName for displaying the object's name.
        value: The value of the object.
        show_price: An instance of ShowPrice for displaying the object's price.
        hovering: An instance of Hovering for managing hovering behavior.
        interaction (bool): Flag indicating if the object is being interacted with.
        dropped (bool): Flag indicating if the object has been dropped.
        for_sale (bool): Flag indicating if the object is for sale.
        bounce: An instance of Bounce for managing bouncing behavior.

    Methods:
        activate_bounce(): Activates bouncing behavior for the object.
        update_bounce(): Updates the bouncing behavior of the object.
        load_image(): Loads the image assets for the object.
        detect_collision(): Detects collision with the player for interaction.
        drop(): Drops the object from the player's inventory.
        update(): Updates the object's state.
        update_hitbox(): Updates the hitbox of the object.
        interact(): Performs interaction with the object.
        remove_object(): Removes the object from the room.
        buy(): Buys the object if the player has enough gold.
        draw(): Draws the object on the game surface.
    """
    def __init__(self, game, name, object_type, size=None, room=None, position=None, player=None):
        """
        Initializes an Object instance.

        Args:
            game: The game instance.
            name (str): The name of the object.
            object_type (str): The type of the object.
            size (tuple, optional): The size of the object.
            room: The room where the object is located.
            position (tuple, optional): The position of the object.
            player: The player associated with the object.
        """
        self.game = game
        self.room = room
        self.name = name
        self.object_type = object_type
        self.size = size
        self.player = player
        self.original_image = None
        self.image_picked = None
        self.hud_image = None
        self.image = None
        self.path = f'./assets/objects/{self.name}'
        self.load_image()
        self.rect = self.image.get_rect()
        self.hitbox = get_mask_rect(self.image, *self.rect.topleft)
        if position:
            self.rect.x, self.rect.y = position[0], position[1]
        self.show_name = ShowName(self)
        self.value = None
        self.show_price = ShowPrice(self)
        self.hovering = Hovering(self.game, self)
        self.interaction = False
        self.dropped = False
        self.for_sale = False
        self.bounce = None

    def __repr__(self):
        """Returns a string representation of the object."""
        return self.name

    def activate_bounce(self):
        """Activates bouncing behavior for the object."""
        self.bounce = Bounce(self.rect.x, self.rect.y, self.rect.y + random.randint(0, 123), self.size)

    def update_bounce(self):
        """Updates the bouncing behavior of the object."""
        if not self.bounce:
            return
        if self.bounce.speed < 0.004:
            self.dropped = False
            self.bounce.reset()
        elif self.dropped:
            for _ in range(15):
                self.bounce.move()
                self.bounce.bounce()
            self.rect.x = self.bounce.x
            self.rect.y = self.bounce.y

    def load_image(self):
        """Loads the image assets for the object."""
        self.original_image = pygame.image.load(
            f'{self.path}/{self.name}.png').convert_alpha()
        self.original_image = pygame.transform.scale(self.original_image, self.size)
        self.image_picked = pygame.image.load(
            f'{self.path}/{self.name}_picked.png').convert_alpha()
        self.image_picked = pygame.transform.scale(self.image_picked, self.size)
        self.hud_image = pygame.image.load(
            f'{self.path}/{self.name}_hud.png').convert_alpha()
        self.image = self.original_image

    def detect_collision(self):
        """Detects collision with the player for interaction."""
        if self.game.player.hitbox.colliderect(self.rect) and self.game.player.interaction:
            self.image = self.image_picked
            self.interaction = True
        else:
            self.image = self.original_image
            self.interaction = False
            self.show_name.reset_line_length()

    def drop(self):
        """Drops the object from the player's inventory."""
        self.room = self.game.room
        self.rect.x = self.game.player.rect.x
        self.rect.y = self.game.player.rect.y
        self.game.player.items.remove(self)
        self.game.player.weapon = None
        self.game.room.objects.append(self)
        if self.game.player.items:
            self.game.player.weapon = self.game.player.items[-1]

    def update(self):
        """Updates the object's state."""
        pass

    def update_hitbox(self):
        """Updates the hitbox of the object after movement."""
        self.hitbox = get_mask_rect(self.image, *self.rect.topleft)
        self.hitbox.midbottom = self.rect.midbottom

    def interact(self):
        """Performs interaction with the object."""
        pass

    def remove_object(self):
        """Removes the object from the room."""
        self.room.objects.remove(self)
    #only allow the player to buy if have higher gold
    def buy(self):
        """
        Buys the object if the player has enough gold.

        Note:
            Only allows the player to buy if they have enough gold.
        """
        if self.game.player.gold >= self.value:
            self.game.player.gold -= self.value
            self.interact()
            self.for_sale = False

    def draw(self):
        """Draws the object on the game surface."""
        surface = self.room.tile_map.map_surface
        # self.room.tile_map.map_surface.blit(self.image, (self.rect.x + 64, self.rect.y + 32))
        surface.blit(self.image, (self.rect.x, self.rect.y))
        if self.interaction:
            self.show_name.draw(surface, self.rect)

class Bounce:
    """
    Represents bouncing behavior for an object.

    Attributes:
        x (float): The x-coordinate of the object.
        y (float): The y-coordinate of the object.
        limit (float): The limit for bouncing.
        size (tuple): The size of the object.
        speed (float): The speed of the bounce.
        angle (float): The angle of the bounce.
        drag (float): The drag applied to the bounce.
        elasticity (float): The elasticity of the bounce.
        gravity (tuple): The gravity affecting the bounce.
        limits (list): List of limits for bouncing.
        
    Methods:
        add_vectors(angle1, length1, angle2, length2): Adds two vectors.
        move(): Moves the bounce according to the gravity and drag.
        bounce(): Handles bouncing behavior of the object.
        reset(): Resets the attributes of the bounce.
    """
    def __init__(self, x, y, limit, size):
        """
        Initializes a Bounce instance.

        Args:
            x (float): The x-coordinate of the object.
            y (float): The y-coordinate of the object.
            limit (float): The limit for bouncing.
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

    @staticmethod
    def add_vectors(angle1, length1, angle2, length2):
        """
        Adds two vectors.

        Args:
            angle1 (float): The angle of the first vector.
            length1 (float): The length of the first vector.
            angle2 (float): The angle of the second vector.
            length2 (float): The length of the second vector.

        Returns:
            tuple: The angle and length of the resulting vector.
        """
        x = math.sin(angle1) * length1 + math.sin(angle2) * length2
        y = math.cos(angle1) * length1 + math.cos(angle2) * length2
        angle = 0.5 * math.pi - math.atan2(y, x)
        length = math.hypot(x, y)
        return angle, length

    def move(self):
        """Moves the bounce according to the gravity and drag."""
        self.angle, self.speed = self.add_vectors(self.angle, self.speed, *self.gravity)
        self.x += math.sin(self.angle) * self.speed
        self.y -= math.cos(self.angle) * self.speed
        self.speed *= self.drag

    def bounce(self):
        """Handles bouncing behavior of the object."""
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
        """Resets the attributes of the bounce."""
        self.speed = 0.5
        self.angle = random.choice([10, -10])
        self.drag = 0.999
        self.elasticity = 0.75
