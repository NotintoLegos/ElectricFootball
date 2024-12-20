import pygame
import random


class Player:
    
    def __init__(self, x, y, width, height, color, team, position, ball_carrier, speed, aim):
        self.rect= pygame.Rect(x, y, width, height)
        self.color= color
        self.original_color= color
        self.team= team
        self.position= position
        self.ball_carrier= ball_carrier
        self.speed= speed
        self.aim= aim

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


    def all_movement(self, width, height, dx, dy, speed, direction):
        if direction== "STAY":
            [(-speed, 0), (speed, 0), (0, speed), (0, -speed)]
        elif direction== "W":
            [(0, 0), (speed, 0), (0, speed), (0, -speed)]
        elif direction== "NW":
            [(0, 0), (speed, 0), (0, speed), (0, -speed)]
        elif direction== "N":
            [(0, 0), (speed, 0), (0, speed), (0, -speed)]
        elif direction== "NE":
            [(0, 0), (speed, 0), (0, speed), (0, -speed)]
        elif direction== "E":
            [(0, 0), (speed, 0), (0, speed), (0, -speed)]
        elif direction== "SE":
            [(0, 0), (speed, 0), (0, speed), (0, -speed)]
        elif direction== "S":
            [(0, 0), (speed, 0), (0, speed), (0, -speed)]
        elif direction== "SW":
            [(0, 0), (speed, 0), (0, speed), (0, -speed)]   

        dx, dy= random.choice(direction)
        self.rect.x += dx
        self.rect.y += dy

        self.rect.x = max(0, min(self.rect.x, width - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, height - self.rect.height))
        
