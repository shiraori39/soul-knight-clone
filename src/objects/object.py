import pygame
from src.utils import get_mask_rect
import src.utils as utils
import random
import math

#a class to draw name of an item name when colliding
class ShowName:
    # drawing animation dependent on player position
    def __init__(self, object):
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
        """Wait 'amount' amount of time"""
        if pygame.time.get_ticks() - time > amount:
            return True
    #call all draw function
    def draw(self, surface, rect):
        self.draw_text_line(surface, rect)
        self.draw_text(surface)
    #draw text function
    def draw_text(self, surface):
        text_surface = pygame.font.Font(utils.font, 15).render(self.text[:self.counter], True, (255, 255, 255))
        surface.blit(text_surface, self.text_position)
    #draw the line (decoration)
    def draw_text_line(self, surface, rect):
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
        self.line_length = 0
        self.counter = 0

#show the price of the item
class ShowPrice(ShowName):
    def __init__(self, object):
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
    #set function
    def set_text_position(self, position):
        self.text_position = position
        self.image_rect = (position[0] - 25, position[1] - 8)
    #get coin image frames
    def load_image(self):
        for i in range(4):
            image = pygame.image.load(f'./assets/objects/coin/coin/coin{i}.png').convert_alpha()
            image = pygame.transform.scale(image, self.image_size)
            self.images.append(image)
        self.image = self.images[0]
    #update coin animation
    def update_animation_frame(self):
        self.animation_frame += 1.5 / 15  # random.randint(10, 20)/100
        if self.animation_frame > 3:
            self.animation_frame = 0
        self.image = self.images[int(self.animation_frame)]
    #update function
    def update(self):
        # self.image_rect.topleft = (self.object.hitbox.midbottom[0] - 15, self.object.hitbox.midbottom[1] + 10)
        # self.text_position = (self.image_rect.topleft[0] + 25, self.image_rect.topleft[1] + 8)
        self.update_animation_frame()
    #draw text function
    def draw_text(self, surface):
        text_surface = pygame.font.Font(utils.font, 18).render(self.text, True, (255, 255, 255))
        surface.blit(text_surface, self.text_position)
    #draw function
    def draw(self, surface):
        if self.object.for_sale:
            surface.blit(self.image, self.image_rect)
            self.draw_text(surface)

#Class to check player on top of items
class Hovering:
    def __init__(self, game, obj):
        self.game = game
        self.object = obj
        self.hover_value = 0
        self.position = 1

    def set_hover_value(self):
        num = self.game.object_manager.up // 2
        if num % 2 == 0:
            self.hover_value = -5
        elif num % 2 == 1:
            self.hover_value = 5

    def hovering(self):
        if self.object.player is not None:
            return
        if self.object.game.object_manager.hover:
            self.object.rect.y += self.hover_value
        self.set_hover_value()
#Base object class for inheritance
class Object:
    def __init__(self, game, name, object_type, size=None, room=None, position=None, player=None):
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
        return self.name
    #for some object like heath potion or coins to bounce around
    def activate_bounce(self):
        self.bounce = Bounce(self.rect.x, self.rect.y, self.rect.y + random.randint(0, 123), self.size)
    #item movement
    def update_bounce(self):
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
    #load item images from assets
    def load_image(self):
        self.original_image = pygame.image.load(
            f'{self.path}/{self.name}.png').convert_alpha()
        self.original_image = pygame.transform.scale(self.original_image, self.size)
        self.image_picked = pygame.image.load(
            f'{self.path}/{self.name}_picked.png').convert_alpha()
        self.image_picked = pygame.transform.scale(self.image_picked, self.size)
        self.hud_image = pygame.image.load(
            f'{self.path}/{self.name}_hud.png').convert_alpha()
        self.image = self.original_image
    #check player on top of item for interacting
    def detect_collision(self):
        if self.game.player.hitbox.colliderect(self.rect) and self.game.player.interaction:
            self.image = self.image_picked
            self.interaction = True
        else:
            self.image = self.original_image
            self.interaction = False
            self.show_name.reset_line_length()
    #player drop item
    def drop(self):
        self.room = self.game.room
        self.rect.x = self.game.player.rect.x
        self.rect.y = self.game.player.rect.y
        self.game.player.items.remove(self)
        self.game.player.weapon = None
        self.game.room.objects.append(self)
        if self.game.player.items:
            self.game.player.weapon = self.game.player.items[-1]

    def update(self):
        pass
    #update hitbox after movement
    def update_hitbox(self):
        self.hitbox = get_mask_rect(self.image, *self.rect.topleft)
        self.hitbox.midbottom = self.rect.midbottom

    def interact(self):
        pass
    #remove object
    def remove_object(self):
        self.room.objects.remove(self)
    #only allow the player to buy if have higher gold
    def buy(self):
        if self.game.player.gold >= self.value:
            self.game.player.gold -= self.value
            self.interact()
            self.for_sale = False
    #draw function
    def draw(self):
        surface = self.room.tile_map.map_surface
        # self.room.tile_map.map_surface.blit(self.image, (self.rect.x + 64, self.rect.y + 32))
        surface.blit(self.image, (self.rect.x, self.rect.y))
        if self.interaction:
            self.show_name.draw(surface, self.rect)

#bounce class which include mathematical functions for bounce movement
class Bounce:
    def __init__(self, x, y, limit, size):
        self.speed = random.uniform(0.5, 0.6)  # 0.5
        self.angle = random.randint(-10, 10) / 10  # random.choice([10, -10])
        self.drag = 0.999
        self.elasticity = random.uniform(0.75, 0.9)  # 0.75
        self.gravity = (math.pi, 0.002)
        self.limit = limit
        self.limits = [limit, 654]
        self.x, self.y = x, y
        self.size = size

    @staticmethod
    def add_vectors(angle1, length1, angle2, length2):
        x = math.sin(angle1) * length1 + math.sin(angle2) * length2
        y = math.cos(angle1) * length1 + math.cos(angle2) * length2
        angle = 0.5 * math.pi - math.atan2(y, x)
        length = math.hypot(x, y)
        return angle, length

    def move(self):
        self.angle, self.speed = self.add_vectors(self.angle, self.speed, *self.gravity)
        self.x += math.sin(self.angle) * self.speed
        self.y -= math.cos(self.angle) * self.speed
        self.speed *= self.drag

    def bounce(self):
        # if self.y > any(self.limits):
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
        self.speed = 0.5
        self.angle = random.choice([10, -10])
        self.drag = 0.999
        self.elasticity = 0.75