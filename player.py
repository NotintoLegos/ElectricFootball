import pygame
import random


class Player:

    def __init__(self, x, y, width, height, color):
        self.rect= pygame.Rect(x, y, width, height)
        self.color= color

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
    def defensive_movement_linemen(self, slow_velocity, width, height, dx, dy, other_players):
        directions= [(slow_velocity, 0), (0, 0), (0, slow_velocity), (0, -slow_velocity)]
        dx, dy= random.choice(directions)

        new_rect= self.rect.move(dx, dy)

        if any(new_rect.colliderect(player.rect) for player in other_players if player != self):
            return

        if 0 <= new_rect.x <= width - self.rect.width:
            self.rect.x = new_rect.x
        if 0 <= new_rect.y <= height - self.rect.height:
            self.rect.y = new_rect.y

            
#offense movements
    def offensive_movement_linemen(self, slow_velocity, width, height, dx, dy, other_players):
        directions= [(0, 0), (-slow_velocity, 0), (0, slow_velocity), (0, -slow_velocity)]
        dx, dy= random.choice(directions)

        new_rect= self.rect.move(dx, dy)

        if any(new_rect.colliderect(player.rect) for player in other_players if player != self):
            return
        
        if 0 <= new_rect.x <= width - self.rect.width:
            self.rect.x = new_rect.x
        if 0 <= new_rect.y <= height - self.rect.height:
            self.rect.y = new_rect.y
