import pygame

class Lines:

    def __init__(self, x, y, width, height, color):
        self.rect= pygame.Rect(x, y, width, height)
        self.color= color
    
    def draw_lines(self, window):
        pygame.draw.rect(window, self.color, self.rect)

