import pygame
import time
import random
from player import Player
from lines import Lines

pygame.font.init()

BALL_H, BALL_W= 12, 12
WIDTH, HEIGHT= 1300, 650
WEST_ENDZONE, EAST_ENDZONE= 150, 1150

VELOCITY_LINEMEN= 1
VELOCTIY_MEDIUM= 2
VELOCITY_FAST= 3

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
    
def reset_ball_position(y_value):
    # keep ball placement within hash marks
    if y_value < 230:
        y_value= 230
    elif y_value > 410:
        y_value= 410

    # qb[0].rect.x= scrimmage_placement + 20
    # qb[0].rect.y = y_value

    # #offensive 
    # o_line[0].rect.x = scrimmage_placement + 5
    # o_line[0].rect.y = y_value

    # o_line[1].rect.x = scrimmage_placement + 5
    # o_line[1].rect.y = y_value + 20

    # o_line[2].rect.x = scrimmage_placement + 5
    # o_line[2].rect.y = y_value - 20

    # o_line[3].rect.x = scrimmage_placement + 5
    # o_line[3].rect.y = y_value + 40

    # o_line[4].rect.x = scrimmage_placement + 5
    # o_line[4].rect.y = y_value - 40

    # # defense
    # d_line[0].rect.x = scrimmage_placement - 12
    # d_line[0].rect.y = y_value

    # d_line[1].rect.x = scrimmage_placement - 12
    # d_line[1].rect.y = y_value + 20

    # d_line[2].rect.x = scrimmage_placement - 12
    # d_line[2].rect.y = y_value - 20

def offense_play_call(play_call, players, scrimmage_placement, y_value, direction):
    if play_call == 1:
        

def find_ball_carrier(players):
    for player in players:
        if player.ball_carrier:
            return player
    return None

def collision_handler(ball_carrier, all_players, lines):
    # for Out of Bounds logic
    for ob_line in lines[6:8]:
        if ball_carrier.rect.colliderect(ob_line.rect):
            print("play_active:\n\tOut of bounds")
            return ball_carrier.rect.x, ball_carrier.rect.y
        
    # TD logic for west endzone
    if ball_carrier.rect.colliderect(lines[2]):
        print("Touchdown!!!")
        return "new_drive"                                      # change to kickoff_logic or score_logic etc 

    # for tackling
    for defender in all_players[6:9]:                           # needs to change to "offense" or "defense" for Player.team when every player is added, 
        if ball_carrier.rect.colliderect(defender.rect):
            print("\tBall carrier tackled by defense!")
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

def new_drive_logic(lines):
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

def play_setup_logic(lines):

    reset_ball_position(game_state["y_value"])          
    lines[0].rect.x= game_state["scrimmage_placement"]

    # send to choose_play game_state

    keys= pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        print("\tspacebar press")
        return "play_active"
    return "play_start"

def play_active_logic(players, lines, elapsed_time):
    ball_carrier= find_ball_carrier(players)
    for player in players:
        player.all_movement(WIDTH, HEIGHT, 0, 0, Player.speed, Player.aim)

    if ball_carrier:                                                                            # keep for testing for now
        ball_carrier.color= "purple"
        keys= pygame.key.get_pressed()
        ball_carrier.move(keys, VELOCITY_FAST, WIDTH, HEIGHT)
    
    tackle_pos= collision_handler(ball_carrier, players, lines)
    if tackle_pos:
        print(f"\ttackle_pos: \n\ttackle at {tackle_pos}")
        game_state["scrimmage_placement"] = tackle_pos[0]
        game_state["y_value"]= tackle_pos[1]

        return "play_end"

    draw(WIN, players, elapsed_time, lines, game_state)
    return "play_active"

def play_end_logic():
    game_state["down_count"] += 1

    if game_state["scrimmage_placement"] < game_state["first_down_line"]:
        print(f"FDL: {game_state['scrimmage_placement'] - 100}\tWest endzone: {WEST_ENDZONE}")
        if game_state["scrimmage_placement"] - 100 < WEST_ENDZONE:
            game_state["first_down_line"]= WEST_ENDZONE
            print(f"Goal Line test: {game_state['first_down_line']}")
            return "new_drive"
        game_state["first_down_line"]= game_state["scrimmage_placement"] - 100
        return "new_drive"

    print(f"play_end_logic\n")
    return "set_of_downs"
#-------------------------------------------------------------------------------------------

def main():
    clock= pygame.time.Clock()

