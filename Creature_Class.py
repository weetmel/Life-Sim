import pygame
import random
import sys
import time
import math
    
class Creature:
    def __init__(self, is_offspring, spawn_x=0, spawn_y=0, width=0, height=0, genetic_code=[], parents=None):
        self.state = 'idle'
        self.target_pos = None
        self.target_radius = 0
        self.target_tag = None
        self.reached_resource = False
        if not is_offspring:
            self.x = random.randint(0, width)
            self.y = random.randint(0, height)
        else:
            self.x = spawn_x
            self.y = spawn_y
        self.idle_angle = random.uniform(0, 2 * math.pi)

        self.birth_time = 0
        self.hunger = 0
        self.thirst = 0  
        self.alive = True

        if not is_offspring:
            self.genes = determine_genes()
        else:
            self.genes = genetic_code

        self.speed_gene = self.genes[0][1]
        self.vision_gene = self.genes[1][1]
        self.color = self.genes[2][1]
        self.lifetime = self.genes[3][1]
        self.hunger_max = self.genes[4][1]
        self.thirst_max = self.genes[5][1]
        if parents is None:
            parents = set([random.randint(0, 1000), random.randint(0, 1000)])
        self.parents = parents

        print(self.parents)

        self.visible_creatures = []
        self.viable_mates = []
        self.horny = False
        self.offspring = None
        self.reproduced = False
        self.maturity_level = 0
        self.maturity_timer = 30
        self.mature = False

        self.radius = 5
        self.screen_width = width
        self.screen_height = height


    def behavior_controller(self, water_sources, food_sources):
        if not self.alive:
            return

        if self.state == 'idle':
            self.idle()
        
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
        
        elif self.state == 'seek_mate':
            self.horny = True
            if not self.target_pos:
                self.wander(water_sources, food_sources)
                self.find_mate()
            else:
                arrived = self.direct_move(self.target_pos, self.target_radius)
                if arrived:
                    self.make_offspring(self.target_pos)
                    self.target_pos = None
                    self.target_radius = None
                    self.state = 'idle'

            # print("me so horny")

         
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)


    def vision_range(self, screen):
        pygame.draw.circle(screen, pygame.Color("white"), (int(self.x), int(self.y)), self.vision_gene, 1)


    def update(self, delta_time):
        self.hunger += delta_time
        self.thirst += delta_time
        self.birth_time += delta_time
        self.maturity_level += delta_time
        if self.maturity_level >= self.maturity_timer:
            self.mature = True

        if self.hunger >= (self.hunger_max / 2):
                self.state = 'seek_food'
        elif self.thirst >= (self.thirst_max / 2):
            self.state = 'seek_water'
        elif (self.hunger <= (self.hunger_max / 2)) and (self.thirst <= (self.thirst_max / 2)) and not self.reproduced and self.mature:
            self.state = 'seek_mate'


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


    def reached_target(self):
        if not hasattr(self, 'wander_target'):
            return True
        dest_x, dest_y = self.wander_target
        return math.hypot(dest_x - self.x, dest_y - self.y) < 5


    def direct_move(self, destination, tag = '', target_radius=0):
        try:
            dest_x, dest_y = destination
        except:
            dest_x, dest_y = destination.x, destination.y
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
    
    def see_others(self, creatures):
        self.visible_creatures.clear()  # reset the list every frame

        for creature in creatures:
            if creature is self:
                continue
            dist_x = creature.x - self.x
            dist_y = creature.y - self.y
            distance_to = math.hypot(dist_x, dist_y)

            if distance_to <= self.vision_gene + creature.radius:
                if creature not in self.visible_creatures:
                    self.visible_creatures.append(creature)

        self.viable_mates = [mate for mate in self.viable_mates if mate in self.visible_creatures]
        # print(f'I can see {len(self.visible_creatures)} other creatures!')
        
    
    def find_mate(self):
        for creature in self.visible_creatures:
            if creature is self:
                continue
            if creature.horny and (creature.mature) and (not creature.reproduced) and (creature.parents != self.parents) and (creature not in self.parents):
                if creature not in self.viable_mates:
                    self.viable_mates.append(creature)
                    self.target_pos = self.viable_mates[len(self.viable_mates) - 1]
                    self.target_radius = creature.radius
            elif not creature.horny:
                if creature in self.viable_mates:
                    self.viable_mates.remove(creature)

        # print(f'I can see {len(self.viable_mates)} viable mates!')


    def make_offspring(self, mate):
        print(self.maturity_level, mate.maturity_level)
        offspring_genes = average_genes(self.genes, mate.genes)
        offspring = Creature(is_offspring=True, spawn_x=self.x, spawn_y=self.y, width=self.screen_width, height=self.screen_height, genetic_code=offspring_genes, parents=set([self, mate]))
        self.offspring = offspring
        self.reproduced = True
        self.state = 'idle'


    def consume(self, tag):
        if tag == 'water':
            self.thirst = 0
            self.state = 'idle'
            print('drank to:', self.thirst)
        if tag == 'food':
            self.hunger = 0
            self.state = 'idle'
            print('ate to:', self.hunger)
 

def determine_genes():
    speed_gene = ['Speed', random.randint(1,5)]
    vision_gene = ['Vision', random.randint(100, 200)]
    color_gene = ['Color', (random.randint(0,255) ,random.randint(0,255), random.randint(0,255))]
    lifetime_gene = ['Lifetime', random.randint(60,90)]
    hunger_max_gene = ['Hunger Max', random.randint(20,35)]
    thirst_max_gene = ['Thirst Max', random.randint(15,30)]

    genetic_code = [speed_gene, vision_gene, color_gene, lifetime_gene, hunger_max_gene, thirst_max_gene]

    return genetic_code

def average_genes(gene1, gene2):
        result = []
         # Average first two ints
        result.append(['Speed', (gene1[0][1] + gene2[0][1]) / 2])
        result.append(['Vision', (gene1[1][1] + gene2[1][1]) / 2])

        # Average the RGB tuple
        color1 = gene1[2][1]
        color2 = gene2[2][1]
        averaged_color = tuple((c1 + c2) // 2 for c1, c2 in zip(color1, color2))
        result.append(['Color', averaged_color])

        # Average the remaining ints
        for i in range(3, len(gene1)):
            if i == 3:
                string = 'Lifetime'
            elif i == 4:
                string = 'Hunger Max'
            elif i == 5:
                string = 'Thirst Max'
            result.append([string, ((gene1[i][1] + gene2[i][1]) / 2)]) 
        return result

