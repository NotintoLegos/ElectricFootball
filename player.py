import pygame


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
