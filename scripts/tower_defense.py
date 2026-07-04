import sys
import os

import pygame

from scripts import tower, gem, monster, ui, level
from scripts.gem_bag import GemBag
from scripts.gem_token import GemToken
from scripts.gem_factory import GemFactory
from scripts.gem_stash import GemStash
from scripts.ui import Button
from scripts.utils.audio import play_audio
from scripts.utils.assets import load_image, load_images, load_monsters
from scripts.utils.ui_utils import draw_text
from scripts.utils.save import load_save, save_game
from scripts.tilemap import Tilemap
from scripts.pathfinding import Pathfinding, make_grid, draw_pathfinding
from scripts.pathfinding import algorithm as pf_algorithm
from scripts.progression import complete_level

FPS = 60
WIDTH = 1280
ROWS = 34
BASE_AUDIO_PATH = "audio/"
TILES_WIDE = 34
TILES_TALL = 22

class TowerDefense:
    def __init__(self, app):
        pygame.display.set_caption("Errour: Canto")
        # here is where we initialize the game, before our while loop, this code only runs once
        pygame.mouse.set_visible(False)
        
        self.app = app
        self.screen = app.screen
        self.display = pygame.Surface((1280, 720))
        self.dt = 0
        
        # here is where we initalize our monsters
        self.monster_data = load_monsters('data/monsters.json')

        # here we will import all the assets we need in our game at runtime
        self.assets = {
            'player': load_image("player.png"),
            'grass': load_images("grass"),
            'dirt': load_images("dirt"),
            'pathway': load_images("pathway"),
            'space_bg': load_images("space_bg"),
            'mouse_pointer': load_image("mouse_pointer.png"),
            'tower': load_image("tower.png"),
            'gem': load_image("gem.png"),
            'valid_target_gizmo': load_image("valid_target_gizmo.png"),
            'target_mask_gizmo': load_image("target_mask_gizmo.png"),
            'monsters': {
                m_type: load_image('monsters/' + data['image'])
                for m_type, data in self.monster_data.items()
            }
        }
        
        self.ui_assets = {
            'l_side_bar': load_image("ui/UI_L_SideBar.png"),
            'r_side_bar': load_image("ui/UI_R_SideBar.png"),
            'top_bar': load_image("ui/UI_TopBar.png"),
            'bottom_bar': load_image("ui/UI_BottomBar.png"),
            'play_button': load_image("ui/play_button.png"),
            'pause_button': load_image("ui/pause_button.png"),
            'fast_forward_button': load_image("ui/fast_forward_button.png"),
            'tower_button': load_image("ui/tower_button.png"),
            'gem_button': load_image("ui/gem_button.png"),
            'tower_button_small': load_image("ui/tower_button_small.png"),
            'gem_button_small': load_image("ui/gem_button_small.png"),
            'mars_hex_01': load_image("ui/mars_hex_01.png"),
            'mars_hex_select_01': load_image("ui/mars_hex_select_01.png"),
            'planet_bg': load_image("ui/planet_bg.png"),
            'mouse_pointer': load_image("mouse_pointer.png"),
            'wave_button_hover': load_image("ui/wave_button_hover.png"),
            'wave_button': load_image("ui/wave_button.png"),
            'gem_stash': load_image("ui/gem_stash.png")
        }
        
        self.sheet_assets = {
            'projectile_img_sheet': [pygame.image.load('art/round_bullets_small.png').convert_alpha(), 6, 8],
            'space_ground_tiles': [pygame.image.load('art/background_tiles.png').convert_alpha(), 32, 6, 12]
        }
        
        self.sfx_assets = {
            'fire': pygame.mixer.Sound(BASE_AUDIO_PATH + "laser_bolt.mp3"),
            'build': pygame.mixer.Sound(BASE_AUDIO_PATH + "build_noise.mp3"),
            'button': pygame.mixer.Sound(BASE_AUDIO_PATH + 'button_press.mp3'),
            'death_1': pygame.mixer.Sound(BASE_AUDIO_PATH + 'death_noise_1.mp3'),
            'death_2': pygame.mixer.Sound(BASE_AUDIO_PATH + 'death_noise_2.mp3'),
            'BGM_Menu': BASE_AUDIO_PATH + 'BGM_Menu.wav',
            'BGM_Game_1': BASE_AUDIO_PATH + 'BGM_Game_1.wav',
            'BGM_Game_2': BASE_AUDIO_PATH + 'BGM_Game_2.wav'
        }

        self.text_font = pygame.font.Font("fonts/Bandwidth8x8.ttf", 10)
        self.clock = app.clock
        self.bg_color = (25, 25, 25)
        self.build_mode = False
        self.paused = True
        self.pathfinding_mode = False
        self.clicking = False
        self.right_clicking = False
        self.shift = False
        self.mpos = None
        self.screen_mpos = pygame.mouse.get_pos()
        self.tile_pos = None
        self.debug_mode = False
        self.fast_forward = False
        self.level_ended = False
        self.dragging_token = None

        # Here is where we can initialize the scene
        self.towers = pygame.sprite.Group()
        self.gems = pygame.sprite.Group()
        self.monsters = pygame.sprite.Group()
        self.current_build_img = None
        self.current_build_type = None
        self.hoverables = []

        # Here is where we can initialize resources
        self.current_steel = 300
        self.gem_cost = 60
        self.tower_cost = 150

        # here is where we initialize our level
        self.level = level.Level(self)
        self.save_data = app.save_data
        self.current_level = None
        self.current_wave = self.level.current_wave

        # here is where we initialize our tilemap
        self.tile_size = 32
        self.tilemap = Tilemap(self,  self.tile_size)
        self.pathfinding = Pathfinding(self)
        self.game_ui = ui.UI("game", self.display)
        self.pf_grid = make_grid(ROWS, WIDTH)
        self.pf_started = False

        # here we manage pathfinding initialization
        self.pf_start = None
        self.pf_end = None
        self.monster_spawn_pos = None
        self.data_filepath = "data"
        self.render_scale = 2.0
        
        self.gem_factory = GemFactory(self)
        self.gem_factory.load('data/gems.json')
        self.gem_bag = GemBag(app.save_data["bags"])
        self.gem_stash = GemStash(self, self.screen, (1135, 400))
        self.hoverables.append(self.gem_stash)
        
    def _init_resolution(self):
        self.screen.blit(pygame.transform.scale(self.display, (1280, 720)), (0, 0))

    def run_pathfinding(self):
        if self.level_ended:
            return
 
        if self.debug_mode:
            self.pathfinding.update(True)
        else:
            self.pathfinding.update()
        if not self.pf_started and self.paused:
            self.paused = False
            for row in self.pf_grid:
                for tile in row:
                    tile.update_neighbors(self.pf_grid)
            if self.debug_mode:
                pf_algorithm(lambda: draw_pathfinding(self.display, self.pf_grid, ROWS, WIDTH),
                                self.pf_grid, self.pf_start, self.pf_end, self, True)
            else:
                pf_algorithm(lambda: draw_pathfinding(self.display, self.pf_grid, ROWS, WIDTH),
                                self.pf_grid, self.pf_start, self.pf_end, self)

    def run_level(self):
        self.level.update()

    def end_level(self):
        self.level_ended = True
        self.app.save_data = complete_level(
            self.app.save_data,
            self.app.current_level_key,
            self.level.unlocks
        )
        save_game('data/save.json', self.app.save_data)
        return 'map'

    def spawn_monsters(self, m_type):
        monster_n = monster.Monster(self.monster_spawn_pos[0], self.monster_spawn_pos[1], self.pathfinding,
                                    self.assets['monsters'][m_type], self.monster_data[m_type])
        self.monsters.add(monster_n)
        monster_n.find_path()
        
    def _clamp_tile_pos(self):
        if self.tile_pos is None:
            return
        if self.tile_pos[0] <= 0:
            self.tile_pos = None
            return
        if self.tile_pos[0] >= TILES_WIDE:
            self.tile_pos = None
            return
        if self.tile_pos[1] <= -1:
            self.tile_pos = None
            return
        if self.tile_pos[1] >= TILES_TALL:
            self.tile_pos = None

    def build_display(self):
        self.current_build_img.set_alpha(100)
        if self.tile_pos is not None:
            if self.current_build_type == 'gem':
                tower_open = False
                for n_tower in self.towers:
                    if self.tile_pos == n_tower.tile_pos and not n_tower.has_gem:
                        tower_open = True
                if tower_open:
                    self.display.blit(self.current_build_img,
                                        (self.tile_pos[0] * self.tilemap.tile_size * self.render_scale,
                                        self.tile_pos[1] * self.tilemap.tile_size * self.render_scale))
                    return
                else:
                    return
            self.display.blit(self.current_build_img,
                                (self.tile_pos[0] * self.tilemap.tile_size * self.render_scale, self.tile_pos[1] * self.tilemap.tile_size * self.render_scale))

    def build(self):
        """Creates instance of object for player"""
        if self.current_build_type == 'tower' and self.current_steel >= self.tower_cost:
            tower_n = tower.Tower(
                (self.tile_pos[0] * self.tilemap.tile_size * self.render_scale, self.tile_pos[1] * self.tilemap.tile_size * self.render_scale), self.tile_pos,
                self.display, self)
            self.towers.add(tower_n)
            self.current_steel -= self.tower_cost
            play_audio('build', self.sfx_assets)

        self.current_build_img = None
        self.current_build_type = None
        self.build_mode = False
        
    def _enter_tower_build_mode(self):
        self.current_build_img = self.assets['tower'].copy()
        self.current_build_type = 'tower'
        self.build_mode = True

    def _draw_gem(self):
        if not self.gem_stash.is_full() and self.current_steel >= self.gem_cost:
            gem_type, tier, star = self.gem_bag.draw()
            gem_token = GemToken(gem_type, tier, star, self)
            self.gem_stash.add(gem_token)
            self.current_steel -= self.gem_cost
            
    def _init_level(self):
        # here we manage our BGM
        play_audio('BGM_Game_1', self.sfx_assets, True)
        play_audio('BGM_Game_2', self.sfx_assets, True)
        
        self.create_level_buttons()
        self._init_resolution()
        
        
        # Here is where we load all our data that is stored in files
        try:
            if os.path.exists(self.data_filepath):
                self.level.load("data/" + self.current_level)
                self.level.start()
                map_name = self.level.map
                self.tilemap.load("data/" + str(map_name) + ".json")
        except FileNotFoundError:
            print("File not found: " + self.data_filepath)
        except PermissionError:
            print("Did not have permission to load file")
            
        # Here is where we initialize our dynamic elements
        for s_tower in self.level.starting_towers:
            tower_pos = s_tower
            s_tower = tower.Tower(
                (tower_pos[0] * self.tilemap.tile_size * self.render_scale, tower_pos[1] * self.tilemap.tile_size * self.render_scale), (tower_pos[0], tower_pos[1]),  # This makes me hate dynamic typing hour long trying to fix this
                self.display, self)
            self.towers.add(s_tower)
            for s_gem in self.level.starting_gems:
                gem_pos = s_gem
                if gem_pos == tower_pos:
                    continue
                    # s_gem = gem.Gem(
                    #     (gem_pos[0] * self.tilemap.tile_size * self.render_scale, gem_pos[1] * self.tilemap.tile_size * self.render_scale),
                    #     s_tower,
                    #     self.display, self)
                    # s_tower.has_gem = True
                    # self.gems.add(s_gem)
                else:
                    s_tower.has_gem = False
                    
        self.level.start_wave()
        self.fast_forward = False
        self.current_wave = 1
        self.pathfinding.update()
        spawn_pos = self.level.monster_spawn_pos
        base_pos = self.level.base_pos
        self.pf_start = self.pf_grid[spawn_pos[0]][spawn_pos[1]]
        self.monster_spawn_pos = spawn_pos
        self.pf_start.make_start()
        self.pf_end = self.pf_grid[base_pos[0]][base_pos[1]]
        self.pf_end.make_end()
        for row in self.pf_grid:
            for tile in row:
                tile.update_neighbors(self.pf_grid)
        pf_algorithm(lambda: draw_pathfinding(self.display, self.pf_grid, ROWS, WIDTH),
                        self.pf_grid, self.pf_start, self.pf_end, self)

        self.game_ui.create_wave_display(self.level.waves, self.monster_data)
            
    def _handle_events(self):
        # This is the event checker for each frame
        for event in pygame.event.get():
            # This is where we make sure the game breaks out of the loop when the player wishes to exit
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if self.pf_started:
                continue

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.build_mode:
                        if self.tile_pos is not None:
                            self.build()
                    else:
                        self.game_ui.check_click()
                    
                    if not self.build_mode:    
                        token = self.gem_stash.get_token_at(pygame.mouse.get_pos())
                        if token:
                            self.dragging_token = token

                    if self.debug_mode:
                        row = self.tile_pos[0]
                        col = self.tile_pos[1]
                        tile = self.pf_grid[row][col]
                        if not self.pf_start and tile != self.pf_end:
                            pf_start = tile
                            pf_start.make_start()
                        elif not self.pf_end and tile != self.pf_start:
                            pf_end = tile
                            pf_end.make_end()
                        elif tile != self.pf_end and tile != self.pf_start:
                            tile.make_barrier()

                if event.button == 3:
                    self.right_clicking = True
                    if self.debug_mode:
                        row = self.tile_pos[0]
                        col = self.tile_pos[1]
                        tile = self.pf_grid[row][col]
                        tile.reset()
                        if tile == self.pf_start:
                            self.pf_start = None
                        if tile == self.pf_end:
                            self.pf_end = None
                            
            if event.type == pygame.MOUSEBUTTONUP:
                if self.dragging_token is not None:
                    for tower in self.towers:
                        if tower.rect.collidepoint(pygame.mouse.get_pos()) and not tower.has_gem:
                            pos = (tower.tile_pos[0] * self.tilemap.tile_size * self.render_scale, tower.tile_pos[1] * self.tilemap.tile_size * self.render_scale)
                            gem = self.gem_factory.build_gem(
                                self.dragging_token.gem_type,
                                self.dragging_token.tier,
                                self.dragging_token.star,
                                tower,
                                self.display)
                            tower.has_gem = True
                            self.gems.add(gem)
                            self.gem_stash.remove(self.dragging_token)
                            self.dragging_token = None
                self.dragging_token = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    self.build_mode = not self.build_mode
                if event.key == pygame.K_p:
                    self.debug_mode = not self.debug_mode
                if event.key == pygame.K_SPACE:
                    self.paused = not self.paused
                if event.key == pygame.K_ESCAPE:
                    self.build_mode = False
                if event.key == pygame.K_q:
                    self.fast_forward = not self.fast_forward
                    
    def _draw_ui(self):
        self.screen.blit(pygame.transform.scale(self.display, (1280, 720)), (0, 8))
        # Left bar
        pygame.draw.rect(self.screen, (41, 39, 43), pygame.Rect(0, 0, 32, 720))
        # Right bar
        pygame.draw.rect(self.screen, (41, 39, 43), pygame.Rect(1088, 0, 192, 720))
        # Top bar
        pygame.draw.rect(self.screen, (52, 47, 67), pygame.Rect(32, 0, 1056, 8))
        # Bottom bar
        pygame.draw.rect(self.screen, (52, 47, 67), pygame.Rect(32, 712, 1056, 8))

        # draw gem_stash
        hovered = self.gem_stash.get_token_at(pygame.mouse.get_pos())
        self.gem_stash.draw(hovered_token=hovered)

        for button in self.game_ui.buttons:
            button.draw_button(self.screen)
            if button.check_hover():
                button.draw_button_hover(self.screen)
                
        steel_text = "Current Steel: " + str(self.current_steel)
        wave_text = "Current Wave: " + str(self.current_wave)
        tower_build_text = str(self.tower_cost) + " Steel"
        gem_build_text = str(self.gem_cost) + " Steel"
        level_text = str(self.current_level)
        draw_text(self.screen, steel_text, self.text_font, (0, 0, 0), 1100, 70)
        draw_text(self.screen, level_text, self.text_font, (0, 0, 0), 1100, 100)
        draw_text(self.screen, wave_text, self.text_font, (0, 0, 0), 1100, 130)
        draw_text(self.screen, tower_build_text, self.text_font, (0, 0, 0), 1100, 375)
        draw_text(self.screen, gem_build_text, self.text_font, (0, 0, 0), 1195, 375)

        # Here we display our mouse
        self.screen.blit(self.assets['mouse_pointer'], self.screen_mpos)
        if self.dragging_token is not None:
            self.screen.blit(self.dragging_token.icon, 
                            (self.screen_mpos[0] - (self.tile_size / 2), 
                            self.screen_mpos[1] - (self.tile_size / 2)))
        
        for _tower in self.towers:
            if self.build_mode:
                break
            if _tower.check_hover():
                _tower.hover(self.screen)

        if not self.paused:
            if self.fast_forward:
                self.game_ui.update_wave_display(True)
            else:
                self.game_ui.update_wave_display() 
                
    def create_level_buttons(self):
        surf_width = self.screen.get_size()[0]
        Button(self.game_ui, 32, 32, (surf_width - 180, 20), 'pause',
           self.ui_assets["pause_button"],
           on_click=lambda: setattr(self, 'paused', True))
    
        Button(self.game_ui, 32, 32, (surf_width - 115, 20), 'play',
            self.ui_assets["play_button"],
            on_click=lambda: self.run_pathfinding())
        
        Button(self.game_ui, 32, 32, (surf_width - 50, 20), 'fast_forward',
            self.ui_assets["fast_forward_button"],
            on_click=lambda: setattr(self, 'fast_forward', not self.fast_forward))
        
        Button(self.game_ui, 64, 64, (surf_width - 180, 300), 'tower_button',
            self.ui_assets["tower_button_small"],
            on_click=lambda: self._enter_tower_build_mode())
        
        Button(self.game_ui, 64, 64, (surf_width - 80, 300), 'gem_button',
            self.ui_assets["gem_button_small"],
            on_click=lambda: self._draw_gem())
                
    def _update(self):
        # Here is where we can draw our background
        self.screen.fill(self.bg_color)
        self.display.fill(self.bg_color)
        self.tilemap.render(self.display)

        # here is where we manage the mouse position input
        self.screen_mpos = pygame.mouse.get_pos()

        self.mpos = ((self.screen_mpos[0] / self.render_scale), (self.screen_mpos[1] / self.render_scale))
        self.tile_pos = (
        int(self.mpos[0] // self.tilemap.tile_size), int(self.mpos[1] // self.tilemap.tile_size))

        # Here we are making sure our tile_position doesn't go out of bounds of the current game display area
        self._clamp_tile_pos()

        # Here is where we manage pathfinding
        if self.debug_mode:
            draw_pathfinding(self.display, self.pf_grid, ROWS, WIDTH)

        # Here is where we draw our static elements to the screen
        for player_tower in self.towers:
            player_tower.draw()
        for player_gem in self.gems:
            player_gem.draw()

        # Here is where we make our monsters move
        for enemy_monster in self.monsters:
            enemy_monster.draw(self.display)
            enemy_monster.update()

        # Here is where we check if the monster is in range of the turret
        for p_gem in self.gems:
            if len(self.monsters) > 0:
                p_gem.detect_monster()
            else:
                p_gem.valid_target = None
        for p_gem in self.gems:
            p_gem.update()

        # Here we handle display changes for hovering gout mouse over it
        for hoverable in self.hoverables:
            if hoverable.rect.collidepoint(self.screen_mpos):
                hoverable.on_hover()

        # Here we update our projectiles
        for player_gem in self.gems:
            for projectile in player_gem.projectiles:
                projectile.update()
                projectile.draw()

        # here is where we handle build mode
        if self.build_mode:
            self.build_display()
            
        self.run_level()

    def run(self):
        self._init_level()
        while True:
            if self.level.waves_finished and len(self.monsters) == 0:
                return self.end_level()
            
            self._update()
            
            self._handle_events()

            self._draw_ui()           

            pygame.display.update()
            self.dt = self.clock.tick(FPS) / 1000             
                