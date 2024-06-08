import math

import pygame
from pygame.math import Vector2
from src.utils import get_mask_rect
from PIL import Image
from .object import Object

class WeaponSwing:
    """
    A class representing the swing behavior of a weapon.

    This class manages the rotation and swinging animation of a weapon during player interaction. It calculates the angle of rotation based on the mouse position relative to the player's hitbox, controls the swinging motion of the weapon, and updates the position and hitbox accordingly.

    Attributes:
        left_swing (int): The angle of rotation for the left swing motion.
        right_swing (int): The angle of rotation for the right swing motion.
        weapon (Weapon): The weapon object associated with the swing behavior.
        angle (float): The current angle of rotation of the weapon.
        offset (Vector2): The offset vector representing the initial position of the weapon relative to the player.
        offset_rotated (Vector2): The rotated offset vector based on the current angle of rotation.
        counter (int): A counter for tracking the progress of the swing animation.
        swing_side (int): An indicator (-1 or 1) representing the direction of the swing motion.

    Methods:
        reset(self): Resets the swing animation counter.
        rotate(self, weapon=None): Rotates the weapon based on the mouse position.
        swing(self): Performs the swinging animation of the weapon.
    """

    left_swing = 10
    right_swing = -190

    def __init__(self, weapon):
        """
        Initialize the WeaponSwing object.

        Args:
            weapon (Weapon): The weapon object associated with the swing behavior.
        """
        self.weapon = weapon
        self.angle = 0
        self.offset = Vector2(0, -50)
        self.offset_rotated = Vector2(0, -25)
        self.counter = 0
        self.swing_side = 1

    def reset(self):
        """
        Reset the swing animation counter.
        """
        self.counter = 0

    def rotate(self, weapon=None):
        """
        Rotate the weapon based on the mouse position.

        Args:
            weapon (bool, optional): Indicates whether to update the weapon image. Defaults to None.
        """
        mx, my = pygame.mouse.get_pos()
        dx = mx - self.weapon.player.hitbox.centerx
        dy = my - self.weapon.player.hitbox.centery

        if self.swing_side == 1:
            self.angle = (180 / math.pi) * math.atan2(-self.swing_side * dy, dx) + self.left_swing
        else:
            self.angle = (180 / math.pi) * math.atan2(self.swing_side * dy, dx) + self.right_swing

        position = self.weapon.player.hitbox.center

        if weapon:
            self.weapon.image = pygame.transform.rotozoom(self.weapon.image, self.angle, 1)
        else:
            self.weapon.image = pygame.transform.rotozoom(self.weapon.original_image, self.angle, 1)

        self.offset_rotated = self.offset.rotate(-self.angle)
        self.weapon.rect = self.weapon.image.get_rect(center=position + self.offset_rotated)
        self.weapon.hitbox = pygame.mask.from_surface(self.weapon.image)

    def swing(self):
        """
        Perform the swinging animation of the weapon.
        """
        self.angle += 20 * self.swing_side
        position = self.weapon.player.hitbox.center
        self.weapon.image = pygame.transform.rotozoom(self.weapon.original_image, self.angle, 1)
        self.offset_rotated = self.offset.rotate(-self.angle)
        self.weapon.rect = self.weapon.image.get_rect(center=position + self.offset_rotated)
        self.weapon.hitbox = pygame.mask.from_surface(self.weapon.image)
        self.counter += 1


