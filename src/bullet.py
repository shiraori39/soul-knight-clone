import math
import pygame
import random

#Bullet base class 
class Bullet():
    def __init__(self, game, master, room, x, y, target):
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
    #direction of the bullet
    def calculate_dir(self):
        length = math.hypot(*self.dir)
        self.dir = pygame.math.Vector2(self.dir[0] / length, self.dir[1] / length)
    #setter function
    def set_damage(self, value):
        self.damage = value
    #load image function
    def load_image(self):
        self.image = pygame.Surface([self.bullet_size, self.bullet_size])
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
    #update pos of the bullet
    def update_position(self):
        if self.room == self.game.world_manager.current_room:
            self.pos = (self.pos[0] + self.dir[0] * self.speed,
                        self.pos[1] + self.dir[1] * self.speed)

            self.rect.x = self.pos[0]  #
            self.rect.y = self.pos[1]  #
    #delete the bullet
    def kill(self):
        if self in self.game.bullet_manager.bullets:
            self.game.bullet_manager.bullets.remove(self)
    #update function
    def update(self):
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
    #draw function
    def draw(self):
        surface = self.master.room.tile_map.map_surface
        pygame.draw.circle(surface, (255, 255, 255), (self.rect.x + self.radius / 2, self.rect.y + self.radius / 2),
                           self.radius)
        pygame.draw.circle(surface, (58, 189, 74), (self.rect.x + self.radius / 2, self.rect.y + self.radius / 2),
                           self.radius - 1)
    #delete if hit a wall
    def wall_collision(self):
        collide_points = (self.rect.midbottom, self.rect.bottomleft, self.rect.bottomright)
        for wall in self.game.world_manager.current_map.wall_list:
            if any(wall.hitbox.collidepoint(point) for point in collide_points):
                self.kill()
                break
    #deal dmg to player
    def player_collision(self, collision_enemy):
        if self.rect.colliderect(collision_enemy.hitbox) and not self.game.world_manager.switch_room:
            if collision_enemy.shield:
                collision_enemy.shield -= 1
            else:
                self.game.player.hp -= self.damage
                self.game.player.hurt = True
                self.game.player.entity_animation.hurt_timer = pygame.time.get_ticks()
            self.kill()

    def bounce(self):
        if (
                self.game.player.weapon
                and self.game.player.attacking
                and pygame.sprite.collide_mask(self.game.player.weapon, self)
                and self.bounce_back
        ):
            self.dir = (-self.dir[0] + random.randint(-20, 10) / 100, -self.dir[1] + random.randint(-10, 10) / 100)
            self.speed *= random.randint(10, 20) / 10
            self.bounce_back = False

#inherited from bullet class
class ImpBullet(Bullet):
    speed = 5
    bullet_size = 7
    radius = 5

    def __init__(self, game, master, room, x, y, target):
        super().__init__(game, master, room, x, y, target)
        self.damage = master.damage

#inherited from bullet class
class BossBullet(Bullet):
    speed = 7
    bullet_size = 7
    radius = 5

    def __init__(self, game, master, room, x, y, target, rotation=None):
        super().__init__(game, master, room, x, y, target)
        if rotation:
            self.dir.rotate_ip(rotation)
        self.damage = master.bullet_damage

    def kill(self):
        if self in self.game.bullet_manager.bullets:
            self.game.bullet_manager.bullets.remove(self)

#inherited from boss bullet class
class MachineGunBullet(BossBullet):

    def __init__(self, game, master, room, x, y, target, rotation=None):
        super().__init__(game, master, room, x, y, target)

    def update(self):
        self.update_position()
        self.player_collision(self.game.player)
        if self.rect.y < 0 or self.rect.y > 1000 or self.rect.x < 0 or self.rect.x > 1300:
            self.kill()
        self.wall_collision()

#a bullet manager containing all the bullets 
class BulletManager:

    def __init__(self, game):
        self.game = game
        self.bullets = []

    def remove_bullets(self):
        for bullet in self.bullets:
            if self.game.world_manager.current_room is not bullet.room:
                self.bullets.remove(bullet)
                #self.kill(bullet)

    def add_bullet(self, bullet):
        self.bullets.append(bullet)

    def kill(self, bullet):
        self.bullets.remove(bullet)

    def update(self):
        self.remove_bullets()
        for bullet in self.bullets:
            bullet.update()

    def draw(self):
        for bullet in self.bullets:
            bullet.draw()
