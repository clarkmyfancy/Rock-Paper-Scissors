import pickle
import pygame 
from button import Button
from network import Network


pygame.font.init()

WIDTH = HEIGHT = 700
window = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Client")

buttons = [
    Button("Rock", 50, 500, (0,0,0)),
    Button("Paper", 250,  500, (255,0,0)),
    Button("Scissors", 450, 500, (0, 255, 0))
]

def main():
    running = True
    clock = pygame.time.Clock()
    network = Network()
    player = int(network.get_player())
    print("You are player", player)

    while running:
        clock.tick(60)
        try:
            game = network.send("get")
        except:
            print("Couldn'g get game")
            break 

        if game.both_players_went():
            redraw_window(window, game, player)
            pygame.time.delay(200)
            try:
                game = network.send("reset")
            except:
                running = True
                print("Couldn't get game")
                break

            font = pygame.font.SysFont("comicsans", 90)
            if (game.winner() == 1 and player == 1) or (game.winner() == 0 and player == 0):
                text = font.render("You WON!", 1, (255, 0, 255))
            elif game.winner() == -1:
                text = font.render("It was a Tie", 1, (255, 0, 0))
            else: 
                text = font.render("You LOST!", 1, (176, 124, 24))
            window.blit(text, (WIDTH/2 - text.get_width()/2, HEIGHT/2 - text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(2000)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                position = pygame.mouse.get_pos()
                for button in buttons:
                    if button.click(position) and game.connected():
                        if player == 0:
                            if not game.p1_has_played:
                                network.send(button.text)
                        else:
                            if not game.p2_has_played:
                                network.send(button.text)

        redraw_window(window, game, player)
 
def redraw_window(window, game, player):
    window.fill((128, 128, 128))
    
    if not game.connected():
        font = pygame.font.SysFont("comicsans", 80)
        text = font.render("Waiting for Player...", 1, (255, 0, 0), True)
        window.blit(text, (int(WIDTH/2 - text.get_width()/2), int(HEIGHT/2 - text.get_height()/2)))
    else:
        font = pygame.font.SysFont("comicsans", 60)
        text = font.render("Your Move", 1, (0, 255, 255))
        window.blit(text, (80, 200))

        text = font.render("Opponent's", 1, (0, 255, 255))
        window.blit(text, (380, 200))

        move1 = game.get_player_move(0)
        move2 = game.get_player_move(1)
        if game.both_players_went():
            text1 = font.render(move1, 1, (0,0,0))
            text2 = font.render(move2, 1, (0,0,0))
        else:
            if game.p1_has_played and player == 0:
                text1 = font.render(move1, 1, (0,0,0))
            elif game.p1_has_played:
                text1 = font.render("Locked In", 1, (0,0,0))
            else:
                text1 = font.render("Waiting...", 1, (0,0,0))

            if game.p2_has_played and player == 1:
                text2 = font.render(move2, 1, (0,0,0))
            elif game.p2_has_played:
                text2 = font.render("Locked In", 1, (0,0,0))
            else:
                text2 = font.render("Waiting...", 1, (0,0,0))
                
        if player == 1:
            window.blit(text2, (100, 350))
            window.blit(text1, (400, 350))
        else:
            window.blit(text1, (100, 350))
            window.blit(text2, (400, 350))

        for button in buttons:
            button.draw(window)
if __name__ == "__main__":
    main()