class Weapon(Object):
    """
    A class representing a weapon object in the game.

    This class encapsulates functionality related to weapons that can be wielded by the player character in the game world. It handles loading weapon images, detecting collisions with the player, interacting with the player, dropping the weapon, hitting enemies, updating weapon state when wielded by the player, updating general weapon state, and drawing the weapon on the screen.

    Attributes:
        scale (int): The scale factor for the weapon's size.
        size (tuple): The size of the weapon, represented as a tuple of width and height.
        player (Player): The player who possesses the weapon.
        time (int): A time attribute for tracking weapon usage or other time-related operations.
        weapon_swing (WeaponSwing): An instance of WeaponSwing class for handling weapon swings.
        starting_position (list): The starting position of the weapon represented as a list [x, y].
        original_image (pygame.Surface): The original image of the weapon before any transformations.
        image_picked (pygame.Surface): The image of the weapon when picked up by the player.
        hud_image (pygame.Surface): The image of the weapon displayed in the heads-up display (HUD).
        image (pygame.Surface): The current image of the weapon to be displayed on the screen.
        rect (pygame.Rect): The rectangular area occupied by the weapon on the screen.
        hitbox (pygame.Rect): The hitbox of the weapon for collision detection purposes.
        interaction (bool): A flag indicating whether the weapon is currently interacting with the player.

    Methods:
        load_image(self): Load weapon image and initialize instance variables.
        detect_collision(self): Detect collision between player and weapon.
        interact(self): Interact with the player to pick up the weapon.
        drop(self): Drop the weapon from the player's possession.
        enemy_collision(self): Handle collision with enemies and apply damage if necessary.
        player_update(self): Update the state of the weapon when held by the player.
        update(self): Update the state of the weapon.
        draw(self): Draw the weapon on the screen.
    """
    def __init__(self, game, name=None, size=None, room=None, position=None):
        self.scale = 3
        Object.__init__(self, game, name, 'weapon', size, room, position)
        self.size = size
        self.player = None
        self.load_image()
        if position:
            self.rect.x, self.rect.y = position[0], position[1]
        self.time = 0
        self.weapon_swing = WeaponSwing(self)
        self.starting_position = [self.hitbox.bottomleft[0] - 1, self.hitbox.bottomleft[1]]
    #load weapon's image
    def load_image(self):
        """Load weapon image and initialize instance variables"""
        self.size = tuple(self.scale * x for x in Image.open(f'./assets/objects/weapon/{self.name}/{self.name}.png').size)
        self.original_image = pygame.image.load(f'./assets/objects/weapon/{self.name}/{self.name}.png').convert_alpha()
        self.original_image = pygame.transform.scale(self.original_image, self.size)
        self.image_picked = pygame.image.load(f'./assets/objects/weapon/{self.name}/picked_{self.name}.png').convert_alpha()
        self.image_picked = pygame.transform.scale(self.image_picked, self.size)
        self.hud_image = pygame.image.load(f'./assets/objects/weapon/{self.name}/{self.name}_hud.png').convert_alpha()
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.hitbox = get_mask_rect(self.original_image, *self.rect.topleft)
    #player and weapon collide with each other in order to equip
    def detect_collision(self):
        if self.game.player.hitbox.colliderect(self.rect):
            self.image = self.image_picked
            self.interaction = True
        else:
            self.image = self.original_image
            self.interaction = False
            self.show_name.reset_line_length()
    #player get the waepon
    def interact(self):
        self.weapon_swing.reset()
        self.player = self.game.player
        self.player.items.append(self)
        if not self.player.weapon:
            self.player.weapon = self
        if self.room == self.game.world_manager.current_room:
            self.room.objects.remove(self)
        self.interaction = False
        self.show_name.reset_line_length()
    #player drop weapon
    def drop(self):
        self.room = self.game.world_manager.current_room
        self.player.items.remove(self)
        self.player.weapon = None
        self.game.world_manager.current_room.objects.append(self)
        if self.player.items:
            self.player.weapon = self.player.items[-1]
        self.load_image()
        self.rect = self.image.get_rect()
        self.hitbox = get_mask_rect(self.image, *self.rect.topleft)
        self.rect.x = self.player.rect.x
        self.rect.y = self.player.rect.y
        self.player = None
        self.weapon_swing.offset_rotated = Vector2(0, -25)
    #hitting enemy
    def enemy_collision(self):
        for enemy in self.game.enemy_manager.enemy_list:
            if (
                    pygame.sprite.collide_mask(self.game.player.weapon, enemy)
                    and enemy.dead is False
                    and enemy.can_get_hurt_from_weapon()
            ):
                self.game.player.weapon.special_effect(enemy)
                enemy.hurt = True
                enemy.hp -= self.game.player.weapon.damage * self.game.player.strength
                enemy.entity_animation.hurt_timer = pygame.time.get_ticks()
                enemy.weapon_hurt_cooldown = pygame.time.get_ticks()
    #if currently equiped by player then update
    def player_update(self):
        self.interaction = False
        if self.weapon_swing.counter == 10:
            self.original_image = pygame.transform.flip(self.original_image, 1, 0)
            self.player.attacking = False
            self.weapon_swing.counter = 0
        if self.player.attacking and self.weapon_swing.counter <= 10:
            self.weapon_swing.swing()
            self.enemy_collision()
        else:
            self.weapon_swing.rotate()
    #update function
    def update(self):
        self.hovering.hovering()
        if self.player:
            self.player_update()
        else:
            self.show_price.update()
            self.update_bounce()
        self.update_hitbox()
    #draw function
    def draw(self):
        surface = self.room.tile_map.map_surface
        if self.player:
            surface = self.game.screen
        surface.blit(self.image, self.rect)
        if self.interaction:
            self.show_name.draw(surface, self.rect)
        self.show_price.draw(surface)

