from os import walk
import pygame


def import_folder(path):
    surface_list = []

    for _, __, imgs in walk(path):
        for img in imgs:
            full_path = f"{path}/{img}"
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)

    return surface_list


def import_folder_dict(path):
    surface_dict = {}

    for _, __, imgs in walk(path):
        for img in imgs:
            full_path = f"{path}/{img}"
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_dict[img.split(".")[0]] = image_surf

    return surface_dict
