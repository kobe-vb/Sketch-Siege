import json
import os

import pygame

from frontend.app.drawing import Drawing



class DrawingGrid:
    
    def __init__(self, on_click: callable):
        
        self.on_click = on_click
        
        self.drawings: list[Drawing] = []
        self.visited_drawings: list[int] = []
        self.correct_drawings: list[int] = []
        self.locked_drawings: list[int] = []
        self.dir_path: str = ""
        
        self.page_width: int = 6
        self.page_height: int = 3
        
        self.page_size: int = self.page_width * self.page_height
        self.page: int = 0
        self.max_pages: int = 0
        self.drawing_names: list[str] = []
    
    def reload(self, correct_drawings: dict[str, int], locked_drawings: dict[str, int]):
        for i, drawing in enumerate(self.drawings):
            drawing.set_max_circles(self.visited_drawings[i + self.page * self.page_size])
        
        self.correct_drawings = correct_drawings
        self.locked_drawings = locked_drawings
    
    def load_drawings(self, dir_path: str, visited_drawings: list[int], correct_drawings: dict[str, int], locked_drawings: dict[str, int]):
        
        self.dir_path = dir_path
        self.visited_drawings = visited_drawings
        self.correct_drawings = correct_drawings
        self.locked_drawings = locked_drawings
        
        self.drawing_names = os.listdir(dir_path)
        
        self.page = 0
        self.max_pages = len(self.visited_drawings) // self.page_size + 1 if len(self.visited_drawings) % self.page_size > 0 else 0
        self.load_page()
    
    def load_page(self):
        
        self.drawings.clear()
        for i in range(self.page_size):
            drawing_index = self.page * self.page_size + i
            if drawing_index >= len(self.visited_drawings):
                break
            with open(f"{self.dir_path}/{self.drawing_names[drawing_index]}", "r") as f:
                data = json.load(f)
            
            circles = data["data"]
            drawing_size = tuple(data["drawing_size"])
            rect = pygame.Rect(
                (118 + (i % self.page_width) * 220,
                 123 + (i // self.page_width) * 220),
                (200, 200)
            )
            name: str = data["name"]
            score: int = data.get("slices", 0)
            self.drawings.append(Drawing(circles, drawing_size, rect, self.visited_drawings[drawing_index], name, score))
            
    def next_page(self):
        if self.page < self.max_pages - 1:
            self.page += 1
            self.load_page()
    
    def previous_page(self):
        if self.page > 0:
            self.page -= 1
            self.load_page()
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for i, drawing in enumerate(self.drawings):
                index: int = self.page * self.page_size + i
                if index in self.locked_drawings:
                    continue
                if drawing.drawing_rect.collidepoint(event.pos):
                    self.on_click(self.page * self.page_size + i, drawing)
                                    
    def update(self):
        for drawing in self.drawings:
            drawing.update()
    
    def draw(self, win):
                        
        for i, drawing in enumerate(self.drawings):
            drawing.draw(win)
            
            index: int = self.page * self.page_size + i
            
            if index in self.locked_drawings:
                pygame.draw.rect(win, (200, 50, 50), drawing.drawing_rect, border_radius=10)
                continue
            
            if index in self.correct_drawings:
                overlay = pygame.Surface(drawing.drawing_rect.size, pygame.SRCALPHA)
                pygame.draw.rect(
                    overlay,
                    (0, 255, 0, 100),  # RGBA
                    overlay.get_rect(),
                    border_radius=10
                )
                win.blit(overlay, drawing.drawing_rect.topleft)
                            
            if drawing.drawing_rect.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(win, (255, 255, 255), drawing.drawing_rect, 3, border_radius=10)
            
