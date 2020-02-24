import pygame 
from network import Network
from player import Player

WIDTH = 500
HEIGHT = 500

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Client")

def main():
    network = Network()
    p1 = network.get_player()
    clock = pygame.time.Clock()
    running = True
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()

        p2 = network.send(p1)
        p1.move()
        redraw_window(window, p1, p2)

def redraw_window(window, p1, p2):
    window.fill((255, 255, 255))
    p1.draw(window)
    p2.draw(window)
    pygame.display.update() 
        
if __name__ == "__main__":
    main()