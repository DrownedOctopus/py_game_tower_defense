import pygame
from scripts.utils import load_image, load_images


class Tower (pygame.sprite.Sprite):

    def __init__(self, pos, surface):
        super().__init__()
        pygame.init()
        self.damage = 10
        self.attack_speed = 2
        self.pos = pos
        self.surface = surface
        self.tower_img = load_image('Tower.png')
        self.valid_target_gizmo = pygame.image.load('art/valid_target_gizmo.png')
        self.no_target_gizmo = pygame.image.load('art/no_target_gizmo.png')
        self.target_mask_gizmo = pygame.image.load('art/target_mask_gizmo.png')
        self.tower_mask = pygame.mask.from_surface(self.tower_img)
        self.range_mask = pygame.mask.from_surface(self.target_mask_gizmo)
        self.display_radius = True
        self.tile_size = 32
        self.tower_pos = [pos[0] - self.tile_size, pos[1] - self.tile_size, self]

        self.target_radius_pos = [int(self.pos[0]) - (self.no_target_gizmo.get_width() / 2) + (self.tile_size / 2),
                                int(self.pos[1]) - (self.no_target_gizmo.get_height() / 2) + (self.tile_size / 2)]
        self.targets = []
        self.valid_target = None

    def draw(self):
        self.surface.blit(self.tower_img, self.pos)

    def detect_monster(self, monster):
        if self.display_radius:
            # Here is where we check if the monster is in range of the turret
            if self.range_mask.overlap(monster.monster_mask,
               (monster.x_pos - self.target_radius_pos[0], monster.y_pos - self.target_radius_pos[1])):
                self.surface.blit(self.valid_target_gizmo, self.target_radius_pos)
                # print(F"Monster in range of {self.tower_img}")
                self.valid_target = monster
            else:
                self.surface.blit(self.no_target_gizmo, self.target_radius_pos)
