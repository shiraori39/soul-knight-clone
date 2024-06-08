import math
import pygame
import random


class Bullet():
    """
    A base class for bullets fired by entities.

    Attributes
    ----------
    game : Game
        The game instance.
    master : Entity
        The entity firing the bullet.
    room : Room
        The room in which the bullet exists.
    image : pygame.Surface
        The image of the bullet.
    rect : pygame.Rect
        The rectangular bounding box of the bullet.
    pos : tuple
        The current position of the bullet.
    dir : pygame.math.Vector2
        The direction vector of the bullet.
    bounce_back : bool
        Indicates whether the bullet can bounce back upon collision.

    Methods
    -------
    calculate_dir():
        Calculates the direction vector of the bullet.
    set_damage(value):
        Sets the damage value of the bullet.
    load_image():
        Loads the image of the bullet.
    update_position():
        Updates the position of the bullet based on its direction and speed.
    kill():
        Removes the bullet from the game.
    update():
        Updates the bullet's position and handles collisions.
    draw():
        Draws the bullet on the screen.
    wall_collision():
        Handles collision with walls.
    player_collision(collision_enemy):
        Handles collision with the player.
    bounce():
        Implements bouncing behavior.
    """
    def __init__(self, game, master, room, x, y, target):
        """
        Initializes the Bullet instance.

        Parameters
        ----------
        game : Game
            The game instance.
        master : Entity
            The entity firing the bullet.
        room : Room
            The room in which the bullet exists.
        x : int
            The x-coordinate of the bullet's initial position.
        y : int
            The y-coordinate of the bullet's initial position.
        target : tuple
            The target position towards which the bullet moves.
        """
        super().__init__()
        self.game = game
        self.master = master
        self.room = room
        self.image = None
        self.rect = None
        self.load_image()
        self.rect.x = x
        self.rect.y = y
        self.pos = (x, y)
        self.dir = pygame.math.Vector2(target[0] - x, target[1] - y)
        self.calculate_dir()
        self.bounce_back = True

    def calculate_dir(self):
        """Calculates the direction vector of the bullet."""
        length = math.hypot(*self.dir)
        self.dir = pygame.math.Vector2(self.dir[0] / length, self.dir[1] / length)

    def set_damage(self, value):
        """
        Sets the damage value of the bullet.

        Parameters
        ----------
        value : int
            The damage value to be set.
        """
        self.damage = value

    def load_image(self):
        """Loads the image of the bullet."""
        self.image = pygame.Surface([self.bullet_size, self.bullet_size])
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()

    def update_position(self):
        """Updates the position of the bullet based on its direction and speed."""
        if self.room == self.game.world_manager.current_room:
            self.pos = (self.pos[0] + self.dir[0] * self.speed,
                        self.pos[1] + self.dir[1] * self.speed)

            self.rect.x = self.pos[0]  #
            self.rect.y = self.pos[1]  #

    def kill(self):
        """Removes the bullet from the game."""
        if self in self.game.bullet_manager.bullets:
            self.game.bullet_manager.bullets.remove(self)

    def update(self):
        """Updates the bullet's position and handles collisions."""
        self.update_position()
        if self.bounce_back is False:
            for enemy in self.game.enemy_manager.enemy_list:
                if self.rect.colliderect(enemy.hitbox):
                    enemy.hp -= self.damage
                    self.kill()
                    break
        self.player_collision(self.game.player)
        self.bounce()
        if self.rect.y < 0 or self.rect.y > 1000 or self.rect.x < 0 or self.rect.x > 1300:
            self.kill()
        self.wall_collision()

    def draw(self):
        """Draws the bullet on the screen."""
        surface = self.master.room.tile_map.map_surface
        pygame.draw.circle(surface, (255, 255, 255), (self.rect.x + self.radius / 2, self.rect.y + self.radius / 2),
                           self.radius)
        pygame.draw.circle(surface, (58, 189, 74), (self.rect.x + self.radius / 2, self.rect.y + self.radius / 2),
                           self.radius - 1)

    def wall_collision(self):
        """Handles collision with walls."""
        collide_points = (self.rect.midbottom, self.rect.bottomleft, self.rect.bottomright)
        for wall in self.game.world_manager.current_map.wall_list:
            if any(wall.hitbox.collidepoint(point) for point in collide_points):
                self.kill()
                break

    def player_collision(self, collision_enemy):
        """
        Handles collision with the player.

        Parameters
        ----------
        collision_enemy : Entity
            The entity with which the bullet collides.
        """
        if self.rect.colliderect(collision_enemy.hitbox) and not self.game.world_manager.switch_room:
            if collision_enemy.shield:
                collision_enemy.shield -= 1
            else:
                self.game.player.hp -= self.damage
                self.game.player.hurt = True
                self.game.player.entity_animation.hurt_timer = pygame.time.get_ticks()
            self.kill()

    def bounce(self):
        """Implements bouncing behavior."""       
        if (
                self.game.player.weapon
                and self.game.player.attacking
                and pygame.sprite.collide_mask(self.game.player.weapon, self)
                and self.bounce_back
        ):
            self.dir = (-self.dir[0] + random.randint(-20, 10) / 100, -self.dir[1] + random.randint(-10, 10) / 100)
            self.speed *= random.randint(10, 20) / 10
            self.bounce_back = False


