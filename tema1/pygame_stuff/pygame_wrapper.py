import pygame

def draw_rect(screen, color, rect: pygame.Rect, width=0):
    pygame.draw.rect(screen, color, pygame.Rect(rect.x-1, rect.y-1, rect.width+2, rect.height+2), width=width)