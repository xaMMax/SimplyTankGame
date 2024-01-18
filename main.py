import sys
import asyncio
import random
import pygame
from pygame import K_s, K_d, K_w, K_a, K_q, K_SPACE, K_r, K_p, K_o
from enemy_class import Enemy
from player_class import Player
from settins import Settings
from background_class import Background
from bonus_class import Bonus


class MainLogic(Settings):
    def __init__(self, ):
        pygame.init()
        pygame.display.set_caption('Бандерівець')
        self.time = pygame.time
        self.fps = pygame.time.Clock()
        super().__init__()
        Settings.__init__(self)

        self.screen = pygame.display.set_mode([self.screen_width, self.screen_height])
        self.create_bonus_event = pygame.USEREVENT + 2
        self.bonus_group = pygame.sprite.Group()
        pygame.time.set_timer(self.create_bonus_event, random.randint(4000, 8000))

        self.create_enemy_event = pygame.USEREVENT + 1
        self.random_resp_number_start = 1000
        self.random_resp_number_end = 1700
        pygame.time.set_timer(self.create_enemy_event,
                              random.randint(self.random_resp_number_start,
                                             self.random_resp_number_end))
        self.player = Player(self.screen)

        self.enemy_speed = 1
        self.enemy_current_health = 100
        self.enemy_max_health = 1000

        self.weapon_group = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()

        self.weapon_list = ['projectile', 'rocket']
        self.running = True

        self.player_level_increase = self.player.level_increase

        self.background = Background()
        self.fire_event = False
        self.animation_duration = 1000
        self.animation_start = 0
        self.pause = False
        self.player_current_speed = 0
        self.enemy_current_speed = 0
        # self.ticks = pygame.time.get_ticks()

        self.smoke = pygame.transform.scale(pygame.image.load('images/smoke.png').convert_alpha(),
                                            (30, 30))

    async def main(self):
        while self.running:
            self._update_screen()
            self.fps.tick(60)
            self._check_events()
            self.hit()
            self.player_moving_events()
            await asyncio.sleep(0)

    def _check_events(self):
        self.keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == K_p:
                print("game at pause")
                self.pause = True
                self.player_current_speed = self.player.player_speed
                self.enemy_current_speed = self.enemy_speed
                self.player.player_speed = 0
                self.enemy_speed = 0
            if self.pause and event.type == pygame.KEYDOWN and event.key == K_o:
                print("game run")

                self.pause = False
                self.player.player_speed = self.player_current_speed
                self.enemy_speed = self.enemy_current_speed

            self.create_enemy(event)
            self.create_bonus(event)
            self.fire(event)

    def create_enemy(self, event):
        if event.type == self.create_enemy_event:
            enemy = Enemy(self.screen, self.enemy_speed, self.enemy_current_health, self.enemy_max_health)
            self.enemy_group.add(enemy)

    def create_bonus(self, event):
        if self.pause:
            print("game on pause")
        else:
            if event.type == self.create_bonus_event:
                bonus = Bonus()
                self.bonus_group.add(bonus)

    def fire(self, event):
        if event.type == pygame.KEYDOWN and event.key == K_SPACE:
            if self.player.projectile_amount > 0:
                self.player.projectile_amount -= 1
                self.weapon_group.add(self.player.fire('projectile'))
                self.fire_event = True
            else:
                print('out of projectiles')
        if event.type == pygame.KEYDOWN and event.key == K_r:
            if self.player.rocket_amount > 0:
                self.player.rocket_amount -= 1
                self.weapon_group.add(self.player.fire('rocket'))
            else:
                print('out of rockets')
        if event.type == pygame.KEYDOWN and event.key == K_q:
            # print(pygame.MOUSEBUTTONDOWN)
            if self.player.bullet_amount > 0:
                self.player.bullet_amount -= 1
                self.weapon_group.add(self.player.fire())
            else:
                print('out of bullets')

    def fire_animate(self):
        self.screen.blit(self.background.fire_fire, (self.player.rect.right + (self.player.player_size[0] / 2),
                                                     self.player.rect.top - self.player.player_size[1] / 3))
        # self.screen.blit(self.background.fire_fire1, (self.player.rect.right + self.player.player_size[0],
        #                                              self.player.rect.top + self.player.player_size[0] / 10))
        # self.screen.blit(self.background.fire_fire2, (self.player.rect.right + self.player.player_size[0],
        #                                              self.player.rect.top + self.player.player_size[0] / 10))
        self.fire_event = False

    def player_moving_events(self):
        if self.keys[K_s] and self.player.rect.centery < self.screen_height:
            self.player.move(down=True)
        if self.keys[K_w] and self.player.rect.top > 0:
            self.player.move(top=True)
        if self.keys[K_a] and self.player.rect.left > 0:
            self.player.move(left=True)
        if self.keys[K_d] and self.player.rect.right < self.screen.get_width():
            self.player.move(right=True)

    def hit(self):
        for enemy in self.enemy_group:
            if enemy.rect.right < 0:
                enemy.kill()
                print('enemy kill self')
                self.player.score -= 1
                if self.player.score <= -1:
                    self.running = False
                    quit()
            if self.player.rect.colliderect(enemy.rect):
                # self.player.score -= 2
                enemy.dead()
                self.player.get_damage(40)
                if self.player.player_current_health <= 0:
                    self.running = False
                    quit()
            for bullet in self.weapon_group:
                if bullet.rect.colliderect(enemy.rect):
                    enemy.hit = True
                    if bullet.get_type() == 'projectile':
                        enemy.get_damage(self.player.projectile_damage)
                        enemy.basic_health(enemy.enemy_current_health)
                        if enemy.enemy_current_health == 0:
                            self.player.score += 1
                            enemy.dead()
                            # self.player.projectile_amount += 2
                    elif bullet.get_type() == 'rocket':
                        enemy.get_damage(self.player.rocket_damage)
                        enemy.basic_health(enemy.enemy_current_health)

                        if enemy.enemy_current_health == 0:
                            self.player.score += 1
                            enemy.dead()
                            # self.player.rocket_amount += 1
                    else:
                        enemy.get_damage(self.player.bullet_damage)
                        enemy.basic_health(enemy.enemy_current_health)

                        if enemy.enemy_current_health == 0:
                            self.player.score += 1
                            self.player.projectile_amount += 2
                            enemy.dead()
                            # self.player.bullet_amount += 1
                    bullet.kill()

    def get_bonus(self):
        random_bonus_number = random.randint(0, 3)
        for bonus in self.bonus_group:
            if self.player.rect.colliderect(bonus.rect):
                if random_bonus_number == 0:
                    self.player.player_current_health += random.randint(10, 45)
                elif random_bonus_number == 1:
                    self.player.rocket_amount += random.randint(5, 15)
                elif random_bonus_number == 2:
                    self.player.projectile_amount += random.randint(15, 25)
                elif random_bonus_number == 3:
                    self.player.bullet_amount += random.randint(100, 170)
                bonus.kill()

    def power_up(self):
        if self.player.score == self.player.level_increase:
            self.player.score += 1
            self.player.level_increase += int((self.player.score//2) * 3)
            self.player.player_power_up()
            self.enemy_power_up()

    def enemy_power_up(self):
        # self.level += 1
        if self.enemy_speed <= 8:
            self.random_resp_number_start += 100
            self.random_resp_number_end -= 100
        self.enemy_speed += 0.7
        self.enemy_current_health += 20

    def game_hud(self, text=None, x=None, y=None):
        return self.screen.blit(self.font.render(str(text), True, 'black'), (x, y))

    def background_func(self):
        if self.pause:
            print("game on pause")
            self.screen.blit(self.background.bg_sun, (50, 50))
            self.background.bg_cloud_far_X1 -= 0
            self.background.bg_cloud_far_X2 -= 0
            if self.background.bg_cloud_far_X1 < 0:
                self.background.bg_cloud_far_X1 = 0
            if self.background.bg_cloud_far_X2 < 0:
                self.background.bg_cloud_far_X1 = 0
            self.screen.blit(self.background.bg_cloud_far, (self.background.bg_cloud_far_X1, 130))
            self.screen.blit(self.background.bg_cloud_far, (self.background.bg_cloud_far_X2, 130))

            self.background.bg_cloud_near_X1 -= 0
            self.background.bg_cloud_near_X2 -= 0
            if self.background.bg_cloud_near_X1 < 0:
                self.background.bg_cloud_near_X1 = 0
            if self.background.bg_cloud_near_X2 < 0:
                self.background.bg_cloud_near_X1 = 0
            self.screen.blit(self.background.bg_cloud_near, (self.background.bg_cloud_near_X1, 130))
            self.screen.blit(self.background.bg_cloud_near, (self.background.bg_cloud_near_X2, 130))

            self.screen.blit(self.background.bg_ground, (self.background.bg_ground_X1, 260))
            self.background.bg_tree_X1 -= 0
            self.background.bg_tree_X2 -= 0
            if self.background.bg_tree_X1 < 0:
                self.background.bg_tree_X1 = 0
            if self.background.bg_tree_X2 < 0:
                self.background.bg_tree_X2 = 0
            self.screen.blit(self.background.bg_tree, (self.background.bg_tree_X1, 130))
            self.screen.blit(self.background.bg_tree, (self.background.bg_tree_X2, 130))
        else:
            self.screen.blit(self.background.bg_sun, (50, 50))
            self.background.bg_cloud_far_X1 -= self.background.bg_cloud_far_move
            self.background.bg_cloud_far_X2 -= self.background.bg_cloud_far_move
            if self.background.bg_cloud_far_X1 < -self.background.bg_cloud_far_X2:
                self.background.bg_cloud_far_X1 = self.background.bg_cloud_far_X2
            if self.background.bg_cloud_far_X2 < -self.background.bg_cloud_far_X2:
                self.background.bg_cloud_far_X1 = self.background.bg_cloud_far_X2
            self.screen.blit(self.background.bg_cloud_far, (self.background.bg_cloud_far_X1, 130))
            self.screen.blit(self.background.bg_cloud_far, (self.background.bg_cloud_far_X2, 130))

            self.background.bg_cloud_near_X1 -= self.background.bg_cloud_near_move
            self.background.bg_cloud_near_X2 -= self.background.bg_cloud_near_move
            if self.background.bg_cloud_near_X1 < -self.background.bg_cloud_near_X2:
                self.background.bg_cloud_near_X1 = self.background.bg_cloud_near_X2
            if self.background.bg_cloud_near_X2 < -self.background.bg_cloud_near_X2:
                self.background.bg_cloud_near_X1 = self.background.bg_cloud_near_X2
            self.screen.blit(self.background.bg_cloud_near, (self.background.bg_cloud_near_X1, 130))
            self.screen.blit(self.background.bg_cloud_near, (self.background.bg_cloud_near_X2, 130))

            self.screen.blit(self.background.bg_ground, (self.background.bg_ground_X1, 260))
            self.background.bg_tree_X1 -= self.background.bg_tree_move
            self.background.bg_tree_X2 -= self.background.bg_tree_move
            if self.background.bg_tree_X1 < -self.background.bg_tree.get_width():
                self.background.bg_tree_X1 = self.background.bg_tree.get_width()
            if self.background.bg_tree_X2 < -self.background.bg_tree.get_width():
                self.background.bg_tree_X2 = self.background.bg_tree.get_width()
            self.screen.blit(self.background.bg_tree, (self.background.bg_tree_X1, 130))
            self.screen.blit(self.background.bg_tree, (self.background.bg_tree_X2, 130))

    def _update_screen(self):
        self.screen.fill(self.bg_color)
        self.background_func()

        self.player.update()

        # DONT DELETE
        self.enemy_group.draw(self.screen)
        self.enemy_group.update()

        self.weapon_group.draw(self.screen)
        self.weapon_group.update()

        self.bonus_group.draw(self.screen)
        self.bonus_group.update()

        self.game_hud(f'FPS: {int(self.fps.get_fps())}', self.screen.get_width() - 200, 10)
        self.game_hud(f'Ваш рахунок: {self.player.score}', self.screen.get_width() - 200, 35)
        self.game_hud(f'Боєзапас снарядів {self.player.projectile_amount} "Пробіл"', 10, 10)
        self.game_hud(f'Боєзапас ракет {self.player.rocket_amount} "R"', 10, 35)
        self.game_hud(f'Боєзапас куль {self.player.bullet_amount} "Q"', 10, 60)
        # self.game_hud(f'weapon speed {int(self.player.bullet_speed)}\n'
        #               f'{self.player.rocket_speed}\n'
        #               f'{self.player.projectile_speed}', 10, 80)
        self.game_hud(f'Наступний рівень після {self.player.level_increase}рахунку', (self.screen.get_width() / 2) - 70, 45)
        self.game_hud(f'Здоров"я {self.player.player_current_health}', (self.screen.get_width() / 2) - 50, 3)
        if self.fire_event:
            self.fire_animate()
        self.get_bonus()
        self.power_up()
        pygame.display.update()


if __name__ == '__main__':
    banderivets = MainLogic()
    asyncio.run(banderivets.main())
