import pygame
import random
import sys
import time
import math

# class Creature:
#     def __init__(self, WIDTH, HEIGHT):
#         self.state = 'idle'
#         self.x = random.randint(0, WIDTH)
#         self.y = random.randint(0, HEIGHT)
#         self.idle_angle = random.uniform(0, 2 * math.pi)

#         self.birth_time = time.time()
#         self.starve_timer = time.time()
#         self.thirst_timer = time.time()
#         self.alive = True

#         self.genes = determine_genes()

#         self.speed_gene = self.genes[0][1]
#         self.vision_gene = self.genes[1][1]
#         self.color = self.genes[2][1]
#         self.lifetime = self.genes[3][1]
#         self.hunger_max = self.genes[4][1]
#         self.thirst_max = self.genes[5][1]

#         self.radius = 5
#         self.screen_width = WIDTH
#         self.screen_height = HEIGHT
    

#     def behavior_controller(self, water_sources, food_sources):
#         self.hunger = time.time() - self.starve_timer
#         self.thirst = time.time() - self.thirst_timer
        
#         if not self.alive:
#             return
        
#         if self.state == 'idle':
#             # print('idle')
#             self.idle()
#             if self.hunger >= (self.hunger_max / 2):
#                 # print('hungry')
#                 self.state = 'seek_food'
#             if self.thirst >= (self.thirst_max / 2):
#                 # print('thirsty')
#                 self.state = 'seek_water'

#         elif self.state == 'seek_food':
#             print('seeking food', self.hunger)
#             self.wander(water_sources, food_sources)
#             self.see_resource(food_sources)

#         elif self.state == 'seek_water':
#             print('seeking water', self.thirst)
#             self.wander(water_sources, food_sources)
#             self.see_resource(water_sources)
        

#     def idle(self):
#         self.idle_angle += random.uniform(-0.75, 0.75)  # wiggle the angle

#         # Random movement
#         self.x += math.cos(self.idle_angle) * self.speed_gene * 0.3
#         self.y += math.sin(self.idle_angle) * self.speed_gene * 0.3

#         # Stay in bounds
#         self.x = max(0, min(self.screen_width, self.x))
#         self.y = max(0, min(self.screen_height, self.y))
    

#     def wander(self, water_sources, food_sources):
#         # If we don't already have a wander target, choose one
#         if not hasattr(self, 'wander_target') or self.reached_target():
#             self.wander_target = (
#                 random.randint(0, self.screen_width),
#                 random.randint(0, self.screen_height)
#             )

#         dest_x, dest_y = self.wander_target
#         dx = dest_x - self.x
#         dy = dest_y - self.y
#         distance = math.hypot(dx, dy)

#         if distance > 0:
#             self.x += (dx / distance) * self.speed_gene
#             self.y += (dy / distance) * self.speed_gene
        
#         # Stay in bounds
#         self.x = max(0, min(self.screen_width, self.x))
#         self.y = max(0, min(self.screen_height, self.y))

    
#     def direct_move(self, destination):
#         dest_x, dest_y = destination
#         dx = dest_x - self.x
#         dy = dest_y - self.y
#         distance = math.hypot(dx, dy)

#         if distance > 0:
#             self.x += (dx / distance) * self.speed_gene
#             self.y += (dy / distance) * self.speed_gene
#             return False
#         elif distance <= 0:
#             return True
#         return False


#     def reached_target(self):
#         if not hasattr(self, 'wander_target'):
#             return True
#         dest_x, dest_y = self.wander_target
#         return math.hypot(dest_x - self.x, dest_y - self.y) < 5  # pixels
    

#     def see_resource(self, resource):
#         for pos, radius, color, tag in resource:
#             dist_x = pos[0] - self.x
#             dist_y = pos[1] - self.y
#             distance_to = math.hypot(dist_x, dist_y)

#             if distance_to <= self.vision_gene + radius:
#                 # print("RESOURCE SIGHTED!")
#                 self.consume(pos, radius, tag)
#         return


#     def consume(self, pos, radius, tag):
#         resource_reached = self.direct_move(pos)
#         if resource_reached == True:
#             if tag == 'water':
#                 self.thirst_timer = 0
#                 print('drank to: ', time.time() - self.thirst_timer)
#             if tag == 'food':
#                 self.starve_timer = 0
#                 print('ate to: ', self.hunger)


#     def lifetime_counter(self):
#         if time.time() - self.birth_time >= self.lifetime:
#             print("Died from old age")
#             self.alive = False
    

#     def needs_counter(self):
#         if time.time() - self.starve_timer >= self.hunger_max:
#             print("Died from starvation")
#             self.alive = False
#         if time.time() - self.thirst_timer >= self.thirst_max:
#             print("Died from thirst")
#             self.alive = False


#     def draw(self, screen):
#         pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
    
#     def vision_range(self, screen):
#         pygame.draw.circle(screen, pygame.Color("white"), (int(self.x), int(self.y)), self.vision_gene, 1)
    
