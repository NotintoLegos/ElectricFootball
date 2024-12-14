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

OFFENSE_COLOR= "blue"
DEFENSE_COLOR= "red"

# boolean for ball carrier
BALL_CARRIER= True
NOT_BALL_CARRIER= False



WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Electric Football")
BG= pygame.transform.scale(pygame.image.load("g558.jpg"), (WIDTH, HEIGHT))
FONT= pygame.font.SysFont("ariel", 60)

# making a dictionary
game_state= {
    "state": "new_drive", # in future change this to kickoff or start_menu
    "down_count": 1,
    "scrimmage_placement": 1000,
    "first_down_line": 900,
    "y_value": 300,
    "elapsed_time": 0
}


def draw(WIN, players, elapsed_time, lines):
    WIN.blit(BG, (0, 0))

    time_text= FONT.render(f"Time: {round(elapsed_time)}s", 1, "white")
    WIN.blit(time_text, (10, 10))

    for player in players:
        player.draw(WIN)
    
    for line in lines:
        line.draw_lines(WIN)

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

def update_FDL(lines, line_of_scrimmage):
    first_down_line= line_of_scrimmage - 100 # -------- add if statement before this for direction the offense travels for + or - 100px
    lines[1].x = first_down_line
    print(f"\nupdated FDL= {lines[1].x}")

def update_LOS(lines, scrimmage_placement):
    lines[0].x= scrimmage_placement
    print("\tupdate line of scrimmage at play_start_logic")

def find_ball_carrier(players):
    for player in players:
        if player.ball_carrier:
            return player
    return None

def collision_handler(ball_carrier, d_line, all_players):
    for defender in d_line:
        if ball_carrier.rect.colliderect(defender.rect):
            print("play_active:\n\tBall carrier tackled by defense!")
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
def new_drive_logic(WIN, lines):
    global SCRIMMAGE_PLACEMENT
    game_state["down_count"]= 1
    lines[0].x= game_state["scrimmage_placement"]
    lines[1].x= game_state["first_down_line"]
    print(f"LOS @ {lines[0].x}")
    print(f"First down line: {lines[1].x}\n")


    return "play_start"    

def set_of_downs_logic(lines):
    lines[1].rect.x= game_state["first_down_line"]
    print(f"\tFirst down line: {lines[1].rect.x}")

    game_state["down_count"] += 1
    print(f"\tdown: {game_state['down_count']}")
    
    if game_state["down_count"] > 4:
        print(f"\tLoss of downs")
        return "new_drive"
    return "play_start"

def play_start_logic(qb, o_line, d_line, lines):
    reset_position(qb, o_line, d_line, game_state["scrimmage_placement"], game_state["y_value"])
    print("play_start_logic:\n\treset position and starting the play")
    
    lines[0].rect.x= game_state["scrimmage_placement"]
    print(f"\tScrimmage placement at play start:{game_state['scrimmage_placement']}")

    print(f"\tStarting down:{game_state['down_count']}")

    return "play_active"

def play_active_logic(qb, o_line, d_line, lines, elapsed_time):
    ball_carrier= find_ball_carrier(qb+ o_line + d_line)
    for player in o_line:
        player.offensive_movement_linemen(VELOCITY_LINEMEN, WIDTH, HEIGHT, 0, 0)
    for player in d_line:
        player.defensive_movement_linemen(VELOCITY_LINEMEN, WIDTH, HEIGHT, 0, 0)
    for player in qb:
        player.qb_movement(VELOCITY_LINEMEN, WIDTH, HEIGHT, 0, 0)

    if ball_carrier:
        ball_carrier.color= "purple"
        keys= pygame.key.get_pressed()
        ball_carrier.move(keys, PLAYER_VEL, WIDTH, HEIGHT)
    
    tackle_pos= collision_handler(ball_carrier, d_line, qb+ o_line+ d_line)
    if tackle_pos:
        print(f"\ttackle_pos: \n\ttackle at {tackle_pos}")
        game_state["scrimmage_placement"] = tackle_pos[0]
        print(f"\tOn tackle. updating line to {lines[0].x}")
        return "play_end"

    draw(WIN, o_line + d_line + qb, elapsed_time, lines)
    return "play_active"

def play_end_logic():
    print(f"\nplay_end_logic")
    return "set_of_downs"
#-------------------------------------------------------------------------------------------

def main():
    clock= pygame.time.Clock()

# object creation, don't know if I should make a factory since its max of 22 players

    qb= [
        Player(0, 0, BALL_W, BALL_H, OFFENSE_COLOR, "offense", BALL_CARRIER)
    ]

    o_line = [
        Player(0, 0, BALL_W, BALL_H, OFFENSE_COLOR, "offense", NOT_BALL_CARRIER),
        Player(0, 0, BALL_W, BALL_H, OFFENSE_COLOR, "offense", NOT_BALL_CARRIER),
        Player(0, 0, BALL_W, BALL_H, OFFENSE_COLOR, "offense", NOT_BALL_CARRIER),
        Player(0, 0, BALL_W, BALL_H, OFFENSE_COLOR, "offense", NOT_BALL_CARRIER),
        Player(0, 0, BALL_W, BALL_H, OFFENSE_COLOR, "offense", NOT_BALL_CARRIER)
    ]
    
    d_line= [
        Player(0, 0, BALL_W, BALL_H, DEFENSE_COLOR, "defense", NOT_BALL_CARRIER),
        Player(0, 0, BALL_W, BALL_H, DEFENSE_COLOR, "defense", NOT_BALL_CARRIER),
        Player(0, 0, BALL_W, BALL_H, DEFENSE_COLOR, "defense", NOT_BALL_CARRIER)

    ]

    lines= [
        Lines(0, 0, SCRIMMAGE_WIDTH, SCRIMMAGE_HEIGHT, "blue"),
        Lines(0, 0, 3, SCRIMMAGE_HEIGHT, "yellow"),
        Lines(97, 0, 3, 550, "white"),
        Lines(1100, 0, 3, 550, "white")
    ]
    
    run = True
    game_state= "new_drive"

    start_time= time.time()
    elapsed_time= 0

    while run:
        
        elapsed_time= time.time() - start_time
        for event in pygame.event.get():
            if event.type== pygame.QUIT:
                run = False
                break

        if game_state== "new_drive":
            game_state= new_drive_logic(WIN, lines)

        elif game_state== "set_of_downs":
            game_state= set_of_downs_logic(lines)

        elif game_state== "play_start":
            game_state= play_start_logic(qb, o_line, d_line, lines)
        
        elif game_state== "play_active":
            game_state= play_active_logic(qb, o_line, d_line, lines, elapsed_time)
        
        elif game_state== "play_end":  # end drive will be used for turnover procedure
            game_state= play_end_logic()
        
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
