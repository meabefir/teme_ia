import pygame
import math

class ColorPicker:
    COLORS = {
        "red": (255, 0, 0),
        "orange": (255, 128, 0),
        "yellow": (255, 255, 0),
        "green": (0, 255, 0),
        "blue": (0, 0, 255),
        "purple": (128, 0, 255),
        "pink": (255, 0, 255),
        "gray": (128, 128, 128)
    }

    def __init__(self, pos = (100, 100), cols=4, width=100, colorChangeCallback=None):
        self.pos = pos
        self.cols = cols
        self.cell_size = width / cols
        height = (math.ceil(len(ColorPicker.COLORS.keys()) / self.cols) + 2.5) * self.cell_size
        self.rect = pygame.Rect(pos[0], pos[1], width, height)

        self.colorChangeCallback = colorChangeCallback

        self.selectedColor = "red"
        self.colorChangeCallback(self.selectedColor)
        self.hoveredColor = None


    def getColorUnderMouse(self, mouse_pos):
        for color, rgb, rect in self.getColorList():
            if rect.collidepoint(mouse_pos):
                return color
        return None


    def getColorList(self):
        """
        returns a list with all the colors names, rgb and their rects
        """
        list = []
        crow = 0
        ccol = 0
        for color, rgb in ColorPicker.COLORS.items():
            color_rect = pygame.Rect(self.pos[0] + ccol * self.cell_size,
                                     self.pos[1] + crow * self.cell_size,
                                     self.cell_size, self.cell_size)
            list += ((color, rgb, color_rect),)

            ccol += 1
            ccol %= self.cols
            if ccol == 0:
                crow += 1
        return list

    def handleEvent(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEMOTION:
            mouse_position = pygame.mouse.get_pos()
            color_under_mouse = self.getColorUnderMouse(mouse_position)
            if color_under_mouse is None:
                self.hoveredColor = None
                return
            self.hoveredColor = color_under_mouse
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # left clicked
            left, middle, right = pygame.mouse.get_pressed()
            if left:
                mouse_position = pygame.mouse.get_pos()
                color_under_mouse = self.getColorUnderMouse(mouse_position)
                if color_under_mouse is None:
                    return
                self.selectedColor = color_under_mouse
                if not self.colorChangeCallback is None:
                    self.colorChangeCallback(self.selectedColor)

    def render(self, screen):
        # draw outline
        pygame.draw.rect(screen, pygame.Color("blue"), self.rect, 3)

        for color, rgb, color_rect in self.getColorList():
            pygame.draw.rect(screen, rgb, color_rect)
            if color == self.hoveredColor:
                pygame.draw.rect(screen, pygame.Color("white"), color_rect, 3)


        # draw the color preview
        rows = math.ceil(len(ColorPicker.COLORS.keys()) / self.cols) + .5
        preview_pos = (self.pos[0] + self.cols * self.cell_size / 2 - self.cell_size,
                       self.pos[1] + rows * self.cell_size)
        preview_size = self.cell_size * 2
        pygame.draw.rect(screen, ColorPicker.COLORS[self.selectedColor], pygame.Rect(preview_pos[0], preview_pos[1],
                                                                                  preview_size, preview_size))