#Create a katana inherited from weapon class
class Katana(Weapon):
    """
    A class representing a katana weapon object in the game.

    This class inherits from the Weapon class and specializes in representing a katana weapon within the game environment. It provides functionality specific to the katana weapon, including its damage, size, special slashing effect, and updating its behavior during player interaction.

    Attributes:
        name (str): The name of the katana weapon.
        damage (int): The damage inflicted by the katana when attacking enemies.
        size (tuple): The size of the katana weapon, represented as a tuple of width and height.
        value (int): The value of the katana weapon, typically used for currency or trading within the game.
        damage_enemies (list): A list containing instances of the Slash class representing enemies damaged by the katana.

    Methods:
        __init__(self, game, room=None, position=None): Initializes the Katana object.
        enemy_in_list(self, enemy): Checks if an enemy is already in the list of damaged enemies.
        special_effect(self, enemy): Applies the special slashing effect of the katana on an enemy.
        player_update(self): Overrides the player_update method of the Weapon class to update katana behavior during player interaction.
    """
    name = 'katana'
    damage = 1000
    size = (36, 90)

    def __init__(self, game, room=None, position=None):
        super().__init__(game, self.name, self.size, room, position)
        self.value = 100
        self.damage_enemies = []

    class Slash:
        def __init__(self, enemy, weapon):
            self.enemy = enemy
            self.weapon = weapon
            self.damage = 0.1

        def update(self):
            self.enemy.hp -= self.weapon.damage * self.damage
            self.update_damage()

        def update_damage(self):
            self.damage += 0.1

        def draw(self):
            pass
    #get all enemy hit
    def enemy_in_list(self, enemy):
        for e in self.damage_enemies:
            if e.enemy is enemy:
                return True
    #update enemy hit
    def special_effect(self, enemy):
        for e in self.damage_enemies:
            if e.enemy is enemy:
                e.update()
        if not self.enemy_in_list(enemy):
            self.damage_enemies.append(self.Slash(enemy, self))
    #overload player_update function
    def player_update(self):
        self.interaction = False
        if self.weapon_swing.counter == 10:
            self.original_image = pygame.transform.flip(self.original_image, 1, 0)
            self.player.attacking = False
            self.weapon_swing.counter = 0
            self.game.screen_position = (0, 0)
        if self.player.attacking and self.weapon_swing.counter <= 10:
            self.weapon_swing.swing()
            self.enemy_collision()
        else:
            self.weapon_swing.rotate()

