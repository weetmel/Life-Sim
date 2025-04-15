import pygame
import random


def generate_water(width, height):
    water_sources = []
    for i in range(random.randint(2,4)):
        pos = (random.randint(30, width - 30), random.randint(30, height - 30))
        size = random.randint(75,150)
        color = pygame.Color("skyblue")
        water_sources.append((pos, size, color, 'water'))
    return water_sources

def generate_food(width, height):
    food_sources = []
    for i in range(random.randint(5,9)):
        pos = (random.randint(10, width - 10), random.randint(10, height - 10))
        size = random.randint(10,30)
        color = pygame.Color((255, 67, 0))
        food_sources.append((pos, size, color, 'food'))
    return food_sources