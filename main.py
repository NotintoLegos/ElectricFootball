import pygame
import time
import random
from player import Player
from lines import Lines

pygame.font.init()

BALL_H, BALL_W= 10, 10
WIDTH, HEIGHT= 1200, 550
PLAYER_VEL= 1
VELOCITY_LINEMEN= 1

SCRIMMAGE_WIDTH= 3
SCRIMMAGE_HEIGHT= HEIGHT
SCRIMMAGE_PLACEMENT= WIDTH

#testing at random location 550
# x value when tackled to set scrimmage placement
SCRIMMAGE_PLACEMENT= 550
FIRST_DOWN_DISTANCE= SCRIMMAGE_PLACEMENT-100

#to set players off the line slightly since line width is 3
DEFENSE_ON_LINE_SETUP= SCRIMMAGE_PLACEMENT - 12
OFFENSE_ON_LINE_SETUP= SCRIMMAGE_PLACEMENT + 5

# y value when tackle to decide start or ball placement, 300 set for testing
Y_VALUE= 300

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

# object creation, don't know if I should make a factory since its max of 22 players
    player1= Player(OFFENSE_ON_LINE_SETUP, Y_VALUE, BALL_W, BALL_H, "brown")
    player2= Player(DEFENSE_ON_LINE_SETUP, Y_VALUE, BALL_W, BALL_H, "teal")
    line_scrimmage= Lines(SCRIMMAGE_PLACEMENT, 0, SCRIMMAGE_WIDTH, SCRIMMAGE_HEIGHT, "blue")
    first_down_line= Lines(FIRST_DOWN_DISTANCE, 0, 3, 550, "yellow")
    goal_line_left= Lines(97, 0, 3, 550, "white")
    goal_line_right= Lines(1100, 0, 3, 550, "white")

    start_time= time.time()
    elapsed_time= 0

    while run:
        clock.tick(30)
        elapsed_time= time.time() - start_time

        for event in pygame.event.get():
            if event.type== pygame.QUIT:
                run = False
                break
                
#        keys= pygame.key.get_pressed()
        player1.offensive_movement_linemen(VELOCITY_LINEMEN, WIDTH, HEIGHT, OFFENSE_ON_LINE_SETUP, Y_VALUE)
        player2.defensive_movement_linemen(VELOCITY_LINEMEN, WIDTH, HEIGHT, DEFENSE_ON_LINE_SETUP, Y_VALUE)

        draw(WIN, [player1, player2], [line_scrimmage, first_down_line, goal_line_left, goal_line_right], elapsed_time)

    pygame.quit()

if __name__ == "__main__":
    main()
