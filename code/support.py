from os import walk, path
import pygame, json


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


def encrypt(path):
    pass


def load_file():
    if path.exists("../saves/1.txt"):
        with open("../saves/1.txt") as save:
            data = json.load(save)
    else:
        with open("../saves/default.txt") as save:
            data = json.load(save)

    return data


def save_file(data):
    with open("../saves/1.txt", "w") as save:
        json.dump(data, save)