# object creation, don't know if I should make a factory since its max of 22 players

    player_build = [
        #---------------------------------team 1 on offense------------------------------------------------------------

        Player(0, 0, BALL_W, BALL_H, OFFENSE_COLOR, "offense", "qb", BALL_CARRIER, VELOCTIY_MEDIUM, "W"), # change to LB TE QB speed
        Player(0, 0, BALL_W, BALL_H, OFFENSE_COLOR, "offense", "rb", NOT_BALL_CARRIER, VELOCITY_FAST, "W"),
        Player(0, 0, BALL_W, BALL_H, OFFENSE_COLOR, "offense", "fb", NOT_BALL_CARRIER, VELOCTIY_MEDIUM, "W"),
        Player(0, 0, BALL_W, BALL_H, OFFENSE_COLOR, "offense", "te", NOT_BALL_CARRIER, VELOCTIY_MEDIUM, "W"),
        Player(0, 0, BALL_W, BALL_H, OFFENSE_COLOR, "offense", "wr1", NOT_BALL_CARRIER, VELOCITY_FAST, "W"),
        Player(0, 0, BALL_W, BALL_H, OFFENSE_COLOR, "offense", "wr2", NOT_BALL_CARRIER, VELOCITY_FAST, "W"),
        Player(0, 0, BALL_W, BALL_H, OFFENSE_COLOR, "offense", "center", NOT_BALL_CARRIER, VELOCITY_LINEMEN, "W"),
        Player(0, 0, BALL_W, BALL_H, OFFENSE_COLOR, "offense", "right_guard", NOT_BALL_CARRIER, VELOCITY_LINEMEN, "W"),
        Player(0, 0, BALL_W, BALL_H, OFFENSE_COLOR, "offense", "left_guard", NOT_BALL_CARRIER, VELOCITY_LINEMEN, "W"),
        Player(0, 0, BALL_W, BALL_H, OFFENSE_COLOR, "offense", "right_tackle", NOT_BALL_CARRIER, VELOCITY_LINEMEN, "W"),
        Player(0, 0, BALL_W, BALL_H, OFFENSE_COLOR, "offense", "left_tackle", NOT_BALL_CARRIER, VELOCITY_LINEMEN, "W"),

        #----------------------------------team 2 on defense-----------------------------------------------------------------

        Player(0, 0, BALL_W, BALL_H, DEFENSE_COLOR, "defense", "nose_tackle", NOT_BALL_CARRIER, VELOCITY_LINEMEN, "W"),
        Player(0, 0, BALL_W, BALL_H, DEFENSE_COLOR, "defense", "left_edge", NOT_BALL_CARRIER, VELOCITY_LINEMEN, "W"),
        Player(0, 0, BALL_W, BALL_H, DEFENSE_COLOR, "defense", "right_edge", NOT_BALL_CARRIER, VELOCITY_LINEMEN, "W"),
        Player(0, 0, BALL_W, BALL_H, DEFENSE_COLOR, "defense", "olb1", NOT_BALL_CARRIER, VELOCTIY_MEDIUM, "W"),
        Player(0, 0, BALL_W, BALL_H, DEFENSE_COLOR, "defense", "olb2", NOT_BALL_CARRIER, VELOCTIY_MEDIUM, "W"),
        Player(0, 0, BALL_W, BALL_H, DEFENSE_COLOR, "defense", "ilb1", NOT_BALL_CARRIER, VELOCTIY_MEDIUM, "W"),
        Player(0, 0, BALL_W, BALL_H, DEFENSE_COLOR, "defense", "ilb2", NOT_BALL_CARRIER, VELOCTIY_MEDIUM, "W"),
        Player(0, 0, BALL_W, BALL_H, DEFENSE_COLOR, "defense", "cb1", NOT_BALL_CARRIER, VELOCITY_FAST, "W"),
        Player(0, 0, BALL_W, BALL_H, DEFENSE_COLOR, "defense", "cb2", NOT_BALL_CARRIER, VELOCITY_FAST, "W"),
        Player(0, 0, BALL_W, BALL_H, DEFENSE_COLOR, "defense", "ss", NOT_BALL_CARRIER, VELOCITY_FAST, "W"),
        Player(0, 0, BALL_W, BALL_H, DEFENSE_COLOR, "defense", "fs", NOT_BALL_CARRIER, VELOCITY_FAST, "W")

    ]

    lines= [
        Lines(0, 50, SCRIMMAGE_WIDTH, SCRIMMAGE_HEIGHT, "blue"), 
        Lines(0, 50, 3, SCRIMMAGE_HEIGHT, "yellow"),
        Lines(149, 50, 1, 550, CLEAR_LINE_COLOR), # 2, goal line west, width and height is entire endzone area- for recievers catching ball in endzone
        Lines(1150, 50, 1, 550, CLEAR_LINE_COLOR), #east            
        Lines(50, 50, 1, 550, CLEAR_LINE_COLOR), # 4, back line of endzone west, line is wide, from edge of screen to where endzone is, for catching out of endzone
        Lines(1250, 50, 1, 550, CLEAR_LINE_COLOR), # east                       
        Lines(50, 49, 1300, 1, CLEAR_LINE_COLOR), # 6, south sideline    
        Lines(50, 600, 1300, 1, CLEAR_LINE_COLOR) # north
        
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
            game_state= new_drive_logic(lines)

        elif game_state== "set_of_downs":
            game_state= set_of_downs_logic(lines)

        elif game_state== "play_start":
            draw(WIN, player_build, elapsed_time, lines, game_state)  # draws current state of game, so not blank screen
            game_state= play_setup_logic(lines)
        
        elif game_state== "play_active":
            game_state= play_active_logic(player_build, lines, elapsed_time)
        
        elif game_state== "play_end":  # end drive will be used for turnover procedure
            game_state= play_end_logic()
        
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
