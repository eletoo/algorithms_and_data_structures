import math
from random import choice


class Agent:
    def __init__(self, x, y):
        self.moves = []
        self.x = x
        self.y = y
        self.weight = 0

    def move(self, grid, forbidden_moves):
        """Moves the agent to the next position."""
        avail_moves = [(self.x, self.y)] + [
            (x, y) for x, y in grid.get_neighbours(self.x, self.y)
            if not grid.exists(x, y) and (x, y) not in forbidden_moves]

        move = choice(avail_moves)
        if move != (self.x, self.y):
            self.weight += 1 if grid.is_adjacent_cell(self.x, self.y, move[0], move[1]) else math.sqrt(2)
        self.x = move[0]
        self.y = move[1]
        self.moves.append(move)

    def __str__(self):
        return '->'.join([f"({x}, {y})" for x, y in self.moves]) + f" W:{self.weight}\n"

    def __repr__(self):
        return self.__str__()

    def get_pos(self):
        return self.x, self.y
