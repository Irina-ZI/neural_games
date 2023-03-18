import random
import math
from sklearn.neural_network import MLPRegressor
import numpy as np
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

class Hive:
    def __init__(self):
        self.health = 100
        self.position = (50, 50)
        self.drones = [Drone(self) for _ in range(5)]
        self.hive_mind = MLPRegressor(hidden_layer_sizes=(10,), max_iter=1000)

    def lose_health(self):
        self.health -= 10

    def gain_health(self):
        self.health += 10

    def update(self, field):
        self.lose_health()

        X = []
        y = []

        for drone in self.drones:
            nearest_resource = drone.find_nearest_resource(field)
            if nearest_resource:
                x1, y1 = drone.position
                x2, y2 = nearest_resource
                distance_to_resource = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
                X.append([distance_to_resource])
                y.append([1])
            else:
                X.append([0])
                y.append([0])
        if len(X) > 0 and len(y) > 0:
            y = np.ravel(y)
            self.hive_mind.partial_fit(X, y)

            predictions = self.hive_mind.predict(X)

            drones_to_send = [drone for i, drone in enumerate(self.drones) if predictions[i] > 0.5]

            for drone in drones_to_send:
                drone.update(field)

class Drone:
    def __init__(self, hive):
        self.hive = hive
        self.position = (0, 0)
        self.carrying_resource = False

    def move_towards(self, target):
        x1, y1 = self.position
        x2, y2 = target
        distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        if distance > 0:
            dx = (x2 - x1) / distance
            dy = (y2 - y1) / distance
            self.position = (x1 + dx * min(distance, 1), y1 + dy * min(distance, 1))

    def find_nearest_resource(self, field):
      nearest_resource=None
      nearest_distance=float('inf')
      for resource in field.resources:
          x1,y1=self.position
          x2,y2=resource
          distance=math.sqrt((x2-x1)**2+(y2-y1)**2)
          if distance<nearest_distance:
              nearest_resource=resource
              nearest_distance=distance
      return nearest_resource

    def pick_up_resource(self, field):
      resource_to_pick_up=None
      for resource in field.resources:
          if math.isclose(resource[0],self.position[0]) and math.isclose(resource[1],self.position[1]):
              resource_to_pick_up=resource
              break
      if resource_to_pick_up:
          field.resources.remove(resource_to_pick_up)
          self.carrying_resource=True

    def pick_up_resource(self, field):
      resource_to_pick_up=None
      for resource in field.resources:
          if math.isclose(resource[0],self.position[0]) and math.isclose(resource[1],self.position[1]):
              resource_to_pick_up=resource
              break
      if resource_to_pick_up:
          field.resources.remove(resource_to_pick_up)
          self.carrying_resource=True
    def update(self, field):
        if not self.carrying_resource:
            nearest_resource = self.find_nearest_resource(field)
            if nearest_resource:
                self.move_towards(nearest_resource)
                self.pick_up_resource(field)
        else:
            self.move_towards(self.hive.position)
            if math.isclose(self.position[0], self.hive.position[0]) and math.isclose(self.position[1], self.hive.position[1]):
                self.carrying_resource = False
                self.hive.gain_health()

class Field:
    def __init__(self):
        self.resources = []

    def add_resource(self):
        x = random.randint(0, 100)
        y = random.randint(0, 100)
        self.resources.append((x, y))

# import matplotlib.pyplot as plt

# def visualize(field, hive):
#     plt.clf()
#     plt.xlim(0, 100)
#     plt.ylim(0, 100)
#     for resource in field.resources:
#         plt.scatter(*resource, c='g')
#     for drone in hive.drones:
#         if drone.carrying_resource:
#             plt.scatter(*drone.position, c='b')
#         else:
#             plt.scatter(*drone.position, c='r')
#     plt.scatter(*hive.position, c='y', s=200)
#     plt.pause(0.01)

# field = Field()
# hive = Hive()

# while True:
#     field.add_resource()
#     hive.update(field)
#     visualize(field, hive)

# plt.show()


# import arcade

# SCREEN_WIDTH = 600
# SCREEN_HEIGHT = 600
# SPRITE_SCALING = 0.5

# class Simulation(arcade.Window):
#     def __init__(self):
#         super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT)
#         self.field = Field()
#         self.hive = Hive()
#         self.resource_list = arcade.SpriteList()
#         self.drone_list = arcade.SpriteList()

#     def setup(self):
#         for resource in self.field.resources:
#             resource_sprite = arcade.Sprite("resource.png", SPRITE_SCALING)
#             resource_sprite.center_x = resource[0] / 100 * SCREEN_WIDTH
#             resource_sprite.center_y = resource[1] / 100 * SCREEN_HEIGHT
#             self.resource_list.append(resource_sprite)

#         for drone in self.hive.drones:
#             drone_sprite = arcade.Sprite("drone.png", SPRITE_SCALING)
#             drone_sprite.center_x = drone.position[0] / 100 * SCREEN_WIDTH
#             drone_sprite.center_y = drone.position[1] / 100 * SCREEN_HEIGHT
#             self.drone_list.append(drone_sprite)

#     def on_draw(self):
#         arcade.start_render()
#         self.resource_list.draw()
#         self.drone_list.draw()

#     def update(self, delta_time):
#         self.field.add_resource()
#         self.hive.update(self.field)

# simulation_window = Simulation()
# simulation_window.setup()

# arcade.run()


import pygame

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

class Simulation:
    def __init__(self):
        self.field = Field()
        self.hive = Hive()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.resource_image = pygame.image.load("resource.png")
        self.drone_image = pygame.image.load("drone.png")

    def draw(self):
        self.screen.fill((255, 255, 255))
        for resource in self.field.resources:
            x = int(resource[0] / 100 * SCREEN_WIDTH)
            y = int(resource[1] / 100 * SCREEN_HEIGHT)
            self.screen.blit(self.resource_image, (x, y))

        for drone in self.hive.drones:
            x = int(drone.position[0] / 100 * SCREEN_WIDTH)
            y = int(drone.position[1] / 100 * SCREEN_HEIGHT)
            if drone.carrying_resource:
                color = (0, 0, 255)
            else:
                color = (255, 0, 0)
            self.screen.blit(self.drone_image,(x,y))

    def update(self):
        self.field.add_resource()
        self.hive.update(self.field)

simulation_window=Simulation()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    simulation_window.update()
    simulation_window.draw()
    pygame.display.flip()
