import pygame
import time
import random
from player import Player
from lines import Lines

pygame.font.init()

BALL_H, BALL_W= 12, 12
WIDTH, HEIGHT= 1300, 650
PLAYER_VEL= 2
VELOCITY_LINEMEN= 1

SCRIMMAGE_WIDTH= 3
SCRIMMAGE_HEIGHT= HEIGHT - 100

OFFENSE_COLOR= "blue"
DEFENSE_COLOR= "red"
CLEAR_LINE_COLOR= (255, 255, 255, 0)

# boolean for ball carrier
BALL_CARRIER= True
NOT_BALL_CARRIER= False

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Electric Football")
BG= pygame.transform.scale(pygame.image.load("Notre_Dame_Field.png"), (WIDTH, HEIGHT))
FONT= pygame.font.SysFont("ariel", 60)

# dictionary
game_state= {
    "state": "new_drive", # in future change this to kickoff or start_menu
    "down_count": 1,
    "scrimmage_placement": 1000,
    "first_down_line": 900,
    "y_value": 321,
    "elapsed_time": 0
}

def draw(WIN, players, elapsed_time, lines, game_state):
    WIN.blit(BG, (0, 0))

    time_text= FONT.render(f"Time: {round(elapsed_time)}s", 1, "white")
    WIN.blit(time_text, (10, 10))

    for player in players:
        player.draw(WIN)
    
    for line in lines:
        line.draw_lines(WIN)

    if game_state == "play_start":
        start_text = FONT.render("Press SPACE to start play", 1, "yellow")
        WIN.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2))

    pygame.display.update()    
    
def reset_position(qb, o_line, d_line, scrimmage_placement, y_value):

    if y_value < 230:
        y_value= 230
    elif y_value > 410:
        y_value= 410

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

#def ob_handler(ball_carrier, lines):
 #   if ball_carrier.rect.colide_rect():

  #  return None

# -----------each play state logic-------------------
def new_drive_logic(WIN, lines):
    global SCRIMMAGE_PLACEMENT

    lines[0].x= game_state["scrimmage_placement"]
    lines[1].x= game_state["first_down_line"]
    print(f"LOS @ {lines[0].x}")
    print(f"First down line: {lines[1].x}\n")

    game_state["down_count"]= 1

    return "set_of_downs"    

def set_of_downs_logic(lines):
    print("set_of_downs_logic")

    lines[1].rect.x= game_state["first_down_line"]
    print(f"\tFirst down line: {lines[1].rect.x}")

    print(f"\tdown: {game_state['down_count']}")
    
    if game_state["down_count"] > 4:
        print(f"\tLoss of downs")
        return "new_drive"
    return "play_start"

def play_start_logic(qb, o_line, d_line, lines):
    reset_position(qb, o_line, d_line, game_state["scrimmage_placement"], game_state["y_value"])  
    lines[0].rect.x= game_state["scrimmage_placement"]

    keys= pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        print("\tspacebar press")
        return "play_active"
    return "play_start"

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
        game_state["y_value"]= tackle_pos[1]

        return "play_end"

    draw(WIN, o_line + d_line + qb, elapsed_time, lines, game_state)
    return "play_active"

def play_end_logic():
    game_state["down_count"] += 1

    if game_state["scrimmage_placement"] < game_state["first_down_line"]:
        game_state["first_down_line"]= game_state["scrimmage_placement"] - 100
        return "new_drive"
        
    print(f"play_end_logic\n")
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
        Lines(0, 50, SCRIMMAGE_WIDTH, SCRIMMAGE_HEIGHT, "blue"),
        Lines(0, 50, 3, SCRIMMAGE_HEIGHT, "yellow"),
        Lines(149, 50, 1, 550, CLEAR_LINE_COLOR), #goal line west     good
        Lines(1150, 50, 1, 550, CLEAR_LINE_COLOR), #east            good
        Lines(49, 50, 1, 550, CLEAR_LINE_COLOR), # back line of endzone west      find
        Lines(1250, 50, 1, 550, CLEAR_LINE_COLOR), # east                       
        Lines(50, 50, 1200, 1, CLEAR_LINE_COLOR), #south sideline     good
        Lines(50, 600, 1200, 1, CLEAR_LINE_COLOR) # north
        
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
            draw(WIN, o_line + d_line + qb, elapsed_time, lines, game_state)  # draws current state of game, so not blank screen
            game_state= play_start_logic(qb, o_line, d_line, lines)
        
        elif game_state== "play_active":
            game_state= play_active_logic(qb, o_line, d_line, lines, elapsed_time)
        
        elif game_state== "play_end":  # end drive will be used for turnover procedure
            game_state= play_end_logic()
        
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
