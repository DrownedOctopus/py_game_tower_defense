import pygame
from scripts.healthBar import HealthBar


class Monster:
    def __init__(self, x_pos, y_pos, max_health=10):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.max_health = max_health
        self.current_health = 10
        self.healthBar = HealthBar(self, self.x_pos, self.y_pos)
        self.monster_img = pygame.image.load('art/centipede.png')
        self.monster_mask = pygame.mask.from_surface(self.monster_img)
        self.monster_move_speed = 10
        self.monster_movement = [False, False]

    def dmg(self, dmg):
        # if self.healthBar is None:
        #     self.healthBar = HealthBar(self.x_pos, self.y_pos)
        self.current_health -= dmg

    def draw_monster(self, surface, pos):
        surface.blit(self.monster_img, pos)

    def get_pos(self):
        return self.x_pos, self.y_pos