class Creature:
    def __init__(self, WIDTH, HEIGHT):
        self.state = 'idle'
        self.target_pos = None
        self.target_radius = 0
        self.target_tag = None
        self.reached_resource = False
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.idle_angle = random.uniform(0, 2 * math.pi)

        self.birth_time = 0
        self.hunger = 0
        self.thirst = 0
        self.alive = True

        self.genes = determine_genes()

        self.speed_gene = self.genes[0][1]
        self.vision_gene = self.genes[1][1]
        self.color = self.genes[2][1]
        self.lifetime = self.genes[3][1]
        self.hunger_max = self.genes[4][1]
        self.thirst_max = self.genes[5][1]

        self.radius = 5
        self.screen_width = WIDTH
        self.screen_height = HEIGHT


    def update(self, delta_time):
        self.hunger += delta_time
        self.thirst += delta_time
        self.birth_time += delta_time


    def lifetime_counter(self):
        if self.birth_time >= self.lifetime:
            print("Died from old age")
            self.alive = False


    def needs_counter(self):
        if self.hunger >= self.hunger_max:
            print("Died from starvation")
            self.alive = False
        if self.thirst >= self.thirst_max:
            print("Died from thirst")
            self.alive = False


    def behavior_controller(self, water_sources, food_sources):
        if not self.alive:
            return

        if self.state == 'idle':
            self.idle()
            if self.hunger >= (self.hunger_max / 2):
                self.state = 'seek_food'
            elif self.thirst >= (self.thirst_max / 2):
                self.state = 'seek_water'

        elif self.state == 'seek_food':
            if not self.target_pos:
                self.wander(water_sources, food_sources)
                self.see_resource(food_sources)
            else:
                arrived = self.direct_move(self.target_pos, self.target_radius)
                if arrived:
                    self.consume(self.target_tag)
                    self.target_pos = None

        elif self.state == 'seek_water':
            if not self.target_pos:
                self.wander(water_sources, food_sources)
                self.see_resource(water_sources)
            else:
                arrived = self.direct_move(self.target_pos, self.target_radius)
                if arrived:
                    self.consume(self.target_tag)
                    self.target_pos = None


    def idle(self):
        self.idle_angle += random.uniform(-0.75, 0.75)
        self.x += math.cos(self.idle_angle) * self.speed_gene * 0.3
        self.y += math.sin(self.idle_angle) * self.speed_gene * 0.3
        self.x = max(0, min(self.screen_width, self.x))
        self.y = max(0, min(self.screen_height, self.y))


    def wander(self, water_sources, food_sources):
        # print('wander')
        if not hasattr(self, 'wander_target') or self.reached_target():
            self.wander_target = (
                random.randint(0, self.screen_width),
                random.randint(0, self.screen_height)
            )

        dest_x, dest_y = self.wander_target
        dx = dest_x - self.x
        dy = dest_y - self.y
        distance = math.hypot(dx, dy)

        if distance > 0:
            self.x += (dx / distance) * self.speed_gene
            self.y += (dy / distance) * self.speed_gene

        self.x = max(0, min(self.screen_width, self.x))
        self.y = max(0, min(self.screen_height, self.y))


    def direct_move(self, destination, tag, target_radius=0):
        dest_x, dest_y = destination
        dx = dest_x - self.x
        dy = dest_y - self.y
        distance = math.hypot(dx, dy)

        threshold = target_radius + self.radius + 2

        if distance > threshold:
            step = min(self.speed_gene, distance)
            self.x += (dx / distance) * step
            self.y += (dy / distance) * step
            return False
            # print('SEARCHING')
        else:
            return True
            # print("ARRIVED")
            

    def reached_target(self):
        if not hasattr(self, 'wander_target'):
            return True
        dest_x, dest_y = self.wander_target
        return math.hypot(dest_x - self.x, dest_y - self.y) < 5
    

    def see_resource(self, resource):
        # print('see resource')
        for pos, radius, color, tag in resource:
            dist_x = pos[0] - self.x
            dist_y = pos[1] - self.y
            distance_to = math.hypot(dist_x, dist_y)

            if distance_to <= self.vision_gene + radius:
                self.target_pos = pos
                self.target_radius = radius
                self.target_tag = tag
                return  # Only chase the first visible resource for now


    def consume(self, tag):
        if tag == 'water':
            self.thirst = 0
            self.state = 'idle'
            print('drank to:', self.thirst)
        if tag == 'food':
            self.hunger = 0
            self.state = 'idle'
            print('ate to:', self.hunger)


    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)


    def vision_range(self, screen):
        pygame.draw.circle(screen, pygame.Color("white"), (int(self.x), int(self.y)), self.vision_gene, 1)


def determine_genes():
    speed_gene = ['Speed', random.randint(1,5)]
    vision_gene = ['Vision', random.randint(100, 200)]
    color_gene = ['Color', (random.randint(0,255) ,random.randint(0,255), random.randint(0,255))]
    lifetime_gene = ['Lifetime', random.randint(60,90)]
    hunger_max_gene = ['Hunger Max', random.randint(30,45)]
    thirst_max_gene = ['Thirst Max', random.randint(25,40)]

    genetic_code = [speed_gene, vision_gene, color_gene, lifetime_gene, hunger_max_gene, thirst_max_gene]

    return genetic_code

