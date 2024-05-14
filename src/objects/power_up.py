import pygame
from .object import Object
import random

#buff into stats 
class PowerUp(Object):
    type = 'flask'
    size = (64, 64)

    def __init__(self, game, room, name, position=None):
        self.name = name
        self.position = [644, 400]
        if position is not None:
            self.position = position
        Object.__init__(self, game, self.name, self.type, self.size, room, self.position)
        self.interaction = False
        self.counter = 0
        self.elevated = False
        self.particles = []
    #load image
    def load_image(self):
        image = pygame.image.load(f'./assets/objects/power_ups/{self.name}/{self.name}.png').convert_alpha()
        image = pygame.transform.scale(image, self.size)
        self.image = image
    #check player on top of object 
    def detect_collision(self):
        if self.game.player.rect.colliderect(self.rect):
            self.image = pygame.image.load(
                f'./assets/objects/power_ups/{self.name}/{self.name}_picked.png').convert_alpha()
            self.interaction = True
        else:
            self.image = pygame.image.load(f'./assets/objects/power_ups/{self.name}/{self.name}.png').convert_alpha()
            self.interaction = False
            self.show_name.reset_line_length()
    #apply buff
    def interact(self):
        pass
    #update functions
    def update(self):
        self.hovering.hovering()
        self.show_price.update()
        self.update_hitbox()
        self.update_bounce()
    #draw functions
    def draw(self):
        surface = self.room.tile_map.map_surface
        surface.blit(self.image, (self.rect.x, self.rect.y))
        self.beautify(surface)
        if self.interaction:
            self.show_name.draw(surface, self.rect)
        self.show_price.draw(surface)

    def beautify(self, surface):
        pass


class AttackPowerUp(PowerUp):
    name = 'attack'

    def __init__(self, game, room, position=None):
        super().__init__(game, room, self.name, position)
        self.value = 250
    #increase player attack damage
    def interact(self):
        self.game.player.strength *= 1.1
        self.room.objects.remove(self)

    def beautify(self, surface):
        if random.randint(1, 20) == 1:
            x = random.randint(self.rect.midtop[0] - 30, self.rect.midtop[0] + 30)
            y = random.randint(self.rect.midtop[1] - 30, self.rect.midtop[1] + 30)


class ShieldPowerUp(PowerUp):
    name = 'armor'

    def __init__(self, game, room, position=None):
        super().__init__(game, room, self.name, position)
        self.value = 150
    #increase player shield
    def interact(self):
        self.game.player.shield += 1
        self.room.objects.remove(self)

    def beautify(self, surface):
        if random.randint(1, 10) == 1:
            x = random.randint(self.hitbox.midtop[0] - 10, self.rect.midtop[0] + 10)
            y = random.randint(self.hitbox.midtop[1] - 10, self.rect.midtop[1] + 10)
