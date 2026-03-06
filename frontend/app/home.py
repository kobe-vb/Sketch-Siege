import os
import pygame
import pygame_gui
from frontend.app.game import Game
from frontend.app.new_game import NewGame
from pygamePlus.core import App, Screen


class HomeScreen(Screen):
    def __init__(self, app: "App"):
        super().__init__(app)
        self.build_ui()

    def build_ui(self):
        """Bouw of herbouw de hele UI."""
        screen_width, screen_height = self.app.win.get_size()
        button_width = 300
        button_height = 50
        spacing = 20
        center_x = (screen_width - button_width) // 2
        start_y = screen_height // 2 - 120

        # Verwijder oude elementen (indien aanwezig)
        for attr in ["title", "level_dropdown", "play_button", "new_game_button", "edit_button"]:
            if hasattr(self, attr):
                getattr(self, attr).kill()

        # Titel
        self.title = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((center_x, start_y - 80), (button_width, 50)),
            text="MY GAME",
            manager=self.manager
        )

        # Dropdown menu dynamisch vullen met mappen in 'games/'
        game_options = self.get_games()
        self.level_dropdown = pygame_gui.elements.UIDropDownMenu(
            options_list=game_options,
            starting_option=game_options[0],
            relative_rect=pygame.Rect((center_x, start_y), (button_width, 40)),
            manager=self.manager
        )

        # Knoppen
        self.play_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((center_x, start_y + 40 + spacing), (button_width, button_height)),
            text="Play",
            manager=self.manager
        )

        self.new_game_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((center_x, start_y + 40 + spacing * 2 + button_height), (button_width, button_height)),
            text="Make New Game",
            manager=self.manager
        )

        self.edit_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((center_x, start_y + 40 + spacing * 3 + button_height * 2), (button_width, button_height)),
            text="Edit",
            manager=self.manager
        )

    def get_games(self):
        games_dir = "games"
        if not os.path.exists(games_dir):
            os.makedirs(games_dir)
        game_options = [d for d in os.listdir(games_dir) if os.path.isdir(os.path.join(games_dir, d))]
        if not game_options:
            game_options = ["No games found"]
        return game_options

    def on_resume(self):
        # Herbouw UI bij terugkeer naar dit scherm
        self.build_ui()

    def handle_event(self, event):
        
        if event.type == pygame.WINDOWMAXIMIZED or event.type == pygame.WINDOWRESIZED:
            self.build_ui()
        
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.play_button:
                selected_game = self.level_dropdown.selected_option
                self.app.switch_screen(Game(self.app, selected_game[0]))

            if event.ui_element == self.new_game_button:
                self.app.switch_screen(NewGame(self.app))

            if event.ui_element == self.edit_button:
                selected_game = self.level_dropdown.selected_option
                self.app.switch_screen(NewGame(self.app, selected_game))

        if event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
            if event.ui_element == self.level_dropdown:
                print("Selected game:", event.text)

    def update(self):
        pass

    def draw(self, win):
        win.fill((0, 100, 200))
