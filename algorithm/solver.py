import math


def reach_goal(grid, agents, max_length, init_x, init_y, goal_x, goal_y, nrows, ncols):
    """Returns the shortest path from the initial position to the goal position."""
    closed_set = set()
    open_set = set()
    open_set.add(((init_x, init_y), 0))
    g = dict()
    f = dict()
    parent = dict()
    for t in range(max_length + 1):
        for x in range(nrows):
            for y in range(ncols):
                g[((x, y), t)] = float('inf')
                parent[((x, y), t)] = None
    g[((init_x, init_y), 0)] = 0
    f[((init_x, init_y), 0)] = heuristic(init_x, init_y, goal_x, goal_y)
    while len(open_set) > 0:
        best_f = float('inf')
        current = None  # tuple of ((x, y), t)
        for item in f.items():  # item is a tuple of (((x, y), t), f)
            if item[1] <= best_f and not grid.exists(item[0][0][0], item[0][0][1]):
                best_f = item[1]
                current = item[0]
        open_set.remove(current)
        closed_set.add(current)
        if current[0] == (goal_x, goal_y):
            return reconstruct_path(init_x, init_y, parent, current), current[1], f[current]

        if current[1] < max_length:
            for n in grid.neighbours(current[0][0], current[0][1]):
                if grid.exists(n[0], n[1]):
                    continue
                if (n, current[1] + 1) in closed_set:
                    continue

                traversable = True
                for a in agents:
                    if current[1] + 1 < len(a.moves) and (
                            a.moves[current[1] + 1] == n or (
                            a.moves[current[1] + 1] == current[0] and a.moves[current[1]] == n)):
                        traversable = False
                        break

                if not traversable:
                    continue

                move_cost = 0
                if current != n:
                    move_cost = 1 if grid.is_adjacent_cell(current[0][0], current[0][1], n[0], n[1]) else math.sqrt(2)
                if g[current] + move_cost < g[(n, current[1] + 1)]:
                    parent[(n, current[1] + 1)] = current
                    g[(n, current[1] + 1)] = g[current] + move_cost
                    f[(n, current[1] + 1)] = g[(n, current[1] + 1)] + heuristic(n[0], n[1], goal_x, goal_y)
                if n not in open_set:
                    open_set.add((n, current[1] + 1))

    return None  # reached max_length without finding a path or finished looking through the open_set


def heuristic(x1, y1, x2, y2):
    """Returns the heuristic value of the given position."""
    return abs(x1 - x2) + abs(y1 - y2)  # squared euclidean distance (Manhattan distance)


def reconstruct_path(init_x, init_y, parent, current):  # TODO: write pseudocode
    """Returns the path from the initial position to the goal position."""
    if parent[current] is None:
        return [current[0]]
    else:
        return reconstruct_path(init_x, init_y, parent, parent[current]) + [current[0]]
