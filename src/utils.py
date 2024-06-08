import csv
# world_size = namedtuple('Size', ['width','length'])
import os
import pygame
import sys

from collections import namedtuple

# Define the size of the game world
world_size = (21 * 64, 14 * 64)

# Define some basic colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Define the size of basic entities
basic_entity_size = (64, 64)

# Define a list of wall tiles
# wall_list = (135, 15, 17, 60, 61, 62, 63, 1, 18, 3, 46, 45, 40, 42, 47, 0, 30, 2, 32, 33, 3)
wall_list = (1, 2, 3, 33, 34, 35, 67, 99, 224, 227, 225, 226, 256, 257, 258, 259, 288, 289)

# Define a list of floor tiles
floor_tiles = [129, 130, 131, 161, 162, 163, 193, 194]

# Define the font path
font = './assets/font/Minecraft.ttf'

# Define wall side tiles
wall_side_left, wall_side_right = 256, 257
wall_side_left_top, wall_side_right_top = 224, 225
wall_side_front_left, wall_side_front_right = 288, 289

# Placeholder for map center
map_center = []


def resource_path(relative_path):
    """
    Get the absolute path to a resource, works for dev and for PyInstaller.

    Parameters
    ----------
    relative_path : str
        The relative path to the resource.

    Returns
    -------
    str
        The absolute path to the resource.
    """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def read_csv(filename):
    """
    Reads a CSV file and returns a 2D list of its contents.

    Parameters
    ----------
    filename : str
        The path to the CSV file.

    Returns
    -------
    list
        A 2D list where each sublist represents a row in the CSV file.
    """
    mapa = []
    with open(os.path.join(filename)) as data:
        data = csv.reader(data, delimiter=',')
        for row in data:
            mapa.append(list(row))
            mapa.append(list(row))
    return mapa


def get_mask_rect(surf, top=0, left=0):
    """
    Returns the minimal bounding rectangle of an image.

    Parameters
    ----------
    surf : pygame.Surface
        The surface to get the bounding rectangle for.
    top : int, optional
        The top offset for the rectangle (default is 0).
    left : int, optional
        The left offset for the rectangle (default is 0).

    Returns
    -------
    pygame.Rect
        The minimal bounding rectangle of the image.
    """
    surf_mask = pygame.mask.from_surface(surf)
    rect_list = surf_mask.get_bounding_rects()
    if rect_list:
        surf_mask_rect = rect_list[0].unionall(rect_list)
        surf_mask_rect.move_ip(top, left)
        return surf_mask_rect


def wait(mil_sec, game):
    """
    Waits for a specified amount of milliseconds.

    Parameters
    ----------
    mil_sec : int
        The number of milliseconds to wait.
    game : Game
        The game instance to check the counter against.

    Returns
    -------
    bool
        True if the specified time has passed, otherwise False.
    """
    ticks = mil_sec / 16
    if game.counter == game.counter + ticks:
        return True


def time_passed(time, amount):
    """
    Checks if a certain amount of time has passed since a given time.

    Parameters
    ----------
    time : int
        The initial time in milliseconds.
    amount : int
        The amount of time to check in milliseconds.

    Returns
    -------
    bool
        True if the specified amount of time has passed, otherwise False.
    """
    if pygame.time.get_ticks() - time > amount:
        time = pygame.time.get_ticks()
        return True
