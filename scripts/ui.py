import pygame
from scripts.utils.assets import load_image
from scripts.utils.ui_utils import build_context_panel

BUTTON_HEIGHT = 80
FONT_PARENT = "fonts/Bandwidth8x8.ttf"


class UI:
    def __init__(self, scene, display):
        self.scene = scene
        self.buttons = []
        self.font = pygame.font.Font(FONT_PARENT, 50)   
        self.sub_font = pygame.font.Font(FONT_PARENT, 30)
        self.wave_font = pygame.font.Font(FONT_PARENT, 20)
        self.context_font = pygame.font.Font(FONT_PARENT, 10)
        self.info_font = pygame.font.Font(FONT_PARENT, 8)
        self.font_color = (198, 172, 201)
        self.context_text_color = (220, 220, 220)
        self.info_text_color = (247, 226, 107)
        self.wave_data = None
        self.monster_data = None
        self.display = display

        self.assets = {
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

    def create_level_buttons(self, surf):
        surf_width = surf.get_size()[0]
        
        # Control buttons - top right area
        pause_button = Button(self, 32, 32, (surf_width - 180, 20), 'pause', self.assets["pause_button"])
        start_button = Button(self, 32, 32, (surf_width - 115, 20), 'play', self.assets["play_button"])
        fast_forward_button = Button(self, 32, 32, (surf_width - 50, 20), 'fast_forward', self.assets["fast_forward_button"])

        # Build buttons - middle right area
        tower_button = Button(self, 64, 64, (surf_width - 180, 300), 'tower_button', self.assets["tower_button_small"])
        gem_button = Button(self, 64, 64, (surf_width - 80, 300), 'gem_button', self.assets["gem_button_small"])

    def check_click(self):
        for button in self.buttons:
            if self.scene == "ow_map":
                if button.rect.collidepoint(pygame.mouse.get_pos()[0] / 2, pygame.mouse.get_pos()[1] / 2):
                    # play_audio('button')
                    button.handle_click()
                    return button.name
            if button.rect.collidepoint(pygame.mouse.get_pos()):
                # play_audio('button')
                button.handle_click()
                return button.name
        return None

    def create_wave_display(self, waves, monster_data):
        self.wave_data = waves
        self.monster_data = monster_data
        for count, wave in enumerate(waves):
            w_data = wave
            wave_button = Button(self, 32, BUTTON_HEIGHT, (0, int(BUTTON_HEIGHT * count)), ('w', + count), self.assets['wave_button'], self.assets['wave_button_hover'], w_data)

    def update_wave_display(self, dt):
        pixels_per_second = BUTTON_HEIGHT / 14
        movement = pixels_per_second * dt
        for button in self.buttons:
            if button.name[0] == 'w':
                button.pos = (button.pos[0], button.pos[1] - movement)
                if button.pos[1] < 0:
                    self.buttons.remove(button)
                    

class Button:
    def __init__(self, ui, width, height, pos, name, img=None, hover_img=None, context=None, on_click=None):
        self.ui = ui
        self.width, self.height = width, height
        self.pos = pos
        self.rect = pygame.Rect(pos[0], pos[1], self.width, self.height)
        self.img = img
        self.hover_img = hover_img
        self.name = name
        self.context = context
        self.on_click = on_click
        ui.buttons.append(self)
        
    def handle_click(self):
        if self.on_click:
            self.on_click()

    def draw_button(self, surf):
        if self.img is not None:
            surf.blit(self.img, self.pos)
            if self.name[0] == 'w':
                wave_num = str(self.name[1] + 1)
                wave_num = self.ui.wave_font.render(wave_num, True, self.ui.font_color)
                wave_num_rect = wave_num.get_rect(center=(self.rect.width / 2, self.pos[1] + 70))
                surf.blit(wave_num, wave_num_rect)

    def draw_button_hover(self, surf):
        if self.hover_img is not None:
            surf.blit(self.hover_img, self.pos)
        if self.context is not None:
            self.draw_context(surf)

    def draw_context(self, surf):
        if self.name and self.name[0] == 'w':
            mpos = pygame.mouse.get_pos()
            width, height = 350, 200
            wave_data = self.ui.wave_data[self.name[1]]
            
            label_text = self.ui.context_font.render(
                'Wave ' + str(self.name[1] + 1) + ' of ' + str(len(self.ui.wave_data)), 
                True, self.ui.context_text_color)
            
            s, context_pos = build_context_panel(mpos, width, height, label_text, self.ui.display.get_width())

            text = str(wave_data[0]) + ' ' + str(wave_data[1])
            enemy_count_text = self.ui.context_font.render(text, True, self.ui.context_text_color)
            s.blit(enemy_count_text, enemy_count_text.get_rect(center=(width / 2, 45)))

            text = 'Hitpoints: ' + str(wave_data[2])
            hit_points_text = self.ui.context_font.render(text, True, self.ui.context_text_color)
            s.blit(hit_points_text, hit_points_text.get_rect(center=(width / 2, 80)))

            monster_type = wave_data[1]
            speed = self.ui.monster_data[monster_type]["move_speed"]
            speed_text = self.ui.context_font.render('Speed: ' + str(speed), True, self.ui.context_text_color)
            s.blit(speed_text, speed_text.get_rect(center=(width / 2, 105)))

            steel = self.ui.monster_data[monster_type]["steel_value"]
            steel_text = self.ui.context_font.render('Steel gain per kill: ' + str(steel), True, self.ui.context_text_color)
            s.blit(steel_text, steel_text.get_rect(center=(width / 2, 130)))

            info_text = self.ui.info_font.render('Click to start this and all waves above now', True, self.ui.info_text_color)
            s.blit(info_text, info_text.get_rect(center=(width / 2, 175)))

            surf.blit(s, context_pos)

    def check_hover(self):
        if self.ui.scene == "ow_map":
            if self.rect.collidepoint(pygame.mouse.get_pos()[0] / 2, pygame.mouse.get_pos()[1] / 2):
                return True
        else:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                return True
        return False
