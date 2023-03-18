import pygame

# Настройка экрана
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Змейка")

# Отображение игровых объектов
SNAKE_COLOR = (0, 255, 0)
FOOD_COLOR = (255, 0, 0)
snake_head = pygame.Rect(350, 250, 25, 25) # голова змеи
snake_body = [pygame.Rect(350, 275, 25, 25), pygame.Rect(350, 300, 25, 25)] # тело змеи
food = pygame.Rect(200, 200, 25, 25) # еда

# Отображение на экране
while True:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            # sys.exit()

    # Отрисовка объектов на экране
    screen.fill((0, 0, 0)) # Черный фон
    pygame.draw.rect(screen, SNAKE_COLOR, snake_head)
    for body_part in snake_body:
        pygame.draw.rect(screen, SNAKE_COLOR, body_part)
    pygame.draw.rect(screen, FOOD_COLOR, food)
    pygame.display.update()
