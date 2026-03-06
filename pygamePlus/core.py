from ast import List
import pygame
import pygame_gui

    
class Screen:
    
    def __init__(self, app: "App"):
        self.app = app
        self.manager = pygame_gui.UIManager(app.win.get_size(), "theme.json")
    
    def handle_event(self, event):
        pass
    
    def update(self):
        pass
    
    def draw(self, win: pygame.Surface):
        pass
    
    def on_resume(self):
        pass

class App:
    
    def __init__(self, width=800, height=600, title="Pygame Plus App"):
        pygame.init()
        self.win = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        self.running = True
        
        self.screen: list[Screen] = []
    
    def get_screen(self, type: type[Screen]) -> Screen | None:
        if isinstance(self.screen[-1], type):
            return self.screen[-1]
        return None
    
    def switch_screen(self, screen: Screen):
        screen.on_resume()
        self.screen.append(screen)
    
    def add_screen(self, screen: Screen):
        self.screen[-1].append(screen)
    
    def pop_screen(self, n=1):
        for _ in range(n):
            if len(self.screen) == 0:
                return
            self.screen.pop()
        
        if len(self.screen) != 0:
            self.screen[-1].on_resume()
                
    def handle_event(self, event):
        pass

    def update(self):
        pass

    def draw(self):
        pass
    
    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_DELETE:
                    self.running = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                    if event.mod & pygame.KMOD_ALT:
                        self.pop_screen()
                        
                if self.screen:
                    self.screen[-1].handle_event(event)
                    self.screen[-1].manager.process_events(event)
                self.handle_event(event)
            
            self.update()
            if self.screen:
                self.screen[-1].update()
                self.screen[-1].manager.update(self.clock.get_time()/1000.0)
            
            self.draw()
            if self.screen:
                self.screen[-1].draw(self.win)
                self.screen[-1].manager.draw_ui(self.win)

            pygame.display.flip()
            self.clock.tick(60)
            pygame.display.set_caption(f"Pygame Plus App - {self.clock.get_fps():.2f} FPS")
        
        pygame.quit()