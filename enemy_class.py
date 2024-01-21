import pygame
import random
from settins import Settings


class Enemy(pygame.sprite.Sprite, Settings):
    def __init__(self, screen, speed, current_health, max_health,):
        super().__init__()
        Settings.__init__(self, font_size=15)

        self.screen = screen

        self.current_sprite = 0
        self.image_sprite_list = []
        self.image_sprite_list.append(pygame.image.load('enemy_tank/enemytank1.png'))
        self.image_sprite_list.append(pygame.image.load('enemy_tank/enemytank2.png'))
        self.image_sprite_list.append(pygame.image.load('enemy_tank/enemytank3.png'))
        self.image_sprite_list.append(pygame.image.load('enemy_tank/enemytank4.png'))
        self.image_sprite_list.append(pygame.image.load('enemy_tank/enemytank5.png'))
        self.image_sprite_list.append(pygame.image.load('enemy_tank/enemytank6.png'))
        self.image_sprite_list.append(pygame.image.load('enemy_tank/enemytank7.png'))
        self.image_sprite_list.append(pygame.image.load('enemy_tank/enemytank8.png'))
        self.image_sprite_list.append(pygame.image.load('enemy_tank/enemytank9.png'))
        self.image_sprite_list.append(pygame.image.load('enemy_tank/enemytank10.png'))
        self.image_sprite_list.append(pygame.image.load('enemy_tank/enemytank11.png'))
        self.image_sprite_list.append(pygame.image.load('enemy_tank/enemytank12.png'))

        self.image = pygame.transform.scale((self.image_sprite_list[self.current_sprite]).convert_alpha(),
                                            (int(self.screen_width/10), int(self.screen_width/10)))
        self.boom = pygame.transform.scale(pygame.image.load('images/boom.png').convert_alpha(),
                                           (int(self.screen_width/10), int(self.screen_width/10)))
        self.enemy_size = self.image.get_size()
        self.rect = pygame.Rect(self.screen_width + int(self.screen_width/10),
                                random.randint(int(self.screen_height/2), int(self.screen_height-50)), *self.enemy_size)
        self.health_line_length = 0.5
        self.hit = False
        self.kill_self = False
        self.enemy_group = pygame.sprite.Group()

        self.enemy_speed = speed
        self.enemy_current_health = current_health
        self.enemy_max_health = max_health

    def update(self):
        self.picture_change()

        if self.hit:
            self.hit_reaction()
            # self.hit = False
        self.rect.x -= self.enemy_speed
        self.basic_health(health_ratio=self.enemy_current_health)
        self.hud(f' здоров"я {self.enemy_current_health}', self.rect.x, self.rect.y - 45)
        self.hit = False

        return

    def get_damage(self, amount):
        if self.enemy_current_health > 0:
            self.enemy_current_health -= amount
        if self.enemy_current_health <= 0:
            self.enemy_current_health = 0
        # if amount > 100:
        #     self.rect.x -= 1

    def get_health(self, amount):
        if self.enemy_current_health < self.enemy_max_health:
            self.enemy_current_health += amount
        if self.enemy_current_health >= self.enemy_max_health:
            self.enemy_current_health = self.enemy_max_health

    def basic_health(self, health_ratio):
        return pygame.draw.rect(self.screen, 'red',
                                (self.rect.x + 30, self.rect.y - 15, health_ratio, 5), border_radius=16)

    def hit_reaction(self):
        return self.screen.blit(self.boom, (self.rect.x - 30, self.rect.y - 50))

    def hud(self, text=None, x=None, y=None):
        return self.screen.blit(self.font.render(str(text), True, 'black'), (x, y))

    def picture_change(self):
        if self.current_sprite >= len(self.image_sprite_list):
            self.current_sprite = 0
        self.image = (self.image_sprite_list[self.current_sprite]).convert_alpha()
        self.current_sprite += 1

    def dead(self):
        self.kill()

