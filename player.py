import pygame 

class Player(): 
    def __init__(self, position, width, height, color):
        self.x = position[0]
        self.y = position[1]
        self.width = width 
        self.height = height 
        self.color = color
        self.rect = (self.x, self.y, width, height)
        self.x_velocity = 3
        self.y_velocity = 3

    def draw(self, window):
        pygame.draw.rect(window, self.color, self.rect)

    def move(self):
        keys = pygame.key.get_pressed()
        self.handle_key_presses(keys)
        self.update()

    def handle_key_presses(self, keys):
        if keys[pygame.K_LEFT]:
            self.x -= self.x_velocity
        if keys[pygame.K_RIGHT]:
            self.x += self.x_velocity
        if keys[pygame.K_UP]:
            self.y -= self.y_velocity
        if keys[pygame.K_DOWN]:
            self.y += self.y_velocity
        if keys[pygame.K_SPACE]:
            self.y = 0
            self.x = 0

    def update(self):
        self.rect = (self.x, self.y, self.width, self.height)