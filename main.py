import pygame
import random
import sys

import Creature_Class
import Sustenance

pygame.init()

WIDTH, HEIGHT = 800, 600
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Test")

clock = pygame.time.Clock()


# Generate creatures
creatures = [Creature_Class.Creature(WIDTH, HEIGHT) for _ in range(2)]
for creature in creatures:
    print(creature.genes, creature.x, creature.y)

# Make water and food sources
water_sources = Sustenance.generate_water(WIDTH, HEIGHT)
food_sources = Sustenance.generate_food(WIDTH, HEIGHT)

# Main loop
running = True
while running:
    clock.tick(FPS) # Frame rate limit
    delta_time = clock.tick(60) / 1000.0

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # update denizens
    for c in creatures:
        c.update(delta_time)
        c.lifetime_counter()
        c.needs_counter()
        c.behavior_controller(water_sources, food_sources)
        c.see_others(creatures)

    screen.fill((30, 30, 30))

    # Draw water and food
    for pos, size, color, tag in water_sources:
        pygame.draw.circle(screen, color, pos, size)
    for pos, size, color, tag in food_sources:
        pygame.draw.circle(screen, color, pos, size)

    # draw creatures
    for c in creatures:
        c.draw(screen)
        c.vision_range(screen) # vision visualizer
    
    creatures = [c for c in creatures if c.alive]

    pygame.display.flip() # Refresh screen

pygame.quit()
sys.exit()