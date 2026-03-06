from itertools import chain
import pygame
import pygame_gui
import math

from pygamePlus.core import Screen
from frontend.app.drawing_setings import DrawingSettingsScreen


class NewDrawingScreen(Screen):
    def __init__(self, app, game_name):
        super().__init__(app)

        self.app = app
        self.game_name = game_name

        self.tracking = False
        self.strokes: list[list[tuple[int, int]]] = []
        self.min_distance = 8

        screen_width, screen_height = self.app.win.get_size()

        self.panel_height = 80
        self.panel_rect = pygame.Rect(20, 20, screen_width - 40, self.panel_height)

        self.drawing_rect = pygame.Rect(
            20,
            20 + self.panel_height + 10,
            screen_width - 40,
            screen_height - self.panel_height - 40
        )

        self.manager = pygame_gui.UIManager((screen_width, screen_height))

        self.info_label = pygame_gui.elements.UILabel(
            relative_rect=self.panel_rect,
            text=f"Game: {self.game_name} | SPACE = Draw | R = Reset | Z = Undo | ENTER = Save",
            manager=self.manager
        )

        self.drawing_surface = pygame.Surface(self.drawing_rect.size)
        self.bg_color_off = (40, 40, 40)
        self.bg_color_on = (70, 40, 70)
        self.bg_color_pause = (70, 70, 40)
        self.drawing_surface.fill(self.bg_color_off)

        self.font = pygame.font.SysFont(None, 24)

        self.settings_screen = DrawingSettingsScreen(self.app, self.game_name)
        
        self.pause_time_ms = 200
        self.last_move_time = pygame.time.get_ticks()
        self.was_paused = False
        
    def start_stroke(self):
        self.strokes.append([])

    def end_stroke(self):
        if self.strokes and len(self.strokes[-1]) < 5:
            self.strokes.pop()

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.tracking = not self.tracking
                if self.tracking:
                    self.start_stroke()
                else:
                    self.end_stroke()

            elif event.key == pygame.K_r:
                self.strokes.clear()

            elif event.key == pygame.K_z:
                if self.strokes:
                    self.strokes.pop()

            elif event.key == pygame.K_RETURN:
                flat = list(chain.from_iterable(self.strokes))
                self.settings_screen.load_drawing(flat)
                self.app.switch_screen(self.settings_screen)
    
    def on_resume(self):
        self.strokes.clear()
        self.tracking = False
        
    def update(self):
        
        if not self.tracking:
            return
        
        mouse_pos = pygame.mouse.get_pos()
        if not self.drawing_rect.collidepoint(mouse_pos):
            return

        now = pygame.time.get_ticks()
        
        local_pos = (
            mouse_pos[0] - self.drawing_rect.x,
            mouse_pos[1] - self.drawing_rect.y
        )

        if not self.strokes:
            self.start_stroke()

        stroke = self.strokes[-1]

        if not stroke:
            stroke.append(local_pos)
            self.last_move_time = now
            self.was_paused = False
            self.manager.update(1 / 60)
            return

        last = stroke[-1]
        dist = math.hypot(local_pos[0] - last[0], local_pos[1] - last[1])

        if dist >= self.min_distance:
            if self.was_paused:
                self.start_stroke()
                stroke = self.strokes[-1]

            stroke.append(local_pos)
            self.last_move_time = now
            self.was_paused = False

        elif now - self.last_move_time > self.pause_time_ms:
            self.end_stroke()
            self.was_paused = True

        self.manager.update(1 / 60)

    def draw(self, win):
        win.fill((30, 30, 30))

        pygame.draw.rect(win, (70, 70, 70), self.panel_rect, border_radius=10)
        self.manager.draw_ui(win)

        bg_color = self.bg_color_on if self.tracking else self.bg_color_off
        if self.was_paused:
            bg_color = self.bg_color_pause
        self.drawing_surface.fill(bg_color)

        for stroke in self.strokes:
            if len(stroke) > 1:
                pygame.draw.lines(self.drawing_surface, (0, 255, 0), False, stroke, 3)

        pygame.draw.rect(win, (100, 100, 100), self.drawing_rect, border_radius=10)
        win.blit(self.drawing_surface, self.drawing_rect.topleft)

        mode_text = "DRAW MODE ON" if self.tracking else "DRAW MODE OFF"
        text_surf = self.font.render(mode_text, True, (255, 255, 255))
        win.blit(text_surf, (self.drawing_rect.x + 10, self.drawing_rect.y + 10))
