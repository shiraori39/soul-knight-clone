import pygame

# Design a base button class to use inheritance
class Button:
    def __init__(self, menu, x, y, name):
        self.name = name
        self.menu = menu
        self.images = []
        self.path = './assets/misc/buttons'
        self.load_images()
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.midtop = (x, y)
        self.clicked = False
        self.played = False
    #Load image of the button
    def load_images(self):
        self.images.append(pygame.image.load(f'{self.path}/{self.name}1.png').convert_alpha())
        self.images.append(pygame.image.load(f'{self.path}/{self.name}2.png').convert_alpha())
    
    #Function to do "things" if clicked
    def detect_action(self, pos):
        pass
    
    #check if hovered
    def update(self):
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            self.image = self.images[1]
        else:
            self.image = self.images[0]
            self.played = False
        #check if clicked
        self.detect_action(pos)

    #draw function
    def draw(self, surface):
        surface.blit(self.image, self.rect)

#Create PlayButton and ExitButton inherited from the button class
class PlayButton(Button):
    def __init__(self, menu, x, y):
        super().__init__(menu, x, y, 'play')
    #If clicked play button then close the menu and start the game
    def detect_action(self, pos):
        if self.rect.collidepoint(pos) and pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
            self.menu.running = False
            self.menu.game.running = True
            self.clicked = True

class ExitButton(Button):
    def __init__(self, menu, x, y):
        super().__init__(menu, x, y, 'exit')
    #if clicked exit button then exit the game
    def detect_action(self, pos):
        if self.rect.collidepoint(pos) and pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
            self.menu.game.running = False
            self.menu.running = False
            self.clicked = True

#Main menu class
class MainMenu:
    def __init__(self, game):
        self.game = game
        self.running = True
        self.play_button = PlayButton(self, 21 * 64 / 2, 8 * 64 / 2)
        self.exit_button = ExitButton(self, 21 * 64 / 2, 7 * 64 / 2 + 240)
    #Input actions from keyboard or mouse
    def input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_ESCAPE]:
            self.game.running = False
    #Check if pressed any buttons
    def update(self):
        self.play_button.update()
        self.exit_button.update()
    #Draw the menu
    def draw(self):
        self.game.screen.fill((0, 0, 0))
        self.play_button.draw(self.game.screen)
        self.exit_button.draw(self.game.screen)
    #Run the menu
    def show(self):
        while self.running:
            self.input()
            self.update()
            self.draw()
            self.play_button.detect_action(pygame.mouse.get_pos())
            self.game.clock.tick(self.game.fps)
            self.game.display.blit(self.game.screen, (0, 0))
            pygame.display.flip()
