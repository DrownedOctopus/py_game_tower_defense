import os
import pygame

os.chdir('.')

BASE_IMG_PATH = r"art/"
BASE_AUDIO_PATH = r"audio/"
pygame.init()
pygame.mixer.init()
pygame.display.set_caption("tower defense game")
pygame.display.set_mode((1280, 720))

sfx_assets = {
    'fire': pygame.mixer.Sound(BASE_AUDIO_PATH + "laser_bolt.mp3"),
    'build': pygame.mixer.Sound(BASE_AUDIO_PATH + "build_noise.mp3"),
    'button': pygame.mixer.Sound(BASE_AUDIO_PATH + 'button_press.mp3'),
    'death_1': pygame.mixer.Sound(BASE_AUDIO_PATH + 'death_noise_1.mp3'),
    'death_2': pygame.mixer.Sound(BASE_AUDIO_PATH + 'death_noise_2.mp3'),
    'BGM_Menu': BASE_AUDIO_PATH + 'BGM_Menu.wav',
    'BGM_Game_1': BASE_AUDIO_PATH + 'BGM_Game_1.wav',
    'BGM_Game_2': BASE_AUDIO_PATH + 'BGM_Game_2.wav'
}

vfx_assets = {
    'projectile_img_sheet': [pygame.image.load('art/round_bullets_small.png').convert_alpha(), 6, 8]
}


def get_sheet_dim(sheet):
    max_frame_width = vfx_assets[sheet][1]
    max_frame_height = vfx_assets[sheet][2]
    return max_frame_width, max_frame_height


def get_image(sheet, frame, width, height):
    image = pygame.Surface((width, height)).convert_alpha()
    image.blit(vfx_assets[sheet][0], (0, 0), ((frame[0] * width), (frame[1] * width), width, height))
    image.set_colorkey((0, 0, 0))

    return image

def play_audio(sound, loop=False):
    if loop:
        print(sfx_assets[sound])
        pygame.mixer.music.load(sfx_assets[sound])
        pygame.mixer.music.play(-1, 0.0)
        return
    sfx_assets[sound].play()


def load_image(path):
    img = pygame.image.load(BASE_IMG_PATH + path).convert()
    img.set_colorkey((0, 0, 0))
    return img


# This script loads a whole folder of images based on the specified folder
def load_images(path):
    images = []
    for img_name in os.listdir(BASE_IMG_PATH + path):
        images.append(load_image(path + '/' + img_name))
    return images


def draw_text(surf, text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    surf.blit(img, (x, y))
