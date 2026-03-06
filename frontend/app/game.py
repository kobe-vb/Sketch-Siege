import os
import pygame
import pygame_gui
from frontend.app.drawing import Drawing
from frontend.app.drawing_grid import DrawingGrid
from frontend.app.game_drawing import GameDrawing
from frontend.app.player import Player
from pygamePlus.core import Screen


class Game(Screen):
    def __init__(self, app, game_name: str):
        super().__init__(app)

        self.game_name: str = game_name
        
        self.drawing_count: int = len(os.listdir(f"games/{game_name}"))
        self.players: dict[str, Player] = {}
        
        self.drawings: DrawingGrid = DrawingGrid(self.open_drawing)
        self.player: Player | None = None
        
        self.font = pygame.font.SysFont("Arial", 60)
        
        #debug
        self.set_player("Kobe")
    
    def open_drawing(self, index: int, drawing: Drawing):
        self.app.switch_screen(GameDrawing(self.app, drawing, self.player, index))
        
    def get_drawings_info(self):
        
        locked_drawings: list[int] = []
        
        for player in self.players.values():
            if player is not self.player:
                locked_drawings.extend(player.correct_drawings)
        return self.player.correct_drawings, locked_drawings
        
    def on_resume(self):
        
        if not self.player:
            return
        
        self.drawings.reload(*self.get_drawings_info())

    def set_player(self, team: str):
        
        if team not in self.players:
            self.players[team] = Player(team, self.drawing_count)
        self.player = self.players[team]
        
        self.drawings.load_drawings(f"games/{self.game_name}", self.player.visited_drawings, *self.get_drawings_info())
     
    def add_points(self, points: int) -> None:
        if not self.player:
            return
        self.player.points += points
     
    def handle_event(self, event):
        self.drawings.handle_event(event)   
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.drawings.previous_page()
            elif event.key == pygame.K_RIGHT:
                self.drawings.next_page()
         
    def update(self):
        self.drawings.update()
        
    def draw(self, win):
        win.fill((30, 30, 30))
        
        pygame.draw.rect(win, (70, 70, 70), [118, 10, 1536 - (118 * 2), 100], border_radius=10)
        
        text = self.font.render(f"Game: {self.game_name} | Player: {self.player.name if self.player else 'None'} | Points: {self.player.points if self.player else 0}  | score: {self.player.score if self.player else 0}", True, (255, 255, 255))
        win.blit(text, (128, 50 - text.get_height() // 2))
        
        self.drawings.draw(win)
