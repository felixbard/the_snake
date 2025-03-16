from random import choice, randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Базовый класс, от которого наследуются другие игровые объекты."""

    # Атрибуты класса GameObject
    position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
    body_color = (0, 0, 0)

    def __init__(self):
        self.position = self.position
        self.body_color = self.body_color

    def draw(self):
        """Абстрактный метод."""
        pass


class Snake(GameObject):
    """Класс, описывающий змейку и её поведение."""

    # Атрибуты класса Snake
    length = 1
    positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
    direction = RIGHT
    next_direction = None
    body_color = SNAKE_COLOR

    def __init__(self):
        super().__init__()
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = Snake.body_color
        self.last = None

    def update_direction(self):
        """Метод обновления направления после нажатия на кнопку."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def get_head_position(self):
        """Метод, возвращающий позицию головы змейки."""
        return self.positions[0]

    def move(self):
        """Метод обновления положения змейки."""
        current_pos = self.get_head_position()
        new_pos = (current_pos[0] + self.direction[0] * GRID_SIZE,
                   current_pos[1] + self.direction[1] * GRID_SIZE)

        # Проверка достижения края экрана
        new_pos = (new_pos[0] % SCREEN_WIDTH, new_pos[1] % SCREEN_HEIGHT)

        if new_pos in self.positions[2:]:
            self.reset()
        else:
            self.positions.insert(0, new_pos)
            if len(self.positions) > self.length:
                self.positions.pop(-1)

    def draw(self):
        """Метод draw класса Snake."""
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def reset(self):
        """Метод сброса змейки в начальное состояние после столкновения."""
        self.length = 1
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        directions = [UP, DOWN, RIGHT, LEFT]
        self.direction = choice(directions)


class Apple(GameObject):
    """Класс, описывающий яблоко и действия с ним."""

    # Переопределение атрибутов для класса Apple
    body_color = APPLE_COLOR
    position = (randint(0, GRID_WIDTH) * GRID_SIZE,
                randint(0, GRID_HEIGHT) * GRID_SIZE)

    def __init__(self):
        super().__init__()
        self.body_color = Apple.body_color
        self.position = self.randomize_position()

    def randomize_position(self):
        """Метод перемещения яблока."""
        pos = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
               randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
        return pos

    def draw(self):
        """Метод draw класса Apple."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


def handle_keys(game_object):
    """Функция обработки действий пользователя."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Основная функция."""
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)

        # Тут опишите основную логику игры.
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        # Проверка на "съедение" яблока
        if snake.positions[0] == apple.position:
            snake.length += 1  # Увеличиваем длину
            apple.position = apple.randomize_position()

        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw()
        apple.draw()

        pygame.display.update()


if __name__ == '__main__':
    main()
