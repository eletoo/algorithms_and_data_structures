import heapq
import math
from collections import namedtuple

from algorithm.Graph import Graph


def reach_goal(grid, agents, max_length, init_x, init_y, goal_x, goal_y, relaxed=False):
    """Returns the shortest path from the initial position to the goal position."""
    # AuxPath = namedtuple('AuxPath', ['next', 'cost', 'time_taken'])
    aux = dijkstra(grid, init_x, init_y, goal_x, goal_y)

    closed_set = set()
    open_set = set()
    open_set.add(((init_x, init_y), 0))
    g = dict()
    f = dict()
    parents = dict()
    parents[((init_x, init_y), 0)] = None

    g[((init_x, init_y), 0)] = 0
    f[((init_x, init_y), 0)] = heuristic(init_x, init_y, goal_x, goal_y)
    incumbent = None
    while len(open_set) > 0:
        current = pop_best(closed_set, f, grid, open_set)  # (x, y), t

        if current[0] == (goal_x, goal_y):
            if incumbent is None or f[current] < f[incumbent] or (
                    f[current] == f[incumbent] and current[1] < incumbent[1]):
                incumbent = current

        if relaxed:
            relaxed_path, time_taken, cost = get_aux_path_and_verify(aux, grid, (current[0][0], current[0][1]), agents,
                                                                     current[1], max_length)
            if relaxed_path is not None:
                return relaxed_path, time_taken, cost

        if current[1] >= max_length:
            continue

        for n in grid.get_me_and_neighbours(current[0][0], current[0][1]):
            if grid.exists(n[0], n[1]):
                continue

            traversable = True
            for a in agents:
                if a.get_pos(current[1] + 1) == n or (
                        a.get_pos(current[1] + 1) == current[0] and a.get_pos(current[1]) == n):
                    traversable = False
                    break

            if not traversable:
                continue

            move_cost = 1 if grid.is_adjacent_cell(current[0][0], current[0][1], n[0], n[1]) or (
                current[0][0], current[0][1]) == (n[0], n[1]) else math.sqrt(2)

            if (n, current[1] + 1) in closed_set and g[current] + move_cost >= g[(n, current[1] + 1)]:
                continue

            initialize_dicts(current, g, n, parents)  # instead of initializing all dicts at the beginning I only
            # initialize the ones I need to save memory

            if g[current] + move_cost < g[(n, current[1] + 1)]:
                parents[(n, current[1] + 1)] = current
                g[(n, current[1] + 1)] = g[current] + move_cost
                f[(n, current[1] + 1)] = g[(n, current[1] + 1)] + heuristic(n[0], n[1], goal_x, goal_y)
            if n not in open_set:
                open_set.add((n, current[1] + 1))

    if incumbent is None:
        return None, 0, float('inf')
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
    return abs(x1 - x2) ** 2 + abs(y1 - y2) ** 2  # squared euler distance


def reconstruct_path(init_x, init_y, parent, current):  # TODO: write pseudocode
    """Returns the path from the initial position to the goal position."""
    if parent[current] is None:
        return [current[0]]
    else:
        return reconstruct_path(init_x, init_y, parent, parent[current]) + [current[0]]


def reconstruct_relaxed_path(init_x, init_y, parent, current):  # TODO: write pseudocode
    """Returns the path from the initial position to the goal position."""
    if parent[current] is None:
        return [current]
    else:
        return reconstruct_path(init_x, init_y, parent, parent[current]) + [current]


def dijkstra(graph, init_x, init_y, goal_x, goal_y):
    """Returns the shortest path from the initial position to the goal position."""
    parents = dict()
    spt_set = dict()
    heap = list()
    spt_set[(goal_x, goal_y)] = 0
    heapq.heappush(heap, (0, (goal_x, goal_y)))
    parents[(goal_x, goal_y)] = None
    while len(heap) > 0:
        current = heapq.heappop(heap)  # (cost, (x, y))
        if current[1] == (init_x, init_y):
            break
        for neighbour in graph.get_me_and_neighbours(current[1][0], current[1][1]):
            w = 1 if graph.is_adjacent_cell(current[1][0], current[1][1], neighbour[0], neighbour[1]) or (
                current[1][0], current[1][1]) == (neighbour[0], neighbour[1]) else math.sqrt(2)

            if neighbour not in spt_set or spt_set[neighbour] > current[0] + w:
                spt_set[neighbour] = current[0] + w
                parents[neighbour] = current[1]
                heapq.heappush(heap, (spt_set[neighbour], neighbour))

    return parents


def get_aux_path_and_verify(aux, grid, init, agents, tstart, tmax):
    path = []
    node = init
    time = tstart
    while node is not None:
        if time > tmax:
            return None, 0, float('inf')
        path.append(node)
        time += 1
        node = aux[node]

    if verify_path(path, init, path[-1], agents, tmax, tstart):
        cost = 0
        for i in range(len(path) - 1):
            if path[i] == path[i + 1] or grid.is_adjacent_cell(path[i][0], path[i][1], path[i + 1][0], path[i + 1][1]):
                cost += 1
            else:
                cost += math.sqrt(2)
        return path, max(0, len(path) - 1), cost

    return None, 0, float('inf')


def verify_path(path, init, last, agents, tmax, tstart):
    return True
