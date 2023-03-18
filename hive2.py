import random
import numpy as np
import math
class Hive:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.health = 100

    def update(self):
        self.health -= 1

class Drone:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 5
        self.direction = random.randint(0, 360)

    def update(self):
        if self.x < 0 or self.x > 800:
            self.direction = (180 - self.direction) % 360
        if self.y < 0 or self.y > 600:
            self.direction = (360 - self.direction) % 360
        self.x += self.speed * math.cos(self.direction)
        self.y -= self.speed * math.sin(self.direction)

    def find_resource(self, hive):
        if hive.health < 50:
            return hive.x, hive.y
        else:
            return random.randint(0, 800), random.randint(0, 600)

class NeuralNetwork:
    def __init__(self):
        self.input_size = 5 # количество входных параметров нейронной сети
        self.hidden_size = 10 # размер скрытого слоя
        self.output_size = 2 # два возможных направления движения дрона
        self.learning_rate = 0.1 # коэффициент обучения

        self.weights_hidden = np.random.randn(self.input_size, self.hidden_size) # матрица весов для связей между входным и скрытым слоем
        self.weights_output = np.random.randn(self.hidden_size, self.output_size) # матрица весов для связей между скрытым и выходным слоем

    def forward(self, inputs):
        hidden = np.dot(inputs, self.weights_hidden)
        hidden = np.tanh(hidden)
        output = np.dot(hidden, self.weights_output)
        output = np.tanh(output)
        return output

    def train(self, inputs, targets):
        hidden = np.dot(inputs, self.weights_hidden)
        hidden = np.tanh(hidden)
        output = np.dot(hidden, self.weights_output)
        output = np.tanh(output)

        error = targets - output
        delta_output = error * (1 - output ** 2)
        error_hidden = np.dot(delta_output, self.weights_output.T)
        delta_hidden = error_hidden * (1 - hidden ** 2)

        self.weights_output += self.learning_rate * hidden.T.dot(delta_output)
        self.weights_hidden += self.learning_rate * inputs.T.dot(delta_hidden)

# Создаем объекты игры
hive = Hive(400, 300)
drones = [Drone(random.randint(0, 800), random.randint(0, 600)) for i in range(10)]
network = NeuralNetwork()

# Цикл игры
while True:
    # Обновляем состояние игры
    hive.update()
    for drone in drones:
        drone.update()
        if drone.x == hive.x and drone.y == hive.y:
            hive.health += 10
        else:
            target = drone.find_resource(hive)
            inputs = [drone.x, drone.y, target[0], target[1], hive.health]
            outputs = network.forward(inputs)
            direction = np.argmax(outputs)
            if direction == 0:
                drone.direction += 10
            else:
                drone.direction -= 10

    # Обучаем нейросеть на основе текущего состояния игры
    inputs = [[drone.x, drone.y, hive.x, hive.y, hive.health] for drone in drones]
    targets = [[1, 0] if drone.direction == 'left' else [0, 1] for drone in drones]
    network.train(inputs, targets)
