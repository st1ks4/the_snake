import pygame
import random

# Определяем размеры и цвета
WIDTH, HEIGHT = 800, 600
GRID_SIZE = 20
BG_COLOR = (0, 0, 0)  # Черный
SNAKE_COLOR = (0, 255, 0)  # Зеленый
APPLE_COLOR = (255, 0, 0)  # Красный

class GameObject:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, 
                         (self.x, self.y, GRID_SIZE, GRID_SIZE))

class Snake(GameObject):
    def __init__(self):
        super().__init__(100, 100, SNAKE_COLOR)  # Начальная позиция
        self.body = [(100, 100), (80, 100), (60, 100)]  # Сегменты тела
        self.direction = (GRID_SIZE, 0)  # Начальное направление (вправо)

    def move(self):
        # Вставляем новую голову
        head_x = self.body[0][0] + self.direction[0]
        head_y = self.body[0][1] + self.direction[1]
        self.body.insert(0, (head_x, head_y))
        self.body.pop()  # Удаляем хвост

    def grow(self):
        # Увеличиваем длину змейки
        self.body.append(self.body[-1])  # Копируем последний сегмент

    def change_direction(self, new_direction):
        # Изменяем направление, если оно не противоположное
        if (new_direction[0] * -1, new_direction[1] * -1) != self.direction:
            self.direction = new_direction

    def draw(self, surface):
        for segment in self.body:
            pygame.draw.rect(surface, self.color, 
                             (segment[0], segment[1], GRID_SIZE, GRID_SIZE))

class Apple(GameObject):
    def __init__(self):
        self.randomize_position()

    def randomize_position(self):
        self.x = random.randint(0, (WIDTH // GRID_SIZE) - 1) * GRID_SIZE
        self.y = random.randint(0, (HEIGHT // GRID_SIZE) - 1) * GRID_SIZE

    def draw(self, surface):
        pygame.draw.rect(surface, APPLE_COLOR, 
                         (self.x, self.y, GRID_SIZE, GRID_SIZE))

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Змейка')

    snake = Snake()
    apple = Apple()

    clock = pygame.time.Clock()
    running = True

    while running:
        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.change_direction((0, -GRID_SIZE))
                elif event.key == pygame.K_DOWN:
                    snake.change_direction((0, GRID_SIZE))
                elif event.key == pygame.K_LEFT:
                    snake.change_direction((-GRID_SIZE, 0))
                elif event.key == pygame.K_RIGHT:
                    snake.change_direction((GRID_SIZE, 0))

        # Движение змейки
        snake.move()

        # Проверка на столкновение с яблоком
        if snake.body[0] == (apple.x, apple.y):
            snake.grow()
            apple.randomize_position()

        # Проверка на столкновение с собой
        if snake.body[0] in snake.body[1:]:
            print("Игра окончена! Змейка столкнулась с собой.")
            running = False

        # Отрисовка объектов
        screen.fill(BG_COLOR)
        snake.draw(screen)
        apple.draw(screen)

        # Обновление экрана
        pygame.display.update()

        # Ограничение FPS
        clock.tick(10)  # Скорость игры

    pygame.quit()

if name == '__main__':
    main()
