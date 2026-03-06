import os
import pygame
import pygame_gui
from frontend.app.game import Game
from frontend.app.new_drawing import NewDrawingScreen
from pygamePlus.core import Screen

class NewGame(Screen):
    def __init__(self, app, game_name: str = None):
        super().__init__(app)

        self.app = app
        self.center_x, _ = app.win.get_size()
        self.center_x //= 2
        self.start_y = 80
        self.element_width = 360
        self.element_height = 40

        self.game_name = game_name

        # ---- Title ----
        self.title = pygame_gui.elements.UILabel(
            relative_rect=self.rect(self.start_y, 50),
            text="MAKE NEW GAME" if not game_name else f"Create {game_name}",
            manager=self.manager
        )

        # ---- Name input ----
        if not game_name:
            self.name_input = pygame_gui.elements.UITextEntryLine(
                relative_rect=self.rect(self.start_y + 100),
                manager=self.manager
            )
        else:
            self._add_game_ui(game_name[0])

    def rect(self, y, h=None):
        if h is None:
            h = self.element_height
        return pygame.Rect(
            (self.center_x - self.element_width // 2, y),
            (self.element_width, h)
        )

    def on_resume(self):
        
        self.drawing_list.kill()
        self.drawing_list = pygame_gui.elements.UISelectionList(
            relative_rect=self.rect(self.start_y + 190, 150),
            item_list=os.listdir(f"games/{self.game_name}"),
            manager=self.manager
        )

    def _add_game_ui(self, name):
        """Add the drawing list and buttons dynamically"""

        os.makedirs(f"games/{name}", exist_ok=True)
    
        self.game_name = name
        self.new_drawing_screen = NewDrawingScreen(self.app, self.game_name)
        self.title.set_text(f"Create {name}")

        # ---- Drawings list ----
        self.drawings_label = pygame_gui.elements.UILabel(
            relative_rect=self.rect(self.start_y + 160, 30),
            text="Drawings:",
            manager=self.manager
        )
        self.drawing_list = pygame_gui.elements.UISelectionList(
            relative_rect=self.rect(self.start_y + 190, 150),
            item_list=os.listdir(f"games/{name}"),
            manager=self.manager
        )

        # ---- Buttons ----
        self.add_drawing_button = pygame_gui.elements.UIButton(
            relative_rect=self.rect(self.start_y + 360),
            text="Add Drawing",
            manager=self.manager
        )
        self.save_game_button = pygame_gui.elements.UIButton(
            relative_rect=self.rect(self.start_y + 420),
            text="Play Game",
            manager=self.manager
        )

    def handle_event(self, event):
        if hasattr(self, "name_input") and event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            name = self.name_input.get_text().strip()
            if name:
                self.name_input.kill()
                del self.name_input
                self._add_game_ui(name)

        if hasattr(self, "add_drawing_button") and event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.add_drawing_button:
                self.app.switch_screen(self.new_drawing_screen)
            elif event.ui_element == self.save_game_button:
                self.app.switch_screen(Game(self.app, self.game_name))

        if hasattr(self, "drawing_list") and event.type == pygame_gui.UI_SELECTION_LIST_NEW_SELECTION:
            if event.ui_element == self.drawing_list:
                print("Selected drawing:", event.text)

    def update(self):
        pass

    def draw(self, win):
        win.fill((30, 30, 30))
