import pygame
from pygame.math import Vector2
from scripts.utils.assets import get_image, get_sheet_dim

PROJECTILE_IMG_SHEET = 'projectile_img_sheet'

class Projectile(pygame.sprite.Sprite):
    def __init__(self, start_pos, target, screen_rect, damage, speed, game):
        super().__init__()
        self.frame = [0, 3]
        self.frame_width = 8
        self.frame_height = 8
        self.max_frame_width, self.max_frame_height = get_sheet_dim(PROJECTILE_IMG_SHEET, game.sheet_assets)
        self.img = get_image(PROJECTILE_IMG_SHEET, self.frame, self.frame_width, self.frame_height, game.sheet_assets)
        self.target = target
        self.game = game
        self.speed = speed
        self.screen_surface = screen_rect
        self.screen_rect = screen_rect.get_rect()
        self.rect = self.img.get_rect(center=start_pos)
        self.position = Vector2(start_pos)
        self.dmg = damage
        self.projectile_mask = pygame.mask.from_surface(self.img)
        
    def draw(self):
        self.screen_surface.blit(self.img, self.position)

    def update(self):
        tile_half = (self.game.tile_size // 2)
        direction = (self.target.screen_pos[0] + tile_half, self.target.screen_pos[1] + tile_half) - self.position
        velocity = direction.normalize() * self.speed * self.game.dt
        new_position = Vector2(self.position[0] + velocity[0], self.position[1] + velocity[1])
        self.position = new_position
        self.rect.center = new_position        
        self._advance_frame()        
        self.img = get_image(PROJECTILE_IMG_SHEET, self.frame, self.frame_width, self.frame_height, self.game.sheet_assets)   
        self._check_collision()        
        if not self.screen_rect.contains(self.rect):
            self.kill()
            
    def _check_collision(self):
        if self.projectile_mask.overlap(self.target.monster_mask, (self.target.screen_pos[0] - self.position[0], self.target.screen_pos[1] - self.position[1])):
            self.target.take_dmg(self.dmg)
            self.kill()
    
    def _advance_frame(self):
        self.frame[0] += 1      
        if self.frame[0] >= self.max_frame_width:
            self.frame[0] = 0
            