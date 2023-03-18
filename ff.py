import pygame
import random

WIDTH = 800
HEIGHT = 600
FPS = 60

# Определяем цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Neural Network Ball Game")
clock = pygame.time.Clock()

class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 50))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.vel = [random.randint(-5, 5), random.randint(-5, 5)]
        self.acceleration = [0, 0]

    def update(self, balls):
        for ball in balls:
            if ball != self:
                dx = ball.rect.centerx - self.rect.centerx
                dy = ball.rect.centery - self.rect.centery
                distance = (dx ** 2 + dy ** 2) ** 0.5
                if distance <= 50:
                    self.acceleration[0] -= dx / 50
                    self.acceleration[1] -= dy / 50
        self.vel[0] += self.acceleration[0]
        self.vel[1] += self.acceleration[1]
        self.rect.x += self.vel[0]
        self.rect.y += self.vel[1]
        self.acceleration = [0, 0]
        if self.rect.right > WIDTH or self.rect.left < 0:
            self.vel[0] *= -1
        if self.rect.bottom > HEIGHT or self.rect.top < 0:
            self.vel[1] *= -1

all_sprites = pygame.sprite.Group()
balls = []
for i in range(10):
    x = random.randint(0, WIDTH)
    y = random.randint(0, HEIGHT)
    ball = Ball(x, y)
    all_sprites.add(ball)
    balls.append(ball)

# running = True
# while running:
#     clock.tick(FPS)
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False

#     screen.fill(BLACK)
#     all_sprites.update(balls)
#     all_sprites.draw(screen)
#     pygame.display.flip()

pygame.quit()

import tensorflow as tf
from tensorflow import keras
import numpy as np

# Создаем модель нейронной сети
model = keras.Sequential([
    keras.layers.Dense(32, input_shape=(3,), activation='relu'),
    keras.layers.Dense(16, activation='relu'),
    keras.layers.Dense(1, activation='sigmoid')
])

# Компилируем модель и задаем функцию потерь и оптимизатор
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

# Генерируем случайные данные для обучения
train_data = []
for i in range(10000):
    x = random.randint(0, WIDTH)
    y = random.randint(0, HEIGHT)
    dx = random.randint(-5, 5)
    dy = random.randint(-5, 5)
    label = 1 if any(ball.rect.collidepoint(x, y) for ball in balls) else 0
    train_data.append([x, y, label])

train_data = np.array(train_data)

# Обучаем модель на сгенерированных данных
model.fit(train_data[:, :2], train_data[:, 2], epochs=10, batch_size=32)
