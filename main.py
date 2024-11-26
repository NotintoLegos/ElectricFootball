import pygame
import time
import random
from player import Player
from lines import Lines

pygame.font.init()

BALL_H, BALL_W= 10, 10
WIDTH, HEIGHT= 1200, 550
PLAYER_VEL= 2

SCRIMMAGE_WIDTH= 3
SCRIMMAGE_HEIGHT= HEIGHT
SCRIMMAGE_PLACEMENT= WIDTH

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Electric Football")
BG= pygame.transform.scale(pygame.image.load("g558.jpg"), (WIDTH, HEIGHT))
FONT= pygame.font.SysFont("ariel", 60)

def draw(WIN, players, lines, elapsed_time):
    WIN.blit(BG, (0, 0))

    time_text= FONT.render(f"Time: {round(elapsed_time)}s", 1, "white")
    WIN.blit(time_text, (10, 10))

    for player in players:
        player.draw(WIN)

    for line in lines:
        line.draw(WIN)

    pygame.display.update()    

def main():
    run = True
    clock= pygame.time.Clock()

#testing at random location 550
# x value when tackled to set scrimmage placement
    SCRIMMAGE_PLACEMENT= 550
    first_down_distance= SCRIMMAGE_PLACEMENT-100
#to set players off the line slightly since line width is 3
    defense_on_line_setup= SCRIMMAGE_PLACEMENT - 12
    offense_on_line_setup= SCRIMMAGE_PLACEMENT + 5

# y value when tackle to decide start or ball placement, 300 set for testing
    y_value= 300

# object creation, don't know if I should make a factory since its max of 22 players
    player1= Player(offense_on_line_setup, y_value, BALL_W, BALL_H, "brown")
    player2= Player(defense_on_line_setup, y_value, BALL_W, BALL_H, "teal")
    line_scrimmage= Lines(SCRIMMAGE_PLACEMENT, 0, SCRIMMAGE_WIDTH, SCRIMMAGE_HEIGHT, "blue")
    first_down_line= Lines(first_down_distance, 0, 3, 550, "yellow")
    goal_line_left= Lines(97, 0, 3, 550, "white")
    goal_line_right= Lines(1100, 0, 3, 550, "white")

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

        draw(WIN, [player1, player2], [line_scrimmage, first_down_line, goal_line_left, goal_line_right], elapsed_time)

    pygame.quit()

if __name__ == "__main__":
    main()
