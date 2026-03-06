import pygame
from math import cos, sin, pi


class Drawing:
    def __init__(self, circles: list[tuple[float, float, float]], drawing_size: tuple[int, int], rect: pygame.Rect, visible_counts: int = None, name: str = "Drawing", score: int = 0):

        self.circles: list[tuple[float, float, float]] = circles
        self.drawing_rect: pygame.Rect = rect
        self.drawing_size: tuple[int, int] = drawing_size
        self.name: str = name
        self.score: int = score

        self.offset: tuple[int, int] = ()
        self.scale: float = 1.0
        self.calculate_drawing_parameters(drawing_size)
        
        self.time = 0.0

        self.path = []
        self.max_path_length = 1000
        
        self.max_circles: int = len(circles)
        if visible_counts is not None:
            self.max_circles = min(visible_counts, len(circles))
                
    def calculate_drawing_parameters(self, drawing_size: tuple[int, int]):
               
        factor: float = 0.9
        available_width = self.drawing_rect.width * factor
        available_height = self.drawing_rect.height * factor
        
        self.scale = min(available_width / drawing_size[0], available_height / drawing_size[1])
        self.offset = (self.drawing_rect.x + self.drawing_rect.width // 2,
                       self.drawing_rect.y + self.drawing_rect.height // 2)

    def set_max_circles(self, n):
        self.max_circles = min(n, len(self.circles))
        self.path.clear()

    def update(self):
        
        self.time += 2 * pi / len(self.circles)
        if self.time > 2 * pi:
            self.time = 0.0

    def draw(self, win):
        
        pygame.draw.rect(win, (50, 50, 50), self.drawing_rect, border_radius=10)

        x, y = self.offset

        for frequency, radius, phase in self.circles[:self.max_circles]:
            prev_x, prev_y = x, y
            scaled_radius = radius * self.scale

            angle = frequency * self.time + phase
            x += scaled_radius * cos(angle)
            y += scaled_radius * sin(angle)

            pygame.draw.circle(win, (0, 255, 0), (prev_x, prev_y), scaled_radius, 1)
            pygame.draw.line(win, (255, 0, 0), (prev_x, prev_y), (x, y), 2)

        self.path.append((int(x), int(y)))
        if len(self.path) > self.max_path_length:
            self.path.pop(0)

        if len(self.path) > 1:
            pygame.draw.lines(win, (0, 255, 100), False, self.path, 2)

        pygame.draw.circle(win, (255, 0, 0), (int(x), int(y)), 4)