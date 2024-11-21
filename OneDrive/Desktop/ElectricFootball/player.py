import pygame

class Player:

    PLAYER_DIMENTIONS= 25

    TEST_LOCATION= 200


    def player_maker():
        player1= pygame.Rect(
            Player.TEST_LOCATION, 
            Player.TEST_LOCATION, 
            Player.PLAYER_DIMENTIONS, 
            Player.PLAYER_DIMENTIONS
            )
    def drawPlayer(player1):
        pygame.draw.rect()