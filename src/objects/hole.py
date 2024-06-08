import pygame
from .object import Object

class Hole:
    """
    Class representing a passage to the next level.

    Attributes:
        name (str): The name of the hole.
        game (Game): The main game object.
        position (tuple): The position of the hole.
        room (Room): The room containing the hole.
        image (Surface): The image representing the hole.
        image_picked (Surface): The image representing the picked hole.
        images (list): A list of images for animation.
        rect (Rect): The rectangular area occupied by the hole.
        animation_frame (float): The current frame of animation.
        animate (bool): Flag indicating whether the hole should animate.
        interaction (bool): Flag indicating whether the hole is interactable.
    """
    
    name = 'next_level'

    def __init__(self, game, position, room):
        """
        Initializes a Hole object.

        Args:
            game (Game): The main game object.
            position (tuple): The position of the hole.
            room (Room): The room containing the hole.
        """
        self.game = game
        self.room = room
        self.image = None
        self.image_picked = pygame.image.load('./assets/objects/passage/passage_picked.png').convert_alpha()
        self.images = []
        self.load_image()
        self.position = position
        self.rect = self.image.get_rect()
        self.rect.topleft = self.position
        self.animation_frame = 0
        self.animate = True
        self.interaction = False

    def load_image(self):
        """Load images for animation."""
        for i in range(5):
            image = pygame.image.load(f'./assets/objects/passage/passage{i}.png').convert_alpha()
            self.images.append(image)
        self.image = self.images[0]

    def update_animation_frame(self):
        """Update the animation frame."""
        self.animation_frame += 1.5 / 15
        if self.animation_frame > 4:
            self.animate = False
        self.image = self.images[int(self.animation_frame)]

    def interact(self):
        """Interact with the hole, loading the next level."""
        self.game.world_manager.load_new_level()

    def detect_collision(self):
        """Detect collision with the player."""
        if self.game.player.hitbox.colliderect(self.rect) and self.game.player.interaction:
            self.image = self.image_picked
            self.interaction = True
        else:
            self.image = self.images[4]
            self.interaction = False

    def update(self):
        """Update the hole."""
        if self.animate:
            self.update_animation_frame()

    def draw(self):
        """Draw the hole on the screen."""
        surface = self.room.tile_map.map_surface
        surface.blit(self.image, (self.rect.x, self.rect.y))
