import pygame
from scripts.health_bar import HealthBar
from scripts.utils.audio import play_audio


class Monster (pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, pathfinding, img, monster_data):
        super().__init__()
        self.pos = (float(x_pos), float(y_pos))
        self.screen_pos = self.pos[0], self.pos[1]
        self.current_rotation = 0        
        self.max_health = monster_data['max_health']
        self.monster_img = img
        self.monster_move_speed = monster_data['move_speed']
        self.steel_value = monster_data['steel_value']
        self.base_hit_cost = monster_data['hit_cost']
        self.current_health = self.max_health
        self.health_bar = HealthBar()
        self.monster_mask = pygame.mask.from_surface(self.monster_img)
        self.pathfinding = pathfinding
        self.game = pathfinding.game
        self.target_pos = None
        self.target_rotation = 0
        self.pathway = None
        self.pathway_index = 0
        self.is_dead = False

    def take_dmg(self, dmg):
        self.current_health -= dmg

    def draw(self, surface):
        if self.current_rotation != self.target_rotation:
            delta_rotation = (self.current_rotation - self.target_rotation)
            self.monster_img = pygame.transform.rotate(self.monster_img, delta_rotation)
            self.current_rotation = self.target_rotation
        surface.blit(self.monster_img, self.screen_pos)
        if self.current_health < self.max_health:
            self.health_bar.draw(surface, self.screen_pos, self.current_health/self.max_health)

    def find_path(self):
        self.pathway = []
        for tile in self.pathfinding.pathway:
            self.pathway.append([tile.row, tile.col])
        self.pathway.reverse()
        self.target_pos = (float(self.pathway[self.pathway_index][0]), float(self.pathway[self.pathway_index][1]))

    def update(self):
        if self.current_health <= 0:
            self.kill()
            self.game.current_steel += self.steel_value
            self.is_dead = True
            play_audio('death_1', self.game.sfx_assets)
            return
        
        if self.pathway is None:
            return
        if self.pathway_index == len(self.pathway) - 1:
            self.kill()
            self.game.current_steel -= self.base_hit_cost
            play_audio('death_2', self.game.sfx_assets)
            return
        
        threshold = .1
        if abs(self.pos[0] - self.target_pos[0]) <= threshold and abs(self.pos[1] - self.target_pos[1]) <= threshold:
            self.pos = self.target_pos
            self.pathway_index += 1
            self.target_pos = (float(self.pathway[self.pathway_index][0]), float(self.pathway[self.pathway_index][1]))
            
        dt = self.game.dt
        #1. Above us
        if self.target_pos[0] == self.pos[0] and self.target_pos[1] < self.pos[1]:
            self.target_rotation = 270
            self.pos = (self.pos[0], self.pos[1] - (self.monster_move_speed * dt))
        # 2. To our right
        elif self.target_pos[0] > self.pos[0] and self.target_pos[1] == self.pos[1]:
            self.target_rotation = 0
            self.pos = (self.pos[0] + (self.monster_move_speed * dt), self.pos[1])
        # 3. Below us
        elif self.target_pos[0] == self.pos[0] and self.target_pos[1] > self.pos[1]:
            self.target_rotation = 90
            self.pos = (self.pos[0], self.pos[1] + (self.monster_move_speed * dt))
        # 4. To our Left
        elif self.target_pos[0] < self.pos[0] and self.target_pos[1] == self.pos[1]:
            self.target_rotation = 180
            self.pos = (self.pos[0] - (self.monster_move_speed * dt), self.pos[1])
        # if none of these things our true, then we have gone off the grid
        else:
            raise ValueError("Target position is out of bounds")
        self.screen_pos = self.pos[0] * self.game.tile_size, self.pos[1] * self.game.tile_size
