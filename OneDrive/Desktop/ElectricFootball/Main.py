import pygame
import time
import random
import player
pygame.font.init()

BALL_H, BALL_W= 10, 10
WIDTH, HEIGHT= 1200, 550
PLAYER_VEL= 5

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Electric Football")
BG= pygame.transform.scale(pygame.image.load("g558.jpg"), (WIDTH, HEIGHT))
FONT= pygame.font.SysFont("ariel", 60)

def draw(player, elapsed_time):
    WIN.blit(BG, (0, 0))

    time_text= FONT.render(f"Time: {round(elapsed_time)}s", 1, "white")
    WIN.blit(time_text, (10, 10))

    pygame.draw.rect(WIN, "blue", player)

    pygame.display.update()

def main():
    run = True

    player= pygame.Rect(200, HEIGHT-BALL_H, BALL_W, BALL_H)

    clock= pygame.time.Clock()

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

        if keys[pygame.K_LEFT] and player.x- PLAYER_VEL >= 0:
            player.x -= PLAYER_VEL
        if keys[pygame.K_RIGHT] and player.x + PLAYER_VEL+ player.width <= WIDTH:
            player.x += PLAYER_VEL
        if keys[pygame.K_DOWN] and player.y + PLAYER_VEL + player.height <= HEIGHT:
            player.y += PLAYER_VEL
        if keys[pygame.K_UP] and player.y- PLAYER_VEL >= 0:
            player.y -= PLAYER_VEL

        draw(player, elapsed_time)



    pygame.quit()

if __name__ == "__main__":
    main()