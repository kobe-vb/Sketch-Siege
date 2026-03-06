import json
import os
import re
import pygame
import pygame_gui
from frontend.app.dft import dft, dft_fft
from frontend.app.drawing import Drawing
from pygamePlus.core import Screen
from threading import Thread

class DrawingSettingsScreen(Screen):
    def __init__(self, app, game_name):
        super().__init__(app)
        self.app = app
        self.game_name = game_name
        self.drawing_points = None

        self.screen_width, self.screen_height = self.app.win.get_size()

        # ---- Panel setup (rechterkant) ----
        panel_width = 300
        panel_margin = 20
        self.panel_rect = pygame.Rect(
            self.screen_width - panel_width - panel_margin,
            panel_margin,
            panel_width,
            self.screen_height - 2 * panel_margin
        )
        self.panel = pygame_gui.elements.UIPanel(
            relative_rect=self.panel_rect,
            starting_height=1,
            manager=self.manager
        )

        # ---- Panel elements ----
        y = 10
        spacing = 50

        # Naam input
        self.name_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(10, y, 280, 25),
            text="Drawing Name:",
            manager=self.manager,
            container=self.panel
        )
        y += 25
        self.name_input = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect(10, y, 280, 30),
            manager=self.manager,
            container=self.panel
        )
        y += spacing

        # Slices input
        self.slices_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(10, y, 280, 25),
            text="Number of slices:",
            manager=self.manager,
            container=self.panel
        )
        y += 25
        self.slices_input = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect(10, y, 280, 30),
            manager=self.manager,
            container=self.panel
        )
        self.slices_input.set_text("0")
        y += spacing

        # Knoppen
        self.save_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(10, y, 130, 40),
            text="Save",
            manager=self.manager,
            container=self.panel
        )
        self.delete_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(160, y, 130, 40),
            text="Delete",
            manager=self.manager,
            container=self.panel
        )
        y += 60

        self.status_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(10, y, 280, 25),
            text="Ready",
            manager=self.manager,
            container=self.panel
        )

        # ---- Background drawing area (links) ----
        self.drawing_rect = pygame.Rect(
            panel_margin,
            panel_margin,
            self.screen_width - panel_width - 3 * panel_margin,
            self.screen_height - 2 * panel_margin
        )
        self.drawing_surface = pygame.Surface(self.drawing_rect.size)
        self.drawing_surface.fill((50, 50, 50))
        
        self.data_ready = False
        self.drawing: Drawing | None = None
        
        self.data: list[tuple[float, float, float]] = []
        self.drawing_size: tuple[int, int] = (0, 0)

    def load_drawing(self, drawing_points):
        """Load drawing in background"""
        self.data_ready = False
        self.status_label.set_text("Computing DFT...")
        Thread(target=self._compute_data, args=(drawing_points,), daemon=True).start()

    def _compute_data(self, points: list[tuple[float, float]]):
        if not points:
            return
            
        min_x = min(p[0] for p in points)
        max_x = max(p[0] for p in points)
        min_y = min(p[1] for p in points)
        max_y = max(p[1] for p in points)
        
        center_x = (min_x + max_x) / 2
        center_y = (min_y + max_y) / 2
        centered_points = [(x - center_x, y - center_y) for x, y in points]
        
        self.data = dft_fft(centered_points)
        
        drawing_width = max_x - min_x
        drawing_height = max_y - min_y
        
        self.drawing_size = (drawing_width, drawing_height)
        
        self.drawing = Drawing(self.data, self.drawing_size, self.drawing_rect)
        
        self.data_ready = True
        self.status_label.set_text(f"Ready! ({len(points)} points)")
        self.slices_input.set_text(str(len(points)))

    def save_drawing(self):
        if not self.data_ready:
            return
        
        name = self.name_input.get_text()
        slices = int(self.slices_input.get_text())
        
        self.app.pop_screen(2)
    
    def set_number(self, number: int):
        self.slices_input.set_text(str(number))
        self.drawing.set_max_circles(number)
        
    def handle_event(self, event):
        
        if not self.data_ready:
            return
    
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.save_button:
                self.save_drawing()

            elif event.ui_element == self.delete_button:
                self.app.pop_screen()
        if event.type == pygame_gui.UI_TEXT_ENTRY_CHANGED:
            if event.ui_element == self.slices_input:
                text = self.slices_input.get_text()
                if not text.isdigit():
                    self.slices_input.set_text('')
                    self.drawing.set_max_circles(0)
                    return
                slices = int(text)
                if slices > len(self.drawing.circles):
                    slices = len(self.drawing.circles)
                    self.slices_input.set_text(str(slices))
                self.drawing.set_max_circles(slices)
                return
        
        if event.type == pygame.KEYDOWN:
            if self.name_input.is_focused:
                return
            if event.key == pygame.K_r:
                self.slices_input.set_text("")
                self.drawing.set_max_circles(0)
            elif event.key == pygame.K_f:
                self.set_number(len(self.drawing.circles))
            elif '0' <= event.unicode <= '9' and not self.slices_input.is_focused:
                slices = int(self.slices_input.get_text()) if self.slices_input.get_text().isdigit() else 0
                self.set_number(slices + int(event.unicode))
        
    def set_status(self, text: str):
        self.status_label.set_text(text)   
         
    def save_drawing(self):
        if not self.data_ready or not self.drawing:
            self.set_status("Nothing to save")
            return

        name = re.sub(r'[^a-zA-Z0-9_\-]', '_', self.name_input.get_text().strip())  # remove non-alphanumeric characters

        if not name:
            self.set_status("Name cannot be empty")
            return
        
        if self.slices_input.get_text().strip() == '':
            self.set_status("Enter number of slices")
            return

        slices = int(self.slices_input.get_text())
        if slices <= 0:
            self.set_status("Slices must be > 0")
            return
        elif slices == len(self.drawing.circles):
            self.set_status("Slices must be less than max")
            return

        file_path = os.path.join("games", self.game_name, f"{name}.json")

        if os.path.exists(file_path):
            self.set_status("Name already exists")
            return

        save_data = {
            "name": name,
            "drawing_size": list(self.drawing_size),
            "slices": slices,
            "data": self.data
        }

        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(save_data, f, indent=4)

        except Exception as e:
            self.set_status(f"Save failed")
            print("Save error:", e)
            return

        self.set_status("Saved successfully!")
        self.app.pop_screen(2)


    def update(self):
        self.manager.update(1/60)
        if self.data_ready and self.drawing:
            self.drawing.update()

    def draw(self, win):
        win.fill((30, 30, 30))
        
        if self.data_ready and self.drawing:
            self.drawing.draw(win)

        pygame.draw.rect(win, (70, 70, 70), self.panel_rect, border_radius=10)
        self.manager.draw_ui(win)