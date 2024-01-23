import pygame
from settins import Settings


class Background:
    def __init__(self, ):
        # self.name = name
        # self.move_int = move_int
        self.settings = Settings()
        self.background = pygame.transform.scale(pygame.image.load
                                                 ('images/background.png').convert_alpha(),
                                                 (self.settings.screen_width, self.settings.screen_height))
        self.bg_ground = pygame.image.load('images/ground.png').convert_alpha()
        self.bg_tree = pygame.transform.scale(pygame.image.load
                                              ('images/trees.png').convert_alpha(),
                                              (self.settings.screen_width, self.settings.screen_height / 2))
        self.bg_cloud_near = pygame.image.load('images/clouds_nearby.png').convert_alpha()
        self.bg_cloud_far = pygame.image.load('images/clouds_far.png').convert_alpha()
        self.bg_sun = pygame.image.load('images/sun.png').convert_alpha()

        self.fire_fire = pygame.transform.scale(pygame.image.load('images/fire_fire.png'),
                                                (200, 100))
        self.fire_fire1 = pygame.transform.scale(pygame.image.load('images/fire_fire.png').convert_alpha(),
                                                (150, 70))
        self.fire_fire2 = pygame.transform.scale(pygame.image.load('images/fire_fire.png').convert_alpha(),
                                                (100, 50))

        self.bg_ground_X1 = 0
        self.bg_tree_X1 = 0
        self.bg_cloud_near_X1 = 0
        self.bg_cloud_far_X1 = 0

        self.bg_ground_X2 = self.bg_ground.get_width()
        self.bg_tree_X2 = self.bg_tree.get_width()
        self.bg_cloud_near_X2 = self.bg_cloud_near.get_width()
        self.bg_cloud_far_X2 = self.bg_cloud_far.get_width()

        self.bg_move = 0
        self.bg_ground_move = 0.8
        self.bg_tree_move = 0.8
        self.bg_cloud_far_move = 0.1
        self.bg_cloud_near_move = 0.3
