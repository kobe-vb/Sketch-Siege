

class Player:
    def __init__(self, name: str, length: int):
        self.name: str = name
        self.visited_drawings: list[int] = [1] * length if name != "Kobe" else [999999] * length
        self.correct_drawings: list[int] = []
        self.points: int = 0 if name != "Kobe" else 999999
        self.score: int = 0
