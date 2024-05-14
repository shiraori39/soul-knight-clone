import pygame
import src.utils as utils
from .animation import load_animation_sprites, EntityAnimation
from src.utils import get_mask_rect

#Create a base class for all entities in the game 
class Entity:
    def __init__(self, game, name):
        self.game = game
        self.name = name
        self.path = f'./assets/characters/{self.name}'
        self.animation_database = load_animation_sprites(f'{self.path}/')
        self.image = pygame.transform.scale(pygame.image.load(f'{self.path}/idle/idle0.png'),
                                            utils.basic_entity_size).convert_alpha()
        self.rect = self.image.get_rect()
        self.hitbox = get_mask_rect(self.image, *self.rect.topleft)
        self.velocity = [0, 0]
        self.hurt = False
        self.dead = False
        self.direction = 'right'
        self.can_move = True
        self.entity_animation = EntityAnimation(self)
        self.time = 0
        self.can_get_hurt = True
    #Get functions
    def __repr(self):
        return self.name

    def __str__(self):
        return f'{id(self)}, {self.name}'
    #set velocity function
    def set_velocity(self, new_velocity):
        self.velocity = new_velocity

    def drop_items(self):
        pass
    #check if dead
    def detect_death(self):
        if self.hp <= 0 and self.dead is False:
            self.dead = True
            self.entity_animation.animation_frame = 0
            self.can_move = False
            self.velocity = [0, 0]
        if self.death_counter == 0:
            self.drop_items()
            if self.room:
                self.room.enemy_list.remove(self)
    #do all update functions
    def basic_update(self):
        self.detect_death()
        self.update_hitbox()
        self.entity_animation.update()
        self.rect.move_ip(self.velocity)
        self.hitbox.move_ip(self.velocity)
    #if hit wall
    def wall_collision(self):
        test_rect = self.hitbox.move(*self.velocity)  # Position after moving, change name later
        collide_points = (test_rect.midbottom, test_rect.bottomleft, test_rect.bottomright)
        for wall in self.game.world_manager.current_map.wall_list:
            if any(wall.hitbox.collidepoint(point) for point in collide_points):
                self.velocity = [0, 0]
    #update self hitbox after moving
    def update_hitbox(self):
        self.hitbox = get_mask_rect(self.image, *self.rect.topleft)
        self.hitbox.midbottom = self.rect.midbottom
    #return velocity to update coordinate
    def moving(self):
        return self.velocity[0] != 0 or self.velocity[1] != 0
