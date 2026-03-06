from math import inf
import pygame
import pygame_gui
from frontend.app.drawing import Drawing
from frontend.app.player import Player
from pygamePlus.core import Screen


class GameDrawing(Screen):
    def __init__(self, app, drawing: Drawing, player: Player, index: int):
        super().__init__(app)
        self.app = app
        self.player: Player = player
        self.index: int = index

        screen_width, screen_height = self.app.win.get_size()
        self.top_bar_height = 60
        self.top_bar_rect = pygame.Rect(0, 0, screen_width, self.top_bar_height)
        rect: pygame.Rect = pygame.Rect(20, 
                                                self.top_bar_height + 20, 
                                                screen_width - 40, 
                                                screen_height - self.top_bar_height - 40)
        self.drawing = Drawing(drawing.circles, drawing.drawing_size, rect, self.player.visited_drawings[self.index], drawing.name, drawing.score)

        self.color: tuple[int, int, int] = (30, 30, 30)
        if self.index in self.player.correct_drawings:
            self.color = (0, 255, 0)

        x = 20
        y = 10
        w = 80
        h = 40
        gap = 10

        self.add1_btn = pygame_gui.elements.UIButton(
            pygame.Rect(x, y, w, h), "+1", self.manager
        )
        x += w + gap

        self.add5_btn = pygame_gui.elements.UIButton(
            pygame.Rect(x, y, w, h), "+5", self.manager
        )
        x += w + gap
        self.add10_btn = pygame_gui.elements.UIButton(
            pygame.Rect(x, y, w, h), "+10", self.manager
        )
        
        x += w + gap
        self.close_btn = pygame_gui.elements.UIButton(
            pygame.Rect(x, y, w, h),
            "Sluit",
            self.manager
        )

        self.check_btn = pygame_gui.elements.UIButton(
            pygame.Rect(screen_width - 190, y, 170, h),
            "Controleer (5p)",
            self.manager
        )
        
        self.control_drawing: bool = False
    
    def get_name(self) -> str | None:
        if self.control_drawing:
            return self.drawing.name
        return None
    
    def set_drawing(self, good: bool) -> bool:
        
        if not self.control_drawing:
            return False
        
        if good:
            self.player.score += self.drawing.score
            self.player.correct_drawings.append(self.index)
            self.player.visited_drawings[self.index] = inf
            self.drawing.set_max_circles(self.player.visited_drawings[self.index])
            self.color = (0, 255, 0)
        else:
            self.color = (255, 0, 0)
            
        self.control_drawing = False
        self.check_btn.set_text("Controleer (5p)")
        
        return True

    def add_slices(self, amount: int):
        
        amount = min(amount, self.player.points)
        self.player.points -= amount
        
        self.player.visited_drawings[self.index] += amount
        self.drawing.set_max_circles(self.player.visited_drawings[self.index])

    def handle_event(self, event):
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.add1_btn:
                self.add_slices(1)
            elif event.ui_element == self.add5_btn:
                self.add_slices(5)
            elif event.ui_element == self.add10_btn:
                self.add_slices(10)
            elif event.ui_element == self.check_btn:
                self.check_answer()
            elif event.ui_element == self.close_btn:
                self.app.pop_screen()

    def check_answer(self):
        
        if self.control_drawing:
            return
        
        if self.player.points < 5:
            return
        self.player.points -= 5
        
        self.control_drawing = True
        self.check_btn.set_text("aan het controleer...")

    def update(self):
        self.manager.update(1/60)
        self.drawing.update()

    def draw(self, win):
        
        win.fill(self.color)

        # top bar
        pygame.draw.rect(win, (50, 50, 50), self.top_bar_rect)
        
        font = pygame.font.SysFont("Arial", 24)
        text = font.render(f"points left: {self.player.points} | points in: {self.drawing.max_circles}" + ("" if self.color != (0, 255, 0) else f" | score: {self.drawing.score}"), True, (255, 255, 255))
        win.blit(text, (400, 10))
        
        self.drawing.draw(win)
        self.manager.draw_ui(win)
