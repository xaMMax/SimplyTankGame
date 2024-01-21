import pygame
from settins import Settings


class Weapon(pygame.sprite.Sprite, Settings):
    def __init__(self, pos_x, pos_y, player_position, ammo_type='bullet', speed=0):
        super().__init__()
        Settings.__init__(self)

        # self.screen = screen
        self.ammo_type = ammo_type
        self.player_position = player_position

        if ammo_type == 'projectile':
            self.image = pygame.transform.scale(pygame.image.load
                                                ('images/snarad.png').convert_alpha(), (30, 20))
            self.image_size = self.image.get_size()
            self.rect = self.image.get_rect(center=(pos_x, pos_y))
        elif ammo_type == 'rocket':
            self.image = pygame.transform.scale(pygame.image.load
                                                ('images/rocket.png').convert_alpha(), (45, 21))
            self.image_size = self.image.get_size()
            self.rect = self.image.get_rect(center=(pos_x, pos_y))
        elif ammo_type == 'enemy_projectile':
            self.image = pygame.transform.scale(pygame.image.load
                                                ('images/snarad.png').convert_alpha(), (30, 20))
            self.image = pygame.transform.rotate(self.image, 180)
            self.image_size = self.image.get_size()
            self.rect = self.image.get_rect(center=(pos_x, pos_y))
        else:
            self.image = pygame.transform.scale(pygame.image.load
                                                ('images/snarad.png').convert_alpha(), (15, 5))
            self.image_size = self.image.get_size()
            self.rect = self.image.get_rect(center=(pos_x, pos_y))

        self.rocket_fire = False
        self.bullet_speed = speed
        self.projectile_speed = speed
        self.rocket_speed = speed

    def moving(self, bullet_type, player_position):
        if bullet_type == 'projectile':
            self.rect.x += self.projectile_speed
            if self.rect.x > self.screen_width + 10:
                self.kill()
        elif bullet_type == 'rocket':
            if self.rect.centerx >= player_position[0]:
                self.rect.centerx += 4
                self.rect.centery -= 4
            if self.rect.centerx - player_position[0] >= 70:
                self.rocket_fire = True
                self.rect.centerx += self.rocket_speed
                self.rect.centery += 5
        elif bullet_type == 'enemy_projectile':
            self.rect.x -= self.projectile_speed
            if self.rect.x < 0:
                self.kill()
        else:
            self.rect.x += self.bullet_speed
            if self.rect.x > self.screen_width + 10:
                self.kill()

    def enemy_bullet(self):
        self.rect.x -= self.projectile_speed
        if self.rect.x < 0:
            self.kill()

    def power_up(self):
        self.bullet_speed += 2
        self.rocket_speed += 2
        self.projectile_speed += 2

    def get_type(self):
        return self.ammo_type

    def update(self, ):
        if self.rect.left > self.screen_width:
            self.kill()
            print(self.ammo_type, 'kill self')
        if self.rocket_fire:
            self.image = pygame.transform.scale(pygame.image.load('images/rocket_fire.png').convert_alpha(), (120, 22))

        return self.moving(self.ammo_type, self.player_position)
