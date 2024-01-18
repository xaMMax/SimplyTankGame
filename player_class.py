import pygame
from bullet_class import Weapon
from settins import Settings
from background_class import Background


class Player(pygame.sprite.Sprite, Settings):
    def __init__(self, screen):
        # Main init
        super().__init__()
        Settings.__init__(self, font_size=15)

        # General init
        self.screen = screen
        self.move_action = False
        self.weapon = Weapon
        self.health_line_length = 0.5

        # Sprite init
        self.current_sprite = 0
        self.image_sprite_list = []
        self.image_sprite_list.append(pygame.image.load('player_tank/ArmyTank.png'))
        self.image_sprite_list.append(pygame.image.load('player_tank/ArmyTank1.png'))
        self.image_sprite_list.append(pygame.image.load('player_tank/ArmyTank2.png'))
        self.image_sprite_list.append(pygame.image.load('player_tank/ArmyTank3.png'))

        self.image = pygame.transform.scale((self.image_sprite_list[self.current_sprite]).convert_alpha(),
                                            (int(self.screen_width / 10), int(self.screen_width / 10)))
        self.player_size = self.image.get_size()
        self.rect = pygame.Rect(20, 450, *self.player_size)

        # Class specifications
        self.player_speed = 1
        self.player_current_health = 100
        self.player_max_health = 500

        self.bullet_speed = 18
        self.projectile_speed = 17
        self.rocket_speed = 16

        self.bullet_damage = 30
        self.projectile_damage = 70
        self.rocket_damage = 200

        self.bullet_amount = 2000
        self.projectile_amount = 40
        self.rocket_amount = 15

        self.score = 0
        self.level = 1
        self.start_level = 1
        self.level_increase = 5

        self.health_ratio = self.player_current_health * self.health_line_length

        self.background = Background()

    def update(self):
        self.picture_change()
        self.create_player()
        self.basic_health()
        self.hud(f' рівень {self.level} швидкість {self.player_speed}', self.rect.x, self.rect.y - 50)

    def fire(self, text='bullet'):
        if text == 'projectile':
            return self.weapon(self.rect.right + (self.player_size[0] / 2), self.rect.top + self.player_size[0] / 10,
                               self.rect.center, text, self.projectile_speed)
        elif text == 'rocket':
            return self.weapon(self.rect.center[0], self.rect.center[1] - 45, self.rect.center, text, self.rocket_speed)
        else:
            return self.weapon(self.rect.right + (self.player_size[0] / 2), self.rect.top + self.player_size[0] / 5,
                               self.rect.center, text, self.bullet_speed)

    def player_power_up(self):
        if self.player_speed <= 8:
            self.player_speed += 0.7
        self.projectile_amount = self.projectile_amount + int(self.score / 2)
        self.rocket_amount = self.rocket_amount + int(self.score / 2)
        self.bullet_amount = self.bullet_amount + int(self.score / 2)
        self.bullet_damage += 5
        self.projectile_damage += 20
        self.rocket_damage += 30
        self.bullet_speed += 2
        self.rocket_speed += 2
        self.projectile_speed += 2
        self.level += 1

    def move(self, left=False, right=False, top=False, down=False):
        if top and self.rect.top > self.screen.get_height() / 2:
            self.rect.y -= self.player_speed
        if down:
            self.rect.y += self.player_speed
        if left:
            self.rect.x -= self.player_speed
        if right:
            self.rect.x += self.player_speed
        self.move_action = True

    def get_damage(self, amount):
        if self.player_current_health > 0:
            self.player_current_health -= amount
        if self.player_current_health <= 0:
            self.player_current_health = 0
        return

    def get_health(self, amount):
        if self.player_current_health < self.player_max_health:
            self.player_current_health += amount
        if self.player_current_health >= self.player_max_health:
            self.player_current_health = self.player_max_health
        return

    def basic_health(self):
        return pygame.draw.rect(self.screen, 'red',
                                (self.screen.get_width() / 2 - self.player_max_health / 2, 30,
                                 self.player_current_health, 15))

    def hud(self, text=None, x=None, y=None):
        return self.screen.blit(self.font.render(str(text), True, 'black'), (x, y))

    def create_player(self):
        self.screen.blit(self.image, self.rect)

    def picture_change(self):
        if self.current_sprite >= len(self.image_sprite_list):
            self.current_sprite = 0
        self.image = (self.image_sprite_list[self.current_sprite]).convert_alpha()
        self.current_sprite += 1

    def dead(self):
        self.kill()
