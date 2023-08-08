import random


class Matrix:
    """A sparse matrix of size height*width, where the matrix is represented as a dictionary of dictionaries."""

    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.rows = dict()

    def add(self, col, row, value=True):
        """Adds the given element at the given position."""
        assert (-1 < row < self.height)
        assert (-1 < col < self.width)
        if row not in self.rows:
            self.rows[row] = dict()
        self.rows[row][col] = value

    def remove(self, col, row):
        """Removes the element at the given position, if it exists."""
        assert (row < self.height)
        assert (col < self.width)
        if row in self.rows:
            if col in self.rows[row]:
                del self.rows[row][col]

    def get(self, col, row):
        """Returns the value of the element at the given position, or None if the element is not found."""
        assert (-1 < row < self.height)
        assert (-1 < col < self.width)
        return self.rows.get(row, dict()).get(col, None)

    def exists(self, col, row):
        """Returns True if the element at the given position exists (i.e. is an obstacle), False otherwise."""
        return self.get(col, row) is not None

    def neighbours(self, col, row):
        """Generator of neighbours of the element at the given position."""
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                if (row + i) < 0 or (row + i) >= self.height or (col + j) < 0 or (col + j) >= self.width:
                    continue
                yield col + j, row + i

    def get_neighbours(self, col, row):
        """Returns the list of neighbours of the element at the given position."""
        return list(self.neighbours(col, row))

    def get_me_and_neighbours(self, col, row):
        """Returns the list of neighbours of the element at the given position, including the element itself."""
        yield from self.neighbours(col, row)
        yield col, row

    def calc_agg_fac(self):
        """Returns the aggregation factor of the matrix."""
        total = 0
        valid = 0
        for i in range(0, self.height):
            for j in range(0, self.width):
                if self.exists(i, j):
                    for l, k in self.neighbours(i, j):
                        if self.exists(l, k):
                            valid += 1
                        total += 1

        return valid / total

    def is_adjacent_cell(self, x1, y1, x2, y2):
        """Returns True if the two given positions are adjacent and free from obstacles, False otherwise."""
        return (not self.exists(x2, y2)) and (
                (x1 == x2 and abs(y1 - y2) == 1) or (y1 == y2 and abs(x1 - x2) == 1))

    def pick_random_cell(self, occupied_cells: list):
        """Returns a random unoccupied cell from the matrix."""
        start = (random.randint(0, self.width - 1), random.randint(0, self.height - 1))
        while self.exists(*start) or start in occupied_cells:
            start = (random.randint(0, self.width - 1), random.randint(0, self.height - 1))
        return start

    def __str__(self):
        ret = ""
        for row in range(self.height):
            for col in range(self.width):
                ret += 'X' if self.exists(col, row) else '.'
            ret += '\n'
        return ret

    def __set__(self, instance, value: tuple):
        self.add(*value)

    def __getitem__(self, item: tuple):
        return self.get(*item)

    def __contains__(self, item: tuple):
        return self.exists(*item)
