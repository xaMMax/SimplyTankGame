import random

import pygame
from settins import Settings


class Bonus(pygame.sprite.Sprite, Settings):
    def __init__(self):
        super().__init__()
        Settings.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load
                                            ('images/bonus.png').convert_alpha(), (100, 150))
        self.image_size = self.image.get_size()
        self.rect = self.image.get_rect(center=(random.randint(100, 500), 0))
        self.stop_drop_position = random.randint(400, 600)

    def update(self):
        # self.picture_change()
        if self.rect.bottom > self.screen_height:
            self.kill()
            print('bonus kill self')
        if self.rect.y <= 400:
            self.rect.y += 3
        else:
            self.rect.y = self.stop_drop_position
            self.rect.x -= 0.8
            self.image = pygame.transform.scale(pygame.image.load
                                            ('images/Bonus_dropped.png').convert_alpha(), (75, 70))
        if self.rect.right <= 0:
            self.kill()
            print('bonus kill self')


