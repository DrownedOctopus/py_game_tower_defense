import pygame, os, json

BASE_IMG_PATH = r"art/"

def load_image(path):
    img = pygame.image.load(BASE_IMG_PATH + path).convert()
    img.set_colorkey((0, 0, 0))
    return img

def load_mask(path):
    mask = pygame.image.load(BASE_IMG_PATH + path)
    return mask

def load_images(path):
    images = []
    for img_name in os.listdir(BASE_IMG_PATH + path):
        images.append(load_image(path + '/' + img_name))
    return images

def load_sheet_images(sheet, sheet_assets):
    size = sheet_assets[sheet][1]
    rows = sheet_assets[sheet][2]
    cols = sheet_assets[sheet][3]
    images = []
    for row in range(1, rows):
        for col in range(1, cols):
            image = pygame.Surface((size, size)).convert_alpha()
            image.blit(sheet_assets[sheet][0], (0, 0), ((row * size), (col * size), size, size))
            image.set_colorkey((0, 0, 0))
            images.append(image)
    return images

def get_image(sheet, frame, width, height, sheet_assets):
    image = pygame.Surface((width, height)).convert_alpha()
    image.blit(sheet_assets[sheet][0], (0, 0), ((frame[0] * width), (frame[1] * width), width, height))
    image.set_colorkey((0, 0, 0))
    return image

def get_sheet_dim(sheet, sheet_assets):
    max_frame_width = sheet_assets[sheet][1]
    max_frame_height = sheet_assets[sheet][2]
    return max_frame_width, max_frame_height

def load_monsters(path):
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Monster data file not found: {path}")
        return None
    except json.JSONDecodeError as e:
        print(f"Monster data file is malformed: {e}")
        return None
    except PermissionError:
        print(f"Permission denied when loading monster data: {path}")
        return None