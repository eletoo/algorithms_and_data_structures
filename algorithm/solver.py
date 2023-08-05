import math


def reach_goal(grid, agents, max_length, init_x, init_y, goal_x, goal_y):
    """Returns the shortest path from the initial position to the goal position."""
    closed_set = set()
    open_set = set()
    open_set.add(((init_x, init_y), 0))
    g = dict()
    f = dict()
    parents = dict()

    # for t in range(max_length + 1):
    #     for x in range(nrows):
    #         for y in range(ncols):
    #             g[((x, y), t)] = float('inf')
    #             parents[((x, y), t)] = None

    g[((init_x, init_y), 0)] = 0
    f[((init_x, init_y), 0)] = heuristic(init_x, init_y, goal_x, goal_y)
    incumbent = None
    while len(open_set) > 0:
        current = pop_best(closed_set, f, grid, open_set)  # (x, y), t
        if current[0] == (goal_x, goal_y):
            if incumbent is None or f[current] < f[incumbent] or (
                    f[current] == f[incumbent] and current[1] < incumbent[1]):
                incumbent = current

        if current[1] >= max_length:
            continue

        for n in grid.get_me_and_neighbours(current[0][0], current[0][1]):
            if grid.exists(n[0], n[1]):
                continue
            if (n, current[1] + 1) in closed_set:
                continue

            traversable = True
            for a in agents:
                if a.get_pos(current[1] + 1) == n or (
                        a.get_pos(current[1] + 1) == current[0] and a.get_pos(current[1]) == n):
                    traversable = False
                    break

            if not traversable:
                continue

            move_cost = 0
            if current != n:
                move_cost = 1 if grid.is_adjacent_cell(current[0][0], current[0][1], n[0], n[1]) else math.sqrt(2)

            initialize_dicts(current, g, n, parents)  # instead of initializing all dicts at the beginning I only
            # initialize the ones I need to save memory

            if g[current] + move_cost < g[(n, current[1] + 1)]:
                parents[(n, current[1] + 1)] = current
                g[(n, current[1] + 1)] = g[current] + move_cost
                f[(n, current[1] + 1)] = g[(n, current[1] + 1)] + heuristic(n[0], n[1], goal_x, goal_y)
            if n not in open_set:
                open_set.add((n, current[1] + 1))

    return reconstruct_path(init_x, init_y, parents, incumbent), incumbent[1], f[incumbent]


def pop_best(closed_set, f, grid, open_set):
    """Returns the item with the best f score from the open_set."""
    best_f = float('inf')
    current = None  # tuple of ((x, y), t)
    for item in open_set:  # item is a tuple of ((x, y), t)
        if f[item] <= best_f and not grid.exists(item[0][0], item[0][1]):
            best_f = f[item]
            current = item
    open_set.remove(current)
    closed_set.add(current)
    return current


def initialize_dicts(current, g, n, parents):
    """Initializes the dictionaries if the current position or the neighbour position are not in the dictionaries."""
    if current not in g:
        g[current] = float('inf')
    if current not in parents:
        parents[current] = None
    if (n, current[1] + 1) not in g:
        g[(n, current[1] + 1)] = float('inf')
    if (n, current[1] + 1) not in parents:
        parents[(n, current[1] + 1)] = None


def heuristic(x1, y1, x2, y2):
    """Returns the heuristic value of the given position."""
    return abs(x1 - x2) + abs(y1 - y2)  # squared euclidean distance (Manhattan distance)


def reconstruct_path(init_x, init_y, parent, current):  # TODO: write pseudocode
    """Returns the path from the initial position to the goal position."""
    if parent[current] is None:
        return [current[0]]
    else:
        return reconstruct_path(init_x, init_y, parent, parent[current]) + [current[0]]
