# Electric Football Game

game states:
    start_menu_logic:
    coin_flip_logic:
    kickoff_logic:
    new_drive_logic:
    play_start_logic:
        choose play type:
            -if play: 
                reset positions
                set player start directions
                declare RUN or PASS, draw these as buttons on screen
                    if RUN
                        ball_carrier = RB
                go to "play_active_logic"
            -if field goal -> "field_goal_logic"

    play_active_logic:
        -tackling
        -out of bounds
        -first down
        -score
    field_goal_logic:
        -kick is good
        -kick is bad
