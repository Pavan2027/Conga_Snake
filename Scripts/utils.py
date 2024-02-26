import pygame

BASE_IMG_PATH = 'Assets/'

def load_image(path):
    img = pygame.image.load(BASE_IMG_PATH + path)
    img = pygame.transform.scale(img, (39, 48)) 
    img.set_colorkey((0, 0, 0))
    return img