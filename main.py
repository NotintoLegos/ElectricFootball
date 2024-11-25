import pygame
import time
import random
from player import Player

pygame.font.init()

BALL_H, BALL_W= 10, 10
WIDTH, HEIGHT= 1200, 550
PLAYER_VEL= 2

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Electric Football")
BG= pygame.transform.scale(pygame.image.load("g558.jpg"), (WIDTH, HEIGHT))
FONT= pygame.font.SysFont("ariel", 60)

def draw(WIN, players, elapsed_time):
    WIN.blit(BG, (0, 0))

    time_text= FONT.render(f"Time: {round(elapsed_time)}s", 1, "white")
    WIN.blit(time_text, (10, 10))

    for player in players:
        player.draw(WIN)

    pygame.display.update()    

def main():
    run = True
    clock= pygame.time.Clock()

    player1= Player(200, HEIGHT-BALL_H, BALL_W, BALL_H, "blue")
    #ball_carrier= Player(300, HEIGHT-BALL_H, BALL_W, BALL_H, "brown")

    start_time= time.time()
    elapsed_time= 0

    while run:
        clock.tick(60)
        elapsed_time= time.time() - start_time

        for event in pygame.event.get():
            if event.type== pygame.QUIT:
                run = False
                break
                
        keys= pygame.key.get_pressed()
        player1.move(keys, PLAYER_VEL, WIDTH, HEIGHT)

        draw(WIN, [player1], elapsed_time)
        #ball_carrier.move_randomly()

    pygame.quit()

if __name__ == "__main__":
    main()
