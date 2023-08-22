import random

import pygame


class Settings:
    def __init__(self, font_size=20):
        self.screen_width = 1200
        self.screen_height = 800
        # self.flags = pygame.OPENGL

        self.bg_color = (255, 247, 192)
        self.black = 'black'
        self.white = 'white'
        self.green = 'green'
        self.blue = 'blue'
        self.gray = 'gray'
        self.font = pygame.font.SysFont('Verdana', font_size)

