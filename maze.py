import numpy
from numpy.random import random_integers as rand
import pygame

pygame.init()
pygame.mixer.music.load('slender_foley.wav')
pygame.mixer.music.play(-1)
step = pygame.mixer.Sound('step.wav')
#enemy_vision = pygame.mixer.Sound("slender_2.wav")
#enemy_range = pygame.mixer.Sound('slender_3.wav')


def initialize_maze():
    maze_height = 40
    maze_width = 80
    maze_attributes = {'entry': [
        0, 0]}
    maze_attributes['shape'] = (
        (maze_height // 2) * 2 + 1, (maze_width // 2) * 2 + 1)
    maze_attributes['exit'] = [0, 0]
    maze_attributes['walls'] = numpy.zeros(
        maze_attributes['shape'], dtype=bool)
    return maze_attributes


def generate_maze_walls(maze_attributes, game_state):

    complexity = .85
    density = .85
    # Only odd shapes
    # Adjust complexity and density relative to maze size
    # number of components
    complexity = int(
        complexity * (5 * (maze_attributes['shape'][0] + maze_attributes['shape'][1])))
    # size of components
    density = int(
        density * ((maze_attributes['shape'][0] // 2) * (maze_attributes['shape'][1] // 2)))
    # Build actual maze

    # Fill borders
    maze_attributes['walls'][0, :] = maze_attributes['walls'][-1, :] = 1
    maze_attributes['walls'][:, 0] = maze_attributes['walls'][:, -1] = 1
    # Make aisles
    for i in range(density):
        x, y = rand(0, maze_attributes['shape'][1] // 2) * 2, rand(0,
                                                                   maze_attributes['shape'][0] // 2) * 2
        # pick a random position
        maze_attributes['walls'][y, x] = 1
        for j in range(complexity):
            neighbours = []
            if x > 1:
                neighbours.append((y, x - 2))
            if x < maze_attributes['shape'][1] - 2:
                neighbours.append((y, x + 2))
            if y > 1:
                neighbours.append((y - 2, x))
            if y < maze_attributes['shape'][0] - 2:
                neighbours.append((y + 2, x))
            if len(neighbours):
                y_, x_ = neighbours[rand(0, len(neighbours) - 1)]
                if maze_attributes['walls'][y_, x_] == 0:
                    maze_attributes['walls'][y_, x_] = 1
                    maze_attributes['walls'][y_ +
                                             (y - y_) // 2, x_ + (x - x_) // 2] = 1
                    x, y = x_, y_
    maze_attributes['entry'] = [0, 1]
    maze_attributes['exit'] = [maze_attributes['shape']
                               [0] // 2, maze_attributes['shape'][1] // 2]

    maze_attributes['walls'][maze_attributes['entry']
                             [0], maze_attributes['entry'][1]] = 0
    maze_attributes['walls'][maze_attributes['exit']
                             [0], maze_attributes['exit'][1]] = 0

    return maze_attributes['walls']