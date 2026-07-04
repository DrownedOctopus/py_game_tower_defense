import pygame

from scripts.utils.assets import load_image

STASH_WIDTH = 100

class GemStash:
    MAX_SIZE = 9
    
    def __init__(self, game, surf, pos, slot_size=33):
        self.game = game
        self.surf = surf
        self.pos = pos
        self.tokens = []
        self.slot_size = slot_size        
        self.rect = pygame.Rect(pos[0], pos[1], STASH_WIDTH, STASH_WIDTH)
        
        self.assets = {
            'gem_stash': load_image("ui/gem_stash.png"),
            'gem_stash_hover': load_image("ui/gem_stash_hover.png")
        }
        
    def check_hover(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            return True
        return False

    def on_hover(self):
        if self.game.mpos is None:
            return
        token = self.get_token_at(pygame.mouse.get_pos())
        
        
    def add(self, gem_token):
        if len(self.tokens) < self.MAX_SIZE:
            self.tokens.append(gem_token)
            return True
        return False
    
    def remove(self, gem_token):
        self.tokens.remove(gem_token)
            
    def is_full(self):
        return len(self.tokens) >= self.MAX_SIZE
    
    def draw(self, hovered_token=None):
        self.surf.blit(pygame.transform.scale(self.assets['gem_stash'], (STASH_WIDTH, STASH_WIDTH)), self.pos)
        for i, token in enumerate(self.tokens):
            pos = self._get_slot_pos(i)
            self.surf.blit(token.icon, pos)
            if token == hovered_token:
                hover_rect = self.get_slot_rect(token)
                self.surf.blit(self.assets['gem_stash_hover'], (hover_rect[0] + 1, hover_rect[1] + 1))

    def _get_slot_pos(self, index):
        col = index % 3
        row = index // 3
        return (self.pos[0] + 1 + col * self.slot_size, 
                self.pos[1] + 1 + row * self.slot_size)
        
    def get_slot_rect(self, token):
        index = self.tokens.index(token)
        pos = self._get_slot_pos(index)
        return pygame.Rect(pos[0], pos[1], self.slot_size, self.slot_size)
        
    def get_token_at(self, mouse_pos):
        for i, token in enumerate(self.tokens):
            pos = self._get_slot_pos(i)
            rect = pygame.Rect(pos[0], pos[1], self.slot_size, self.slot_size)
            if rect.collidepoint(mouse_pos):
                return token
        return None