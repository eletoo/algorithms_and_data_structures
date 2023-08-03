import random


class Matrix:
    """A sparse matrix of size height*width, where the matrix is represented as a dictionary of dictionaries."""

    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.rows = dict()

    def add(self, row, col, value=True):
        """Adds the given element at the given position."""
        assert (row < self.height)
        assert (col < self.width)
        if row not in self.rows:
            self.rows[row] = dict()
        self.rows[row][col] = value

    def remove(self, row, col):  # TODO: check if this method is needed
        """Removes the element at the given position, if it exists."""
        assert (row < self.height)
        assert (col < self.width)
        if row in self.rows:
            if col in self.rows[row]:
                del self.rows[row][col]

    def get(self, row, col):
        """Returns the value of the element at the given position, or None if the element is not found."""
        assert (row < self.height)
        assert (col < self.width)
        return self.rows.get(row, dict()).get(col, None)

    def exists(self, row, col):
        """Returns True if the element at the given position exists (i.e. is an obstacle), False otherwise."""
        return self.get(row, col) is not None

    def neighbours(self, row, col):
        """Generator of neighbours of the element at the given position."""
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                if (row + i) < 0 or (row + i) >= self.height or (col + j) < 0 or (col + j) >= self.width:
                    continue
                yield row + i, col + j

    def get_neighbours(self, row, col):
        """Returns the list of neighbours of the element at the given position."""
        return list(self.neighbours(row, col))

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

    def is_adjacent_cell(self, row1, col1, row2, col2):
        """Returns True if the two given positions are adjacent and free from obstacles, False otherwise."""
        return (not self.exists(row2, col2)) and (
                (row1 == row2 and abs(col1 - col2) == 1) or (col1 == col2 and abs(row1 - row2) == 1))

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
                ret += 'X' if self.exists(row, col) else '.'
            ret += '\n'
        return ret

    def __set__(self, instance, value: tuple):
        self.add(*value)

    def __getitem__(self, item: tuple):
        return self.get(*item)

    def __contains__(self, item: tuple):
        return self.exists(*item)