class ImpBullet(Bullet):
    """
    A class representing bullets fired by imp enemies.

    Attributes
    ----------
    speed : int
        The speed of the bullet.
    bullet_size : int
        The size of the bullet.
    radius : int
        The radius of the bullet.

    Methods
    -------
    __init__(game, master, room, x, y, target):
        Initializes the ImpBullet instance.
    """
    speed = 5
    bullet_size = 7
    radius = 5

    def __init__(self, game, master, room, x, y, target):
        """
        Initializes the ImpBullet instance.

        Parameters
        ----------
        game : Game
            The game instance.
        master : Entity
            The entity firing the bullet.
        room : Room
            The room in which the bullet exists.
        x : int
            The x-coordinate of the bullet's initial position.
        y : int
            The y-coordinate of the bullet's initial position.
        target : tuple
            The target position towards which the bullet moves.
        """
        super().__init__(game, master, room, x, y, target)
        self.damage = master.damage


class BossBullet(Bullet):
    """
    A class representing bullets fired by boss enemies.

    Attributes
    ----------
    speed : int
        The speed of the bullet.
    bullet_size : int
        The size of the bullet.
    radius : int
        The radius of the bullet.

    Methods
    -------
    __init__(game, master, room, x, y, target, rotation=None):
        Initializes the BossBullet instance.
    kill():
        Removes the bullet from the game.
    """
    speed = 7
    bullet_size = 7
    radius = 5

    def __init__(self, game, master, room, x, y, target, rotation=None):
        """
        Initializes the BossBullet instance.

        Parameters
        ----------
        game : Game
            The game instance.
        master : Entity
            The entity firing the bullet.
        room : Room
            The room in which the bullet exists.
        x : int
            The x-coordinate of the bullet's initial position.
        y : int
            The y-coordinate of the bullet's initial position.
        target : tuple
            The target position towards which the bullet moves.
        rotation : float, optional
            The rotation angle (in degrees) of the bullet (default is None).
        """
        super().__init__(game, master, room, x, y, target)
        if rotation:
            self.dir.rotate_ip(rotation)
        self.damage = master.bullet_damage

    def kill(self):
        """Removes the bullet from the game."""
        if self in self.game.bullet_manager.bullets:
            self.game.bullet_manager.bullets.remove(self)

class MachineGunBullet(BossBullet):
    """
    A class representing bullets fired by boss enemies with a machine gun.

    Methods
    -------
    __init__(game, master, room, x, y, target, rotation=None):
        Initializes the MachineGunBullet instance.
    update():
        Updates the bullet's position and handles collisions.
    """
    def __init__(self, game, master, room, x, y, target, rotation=None):
        """
        Initializes the MachineGunBullet instance.

        Parameters
        ----------
        game : Game
            The game instance.
        master : Entity
            The entity firing the bullet.
        room : Room
            The room in which the bullet exists.
        x : int
            The x-coordinate of the bullet's initial position.
        y : int
            The y-coordinate of the bullet's initial position.
        target : tuple
            The target position towards which the bullet moves.
        rotation : float, optional
            The rotation angle (in degrees) of the bullet (default is None).
        """
        super().__init__(game, master, room, x, y, target)

    def update(self):
        """Updates the bullet's position and handles collisions."""
        self.update_position()
        self.player_collision(self.game.player)
        if self.rect.y < 0 or self.rect.y > 1000 or self.rect.x < 0 or self.rect.x > 1300:
            self.kill()
        self.wall_collision()

class BulletManager:
    """
    A class to manage bullets in the game.

    Attributes
    ----------
    game : Game
        The game instance.
    bullets : list
        A list to store all active bullets.

    Methods
    -------
    remove_bullets():
        Removes bullets that are not in the current room.
    add_bullet(bullet):
        Adds a new bullet to the bullet list.
    kill(bullet):
        Removes a specified bullet from the bullet list.
    update():
        Updates the position of all bullets and handles their collisions.
    draw():
        Draws all active bullets on the screen.
    """
    def __init__(self, game):
        """
        Initializes the BulletManager instance.

        Parameters
        ----------
        game : Game
            The game instance.
        """
        self.game = game
        self.bullets = []

    def remove_bullets(self):
        """Removes bullets that are not in the current room."""
        for bullet in self.bullets:
            if self.game.world_manager.current_room is not bullet.room:
                self.bullets.remove(bullet)
                #self.kill(bullet)

    def add_bullet(self, bullet):
        """
        Adds a new bullet to the bullet list.

        Parameters
        ----------
        bullet : Bullet
            The bullet to be added.
        """
        self.bullets.append(bullet)

    def kill(self, bullet):
        """
        Removes a specified bullet from the bullet list.

        Parameters
        ----------
        bullet : Bullet
            The bullet to be removed.
        """
        self.bullets.remove(bullet)

    def update(self):
        """Updates the position of all bullets and handles their collisions."""
        self.remove_bullets()
        for bullet in self.bullets:
            bullet.update()

    def draw(self):
        """Draws all active bullets on the screen."""
        for bullet in self.bullets:
            bullet.draw()
