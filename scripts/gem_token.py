import pygame

from scripts.utils.assets import load_image
from scripts.utils.ui_utils import build_context_panel

class GemToken:
    def __init__(self, gem_type, tier, star, game):
        self.gem_type = gem_type
        self.tier = tier
        self.star = star
        self.icon = load_image('gems/' + str(gem_type) + '_' + 'tier_' + str(tier) + '_star_' + str(star) + '.png')
        self.game = game
        self.dragging = False
        # self.game.hoverables.append(self)
        # self.rect = pygame.Rect(self.pos[0], self.pos[1], self.tile_size, self.tile_size)
        
    # def draw_context(self, game, surf):
    #     height = 150
    #     width = 350
    #     lable_text = self.game.game_ui.context_font.render('Tier' + self.tier + ' ' + self.gem_type + 'Gem', True, self.game.game_ui.context_text_color)
    #     context_panel, context_pos = build_context_panel(self.game.mpos, width, height, lable_text, game.display.pygame.Surface.get_width())
        
    #     # text = 'Damage: ' + str(self.gem.damage)
    #     # damage_text = self.game.game_ui.info_font.render(text, True, self.game.game_ui.info_text_color)
    #     # damage_text_rect = damage_text.get_rect(center=(s.get_width() / 2, 60))
    #     # s.blit(damage_text, damage_text_rect)

    #     # text = 'Range: ' + str(self.gem.range / 10)
    #     # range_text = self.game.game_ui.info_font.render(text, True, self.game.game_ui.info_text_color)
    #     # range_text_rect = range_text.get_rect(center=(s.get_width() / 2, 80))
    #     # s.blit(range_text, range_text_rect)

    #     # text = 'Shots per second: ' + str(1 / self.gem.shot_delay)
    #     # sps_text = self.game.game_ui.info_font.render(text, True, self.game.game_ui.info_text_color)
    #     # sps_text_rect = sps_text.get_rect(center=(s.get_width() / 2, 100))
    #     # s.blit(sps_text, sps_text_rect)

    #     # text = 'Hits: ' + str(self.gem.hit_count)
    #     # hits_text = self.game.game_ui.info_font.render(text, True, self.game.game_ui.context_text_color)
    #     # hits_text_rect = hits_text.get_rect(center=(s.get_width() / 2, 120))
    #     # s.blit(hits_text, hits_text_rect)

    #     surf.blit(context_panel, context_pos)