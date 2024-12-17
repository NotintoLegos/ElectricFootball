import pygame
import random


class Player:

    def __init__(self, x, y, width, height, color, team, ball_carrier=False):
        self.rect= pygame.Rect(x, y, width, height)
        self.color= color
        self.original_color= color
        self.team= team
        self.ball_carrier= ball_carrier

    def draw(self, window):
        pygame.draw.rect(window, self.color, self.rect)

    def move(self, keys, player_vel, width, height):
        if keys[pygame.K_LEFT] and self.rect.x - player_vel >=0:
            self.rect.x -= player_vel
        if keys[pygame.K_RIGHT] and self.rect.x + player_vel + self.rect.width <= width:
            self.rect.x += player_vel
        if keys[pygame.K_DOWN] and self.rect.y + player_vel + self.rect.height <= height:
            self.rect.y += player_vel
        if keys[pygame.K_UP] and self.rect.y - player_vel >=0:
            self.rect.y -= player_vel

#defense movements, linemen, DBs, linebackers
    def defensive_movement_linemen(self, slow_velocity, width, height, dx, dy):
        directions= [(0, 0), (-slow_velocity, 0), (0, slow_velocity), (0, -slow_velocity)]           # testing going backward for first down line
        dx, dy= random.choice(directions)
        self.rect.x += dx
        self.rect.y += dy

        self.rect.x = max(0, min(self.rect.x, width - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, height - self.rect.height))


            
#offense movements
    def offensive_movement_linemen(self, slow_velocity, width, height, dx, dy):
        directions= [(0, 0), (-slow_velocity, 0), (0, slow_velocity), (0, -slow_velocity)]
        dx, dy= random.choice(directions)
        self.rect.x += dx
        self.rect.y += dy

        self.rect.x = max(0, min(self.rect.x, width - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, height - self.rect.height))

# qb is first ball carrier by default
    def qb_movement(self, slow_velocity, width, height, dx, dy):
        directions= [(slow_velocity, 0), (-slow_velocity, 0), (0, slow_velocity), (0, -slow_velocity)]
        dx, dy= random.choice(directions)
        self.rect.x += dx
        self.rect.y += dy
        
        self.rect.x = max(0, min(self.rect.x, width - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, height - self.rect.height))
