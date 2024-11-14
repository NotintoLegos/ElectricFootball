import pygame
import time
import random

BALL_H, BALL_W= 20, 20
WIDTH, HEIGHT= 1200, 550
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Electric Football")

BG= pygame.transform.scale(pygame.image.load("g558.jpg"), (WIDTH, HEIGHT))



def draw():
    WIN.blit(BG, (0, 0))
    pygame.display.update()

def main():
    run = True
    while run:
        for event in pygame.event.get():
            if event.type== pygame.QUIT:
                run = False
                break

        draw()

    pygame.quit()

if __name__ == "__main__":
    main()