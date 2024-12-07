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
SCRIMMAGE_PLACEMENT= 1200

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

def update_lines(lines, scrimmage_placement):
    lines[0].x= scrimmage_placement
    first_down_distance= scrimmage_placement- 100
    lines[1].x = first_down_distance
    print(f"updated scrimmage line= {lines[0].x} FD= {lines[1].x}")

def update_LOS(lines, scrimmage_placement):
    lines[0].x= scrimmage_placement
    print("only updating line of scrimmage after tackle")

def find_ball_carrier(players):
    for player in players:
        if player.ball_carrier:
            return player
    return None

def next_down(down):
    return down + 1

def collision_handler(down, ball_carrier, d_line, all_players):
    for defender in d_line:
        if ball_carrier.rect.colliderect(defender.rect):
            next_down(down)
            print("Ball carrier tackled by defense!")
            print(f"Down: {down}")
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

    return None

# -----------each play state logic-------------------
def new_drive_logic(qb, o_line, d_line, lines):
    global SCRIMMAGE_PLACEMENT
    lines[0].x= SCRIMMAGE_PLACEMENT
    lines[1].x= SCRIMMAGE_PLACEMENT - 100
    print(f"LOS @ {lines[0].x}")
    print(f"First down line: {lines[1].x}")
    reset_position(qb, o_line, d_line, SCRIMMAGE_PLACEMENT, Y_VALUE)
    return "play_start"    

def play_start_logic(qb, o_line, d_line, elapsed_time, lines):
    reset_position(qb, o_line, d_line, SCRIMMAGE_PLACEMENT, Y_VALUE)
    print("reset position and starting the play")
    return "play_active"

def play_active_logic(qb, o_line, d_line, lines, elapsed_time, down_count):
    global SCRIMMAGE_PLACEMENT
    ball_carrier= find_ball_carrier(qb+ o_line + d_line)
    for player in o_line:
        player.offensive_movement_linemen(VELOCITY_LINEMEN, WIDTH, HEIGHT, 0, 0)
    for player in d_line:
        player.defensive_movement_linemen(VELOCITY_LINEMEN, WIDTH, HEIGHT, 0, 0)

    if ball_carrier:
        ball_carrier.color= "purple"
        keys= pygame.key.get_pressed()
        ball_carrier.move(keys, PLAYER_VEL, WIDTH, HEIGHT)
    
    tackle_pos= collision_handler(down_count, ball_carrier, d_line, qb+ o_line+ d_line)
    if tackle_pos:
        print(f"tackle_pos: tackle at {tackle_pos}")
        SCRIMMAGE_PLACEMENT= tackle_pos[0]
        update_LOS(lines, SCRIMMAGE_PLACEMENT)
        print(f"On tackle. updating line to {lines[0].x}")
        next_down(down_count)
        return "play_end"

    draw(WIN, o_line + d_line + qb, lines, elapsed_time)
    return "play_active"

def play_end_logic(down_count):
    if down_count >= 4:
        print(f"Loss of downs")
        return "new_drive"
    print(f"play ended. get ready for next play")
    return "play_start"
#-------------------------------------------------------------------------------------------

def main():
    clock= pygame.time.Clock()
    SCRIMMAGE_PLACEMENT= 300

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
        Lines(FIRST_DOWN_DISTANCE, 0, 3, SCRIMMAGE_HEIGHT, "yellow"),
        Lines(97, 0, 3, 550, "white"),
        Lines(1100, 0, 3, 550, "white")
    ]
    
    run = True
    game_state= "new_drive"
    down_count= 1



    start_time= time.time()
    elapsed_time= 0

    while run:
        
        elapsed_time= time.time() - start_time
        for event in pygame.event.get():
            if event.type== pygame.QUIT:
                run = False
                break

        if game_state== "new_drive":
            game_state= new_drive_logic(qb, o_line, d_line, lines)

        elif game_state== "play_start":
            game_state= play_start_logic(qb, o_line, d_line, elapsed_time, lines)
        
        elif game_state== "play_active":
            game_state= play_active_logic(qb, o_line, d_line, lines, elapsed_time, down_count)
        
        elif game_state== "play_end":  # end drive will be used for turnover procedure
            game_state= play_end_logic(down_count)
        
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
