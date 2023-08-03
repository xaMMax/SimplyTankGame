import random

import pygame


class Settings:
    def __init__(self, font_size=20):
        self.screen_width = 1200
        self.screen_height = 800
        self.flags = pygame.DOUBLEBUF | pygame.HWSURFACE

        self.bg_color = (255, 247, 192)
        self.black = 'black'
        self.white = 'white'
        self.green = 'green'
        self.blue = 'blue'
        self.gray = 'gray'

        self.font = pygame.font.SysFont('Verdana', font_size)

        # self.player_speed = 1
        # self.enemy_speed = 1
        # self.bullet_speed = 18
        # self.projectile_speed = 17
        # self.rocket_speed = 16
        #
        # self.start_level = 1
        # self.level_increase = 40
        #

        #
        # self.enemy_current_health = 100
        # self.enemy_max_health = 500
        #
        # self.player_current_health = 100
        # self.player_max_health = 500
        #
        # self.bullet_damage = 30
        # self.projectile_damage = 70
        # self.rocket_damage = 200
        #
        # self.bullet_amount = 200
        # self.projectile_amount = 100
        # self.rocket_amount = 30
        #
        #
        #
