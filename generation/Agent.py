import math
from random import choice


class Agent:
    def __init__(self, x, y):
        """Initializes the agent."""
        self.moves = [(x, y)]
        self.x = x
        self.y = y
        self.weight = 0

    def move(self, grid, forbidden_moves):
        """Moves the agent to the next position."""
        avail_moves = [(self.x, self.y)] + [
            (x, y) for x, y in grid.get_neighbours(self.x, self.y)
            if not grid.exists(x, y) and (x, y) not in forbidden_moves]  # all moves are valid except for the ones that
        # are occupied by other agents or obstacles

        move = choice(avail_moves)
        self.weight += 1 if grid.is_adjacent_cell(self.x, self.y, move[0], move[1]) or move == (
            self.x, self.y) else math.sqrt(2)  # compute weight
        self.x = move[0]  # update position
        self.y = move[1]
        self.moves.append(move)  # add move to the list of moves

    def get_pos(self, time=None):
        """Returns the position of the agent at the given time. If time is None, returns the last position."""
        if time is None or time >= len(self.moves):
            return self.moves[-1]
        return self.moves[time]

    def __str__(self):
        """Returns a string representation of the agent."""
        return '->'.join([f"({x}, {y})" for x, y in self.moves]) + f" W:{self.weight}\n"

    def __repr__(self):
        return self.__str__()
