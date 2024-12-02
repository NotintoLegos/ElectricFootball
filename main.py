import pygame
import time
import random
from player import Player
from lines import Lines

pygame.font.init()

BALL_H, BALL_W= 12, 12
WIDTH, HEIGHT= 1200, 550
PLAYER_VEL= 2
VELOCITY_LINEMEN= 1

SCRIMMAGE_WIDTH= 3
SCRIMMAGE_HEIGHT= HEIGHT
SCRIMMAGE_PLACEMENT= WIDTH

OFFENSE_COLOR= "blue"
DEFENSE_COLOR= "red"

# boolean for ball carrier
BALL_CARRIER= True
NOT_BALL_CARRIER= False

#testing at random location 550
# x value when tackled to set scrimmage placement
SCRIMMAGE_PLACEMENT= 550
FIRST_DOWN_DISTANCE= SCRIMMAGE_PLACEMENT-100

#to set players off the line slightly since line width is 3
DEFENSE_ON_LINE_SETUP= SCRIMMAGE_PLACEMENT - 12
OFFENSE_ON_LINE_SETUP= SCRIMMAGE_PLACEMENT + 5
QB_SETUP= SCRIMMAGE_PLACEMENT + 20

# y value when tackle to decide start or ball placement, 300 set for testing
Y_VALUE= 300
GUARD_SET_TOP= Y_VALUE + 20
GUARD_SET_BOTTOM= Y_VALUE - 20
TACKLE_SET_TOP= GUARD_SET_TOP + 20
TACKLE_SET_BOTTOM= GUARD_SET_BOTTOM - 20

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

def reset_position(qb, o_line, d_line, scrimmage_placement, y_value):
    qb[0].rect.x= scrimmage_placement + 20
    qb[0].rect.y = y_value

    #offensive 
    o_line[0].rect.x = scrimmage_placement + 5
    o_line[0].rect.y = y_value

    o_line[1].rect.x = scrimmage_placement + 5
    o_line[1].rect.y = y_value + 20

    o_line[2].rect.x = scrimmage_placement + 5
    o_line[2].rect.y = y_value - 20

    o_line[3].rect.x = scrimmage_placement + 5
    o_line[3].rect.y = y_value + 40

    o_line[4].rect.x = scrimmage_placement + 5
    o_line[4].rect.y = y_value - 40

    # defense
    d_line[0].rect.x = scrimmage_placement - 12
    d_line[0].rect.y = y_value

    d_line[1].rect.x = scrimmage_placement - 12
    d_line[1].rect.y = y_value + 20

    d_line[2].rect.x = scrimmage_placement - 12
    d_line[2].rect.y = y_value - 20

def find_ball_carrier(players):
    for player in players:
        if player.ball_carrier:
            return player
    return None

def next_down(down):
    return down + 1

def collision_handler(down, ball_carrier, d_line, o_line, all_players):
    for defender in d_line:
        if ball_carrier.rect.colliderect(defender.rect):
            next_down(down)
            print("Ball carrier tackled by defense!")
            print("Down: {down}")
            return ball_carrier.rect.x, ball_carrier.rect.y
    
    for player in all_players:
        if player != ball_carrier:
            for other_player in all_players:
                if player != other_player and player.rect.colliderect(other_player.rect):
                    if player.rect.x < other_player.rect.x:
                        player.rect.x -= 1
                    else:
                        player.rect.x += 1
                    if player.rect.y < other_player.rect.y:
                        player.rect.y -= 1
                    else:
                        player.rect.y += 1

    return "no_collision", None


#-------------------------------------------------------------------------------------------

def main():
    global SCRIMMAGE_PLACEMENT
    run = True
    clock= pygame.time.Clock()

    down_count= 1    

# object creation, don't know if I should make a factory since its max of 22 players

    qb= [
        Player(QB_SETUP, Y_VALUE, BALL_W, BALL_H, OFFENSE_COLOR, "offense", BALL_CARRIER)
    ]

    o_line = [
        Player(OFFENSE_ON_LINE_SETUP, Y_VALUE, BALL_W, BALL_H, OFFENSE_COLOR, "offense", NOT_BALL_CARRIER),
        Player(OFFENSE_ON_LINE_SETUP, GUARD_SET_TOP, BALL_W, BALL_H, OFFENSE_COLOR, "offense", NOT_BALL_CARRIER),
        Player(OFFENSE_ON_LINE_SETUP, GUARD_SET_BOTTOM, BALL_W, BALL_H, OFFENSE_COLOR, "offense", NOT_BALL_CARRIER),
        Player(OFFENSE_ON_LINE_SETUP, TACKLE_SET_TOP, BALL_W, BALL_H, OFFENSE_COLOR, "offense", NOT_BALL_CARRIER),
        Player(OFFENSE_ON_LINE_SETUP, TACKLE_SET_BOTTOM, BALL_W, BALL_H, OFFENSE_COLOR, "offense", NOT_BALL_CARRIER)
    ]
    
    d_line= [
        Player(DEFENSE_ON_LINE_SETUP, Y_VALUE, BALL_W, BALL_H, DEFENSE_COLOR, "defense", NOT_BALL_CARRIER),
        Player(DEFENSE_ON_LINE_SETUP, GUARD_SET_TOP, BALL_W, BALL_H, DEFENSE_COLOR, "defense", NOT_BALL_CARRIER),
        Player(DEFENSE_ON_LINE_SETUP, GUARD_SET_BOTTOM, BALL_W, BALL_H, DEFENSE_COLOR, "defense", NOT_BALL_CARRIER)

    ]

    lines= [
        Lines(SCRIMMAGE_PLACEMENT, 0, SCRIMMAGE_WIDTH, SCRIMMAGE_HEIGHT, "blue"),
        Lines(FIRST_DOWN_DISTANCE, 0, 3, 550, "yellow"),
        Lines(97, 0, 3, 550, "white"),
        Lines(1100, 0, 3, 550, "white")
    ]
    

    start_time= time.time()
    elapsed_time= 0

    while run:
        clock.tick(30)
        elapsed_time= time.time() - start_time

        for event in pygame.event.get():
            if event.type== pygame.QUIT:
                run = False
                break
        
        ball_carrier= find_ball_carrier(qb + o_line + d_line) # needs to go>> within single_play loop, only qb rn, need to add more ball carrier types, wr & rb
        
        keys= pygame.key.get_pressed()      # user control of qb for testing purposes
                # Ball carrier movement (controlled by keys)
        if ball_carrier:
            ball_carrier.color= "purple"
            ball_carrier.move(keys, PLAYER_VEL, WIDTH, HEIGHT)
        


        draw(WIN, o_line + d_line + qb, lines, elapsed_time)

    pygame.quit()

if __name__ == "__main__":
    main()
