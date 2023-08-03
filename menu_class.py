import pygame
from settins import screen, WIDTH, HEIGHT, C_GRAY, C_BLACK, FONT


class Button():
    def __init__(self,msg, screen):
        self.screen = screen
        self.rect = self.screen.get_rect()
        self.width, self.height = 200, 50
        self.button_color = C_GRAY
        self.text_color = C_BLACK
        self.font = FONT
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.rect.center
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect = self.rect.center

    def draw_button(self):
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)


class Menu(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((WIDTH, HEIGHT))
        self.menu_size = (WIDTH, HEIGHT)
        self.rect = pygame.Rect(0, 0, *self.menu_size)

    def update(self):
        pass
    def show_menu(self):
        pass

