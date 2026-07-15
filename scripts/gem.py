import pygame

from scripts.utils.assets import load_image, load_mask
from scripts.utils.audio import play_audio
from scripts.projectile import Projectile

class Gem (pygame.sprite.Sprite):

    def __init__(self, gem_type, tier, star, stats, abilities, tower, surf, game):
        super().__init__()
        self.gem_type = gem_type
        self.tier = tier
        self.star = star
        self.stats = stats
        self.abilities = abilities
        self.pos = tower.pos
        self.surf = surf
        self.tower = tower
        self.tower.gem = self
        self.projectiles = pygame.sprite.Group()
        self.shot_timer = 0.0
        self.shot_delay = stats["shot_delay"]
        self.range = stats["range"] # Was 100
        self.damage = stats["damage"]
        self.projectile_speed = stats["projectile_speed"]
        self.hit_count = 0
        self.game = game
        self.valid_target_gizmo = load_image('valid_target_gizmo.png')
        self.target_mask_gizmo = load_mask('target_mask_gizmo.png')
        self.valid_target_gizmo = pygame.transform.scale(self.valid_target_gizmo, (self.range * 2, self.range * 2))
        self.target_mask_gizmo = pygame.transform.scale(self.target_mask_gizmo, (self.range * 2, self.range * 2))
        self.gem_img = load_image('gems/' + str(gem_type) + '_' + 'tier_' + str(tier) + '_star_' + str(star) + '.png')
        self.range_mask = pygame.mask.from_surface(self.target_mask_gizmo)
        self.tile_size = self.game.tile_size
        self.targets = []
        self.game.hoverables.append(self)
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.tile_size, self.tile_size)

    def draw(self):
        self.surf.blit(self.gem_img, self.pos)

    def update(self):
        self.shot_timer += self.game.dt
        if len(self.targets) > 0:
            current_target = self.targets[0]
            for target in self.targets:
                if target.pathway_index > current_target.pathway_index:
                    current_target = target
            if self.shot_timer >= self.shot_delay:
                if current_target in self.game.monsters:
                    self.fire(current_target)
                    self.hit_count += 1
                    self.shot_timer = 0.0

    def on_hover(self):
        range_display_pos = (
            self.pos[0] + (self.tile_size / 2) - self.range, self.pos[1] + (self.tile_size / 2) - self.range)
        self.surf.blit(self.valid_target_gizmo, range_display_pos)

    def detect_monster(self):
        self.targets = []
        range_display_pos = (
            self.pos[0] + (self.tile_size / 2) - self.range, self.pos[1] + (self.tile_size / 2) - self.range)
        for monster in self.game.monsters:
            if self.range_mask.overlap(monster.monster_mask,
                                       (monster.screen_pos[0] - range_display_pos[0],
                                        monster.screen_pos[1] - range_display_pos[1])):
                if monster not in self.targets and not monster.is_dead:
                    self.targets.append(monster)

    def fire(self, monster):
        projectile = Projectile(self.pos, monster, self.surf, self.damage, self.projectile_speed, self.game)
        self.projectiles.add(projectile)
        play_audio('fire', self.game.sfx_assets)
        