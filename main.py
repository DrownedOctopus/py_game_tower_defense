import sys

import pygame

from scripts import tower
from scripts import monster

# Player monster details
monster_pos = [626, 222]


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("tower defense game")

        self.SCREEN_WIDTH = pygame.display.get_desktop_sizes()[0][0]
        self.SCREEN_HEIGHT = pygame.display.get_desktop_sizes()[0][1]

        self.bg_border = 25
        self.bg_color = (25, 25, 25)
        self.game_bg_rect_width = self.SCREEN_WIDTH - (self.bg_border * 2)
        self.game_bg_rect_height = self.SCREEN_HEIGHT - (self.bg_border * 2)
        self.game_bg_rect = (self.bg_border, self.bg_border, self.game_bg_rect_width, self.game_bg_rect_height)

        self.bg_grid_width_count = 28
        self.bg_grid_height_count = 45
        self.bg_grid_color = (50, 50, 50)

        # screen is now a "Surface" as that is the return type from setting the display mode
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

        self.clock = pygame.time.Clock()

    def draw_grid(self):
        # Here is where we are initializing the bg and bg grid
        pygame.draw.rect(self.screen, self.bg_color, self.game_bg_rect)
        for count in range(self.bg_grid_width_count - 1):
            pygame.draw.line(self.screen, self.bg_grid_color,
                             (self.bg_border,
                              ((count + 1) * self.game_bg_rect_height / self.bg_grid_width_count + self.bg_border)),
                             ((self.game_bg_rect_width + self.bg_border),
                              ((count + 1) * self.game_bg_rect_height / self.bg_grid_width_count + self.bg_border)))

        for count in range(self.bg_grid_height_count - 1):
            pygame.draw.line(self.screen, self.bg_grid_color,
                             (((count + 1) * self.game_bg_rect_width / self.bg_grid_height_count + self.bg_border),
                              self.bg_border),
                             (((count + 1) * self.game_bg_rect_width / self.bg_grid_height_count + self.bg_border),
                              self.SCREEN_HEIGHT - self.bg_border))

    def run(self):
        while True:
            self.draw_grid()
            tower1 = tower.Tower([226, 222], self.screen)

            # Here is where we update the position of the monster
            monster1 = monster.Monster(monster_pos[0], monster_pos[1])
            monster1.draw_monster(self.screen, monster_pos)
            monster1.healthBar.draw_health_bar(self.screen)
            monster_pos[0] += (monster1.monster_movement[1] - monster1.monster_movement[0]) * monster1.monster_move_speed

            # Here is where we check if the monster is in range of the turret
            tower1.detect_monster(monster1)

            # This is the event checker for each frame
            for event in pygame.event.get():
                # This is where we make sure the game breaks out of the loop when the player wishes to exit
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        monster1.monster_movement[0] = True
                    if event.key == pygame.K_RIGHT:
                        monster1.monster_movement[1] = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        monster1.monster_movement[0] = False
                    if event.key == pygame.K_RIGHT:
                        monster1.monster_movement[1] = False

            pygame.display.update()
            self.clock.tick(60)


Game().run()
