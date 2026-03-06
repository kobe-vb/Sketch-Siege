from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import threading

from fastapi.responses import FileResponse

from frontend.app.game import Game
from frontend.app.game_drawing import GameDrawing
from frontend.app.home import HomeScreen
from pygamePlus.core import App as pygameApp

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return FileResponse("frontend/www/index.html")

@app.post("/player/{name}")
def set_player(name: str):
    game: Game | None = games.get_screen(Game)
    if not game:
        return {"success": False, "message": "Game not found"}
    game.set_player(name)
    return {"success": True}

@app.post("/points/{points}")
def add_points(points: int):
    game: Game | None = games.get_screen(Game)
    if not game:
        return {"success": False, "message": "Game not found"}
    game.add_points(points)
    return {"success": True}

@app.get("/drawing/name")
def get_drawing_name():
    game: GameDrawing | None = games.get_screen(GameDrawing)
    if not game:
        return {"success": False, "message": "not in the correct screen"}
    name: str | None = game.get_name()
    if not name:
        return {"success": False, "message": "not in control mode"}
    return {"success": True, "name": name}

@app.post("/drawing/{good}")
def set_drawing(good: bool):
    game: GameDrawing | None = games.get_screen(GameDrawing)
    if not game:
        return {"success": False, "message": "not in the correct screen"}
    if game.set_drawing(good):
        return {"success": True}
    return {"success": False, "message": "not in control mode"}


def get_local_ip():
    import socket
    
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip

@app.on_event("startup")
async def startup_event():
    ip = get_local_ip()
    print(f"➡ Local:   http://localhost:8000")
    print(f"➡ Network: http://{ip}:8000")

def run_server():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

def start_fastapi():
    threading.Thread(target=run_server, daemon=True).start()

start_fastapi()

games = pygameApp(title="sick game")
games.switch_screen(HomeScreen(games))
games.run()
