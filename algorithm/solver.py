import heapq
import math


def reach_goal(grid, agents, max_length, init_x, init_y, goal_x, goal_y, relaxed=False, greedy=True):
    """Returns the shortest path from the initial position to the goal position."""
    if relaxed:  # if I want to use the relaxed version of the algorithm I need to run the Dijkstra algorithm
        aux = dijkstra(grid, goal_x, goal_y, max_length)

    closed_set = set()
    open_set = list()
    heapq.heappush(open_set, (heuristic(init_x, init_y, goal_x, goal_y), ((init_x, init_y), 0)))  # (f, ((x, y), t))
    # open_set.add(((init_x, init_y), 0))
    g = dict()  # weights
    # f = dict()  # f = g + heuristic
    parents = dict()
    parents[((init_x, init_y), 0)] = None  # parent node of initial state is None

    g[((init_x, init_y), 0)] = 0  # weight of initial state is 0
    # f[((init_x, init_y), 0)] = heuristic(init_x, init_y, goal_x, goal_y)  # f = g(initial node) + heuristic

    incumbent = None
    current = None
    opened_states = 1

    while len(open_set) > 0:
        # current = pop_best(closed_set, f, grid, open_set)  # (x, y), t
        f, current = heapq.heappop(open_set)

        closed_set.add(current)
        if current[0] == (goal_x, goal_y):  # if I reached the goal I return the path from init to goal
            if incumbent is None or g[current] < g[incumbent] or (
                    g[current] == g[incumbent] and current[1] < incumbent[1]):
                incumbent = current
            if greedy:
                return reconstruct_path(init_x, init_y, parents, current), current[1], g[current], len(
                    closed_set), opened_states

        if relaxed:
            # compute the relaxed path from current node to goal and verify that it does not collide with other agents
            relaxed_path, time_taken, cost = get_aux_path_and_verify(aux, grid, current[0], agents, current[1],
                                                                     max_length)
            if relaxed_path is not None and time_taken != 0 and cost is not float('inf'):
                # return the path from init to current node + the relaxed path from current node to goal, the time taken
                # to reach the goal, the cost of the path, the number of nodes in the closed set and the number of
                # opened states
                return reconstruct_path(init_x, init_y, parents, current) + relaxed_path[1:], time_taken + current[
                    1], cost + g[current], len(closed_set), opened_states

        if current[1] >= max_length:  # if I reached the maximum length I go to the next iteration of the while loop
            continue

        for n in grid.get_me_and_neighbours(current[0][0],
                                            current[0][1]):  # for all neighbours of current node (included)
            if grid.exists(n[0], n[1]):  # if the neighbour is an obstacle I go to the next iteration of the for loop
                continue

            traversable = True
            for a in agents:  # for all agents check that they are not/will not be in the same position as the neighbour
                if a.get_pos(current[1] + 1) == n or (
                        a.get_pos(current[1] + 1) == current[0] and a.get_pos(current[1]) == n):
                    traversable = False
                    break

            if not traversable:  # if the neighbour is not traversable I go to the next iteration of the for loop
                continue

            move_cost = 1 if grid.is_adjacent_cell(current[0][0], current[0][1], n[0], n[1]) or (
                current[0][0], current[0][1]) == (n[0], n[1]) else math.sqrt(2)  # if the neighbour is adjacent to the
            # current node or there is a wait move, the move cost is 1, otherwise it is sqrt(2)

            if (n, current[1] + 1) in closed_set and g[current] + move_cost >= g[(n, current[1] + 1)]:
                continue

            initialize_dicts(current, g, n, parents)  # instead of initializing all dicts at the beginning I only
            # initialize the ones I need, which helps to save memory

            if g[current] + move_cost < g[(n, current[1] + 1)]:  # if the new path is better than the previous one
                parents[(n, current[1] + 1)] = current  # update the parent of the neighbour
                g[(n, current[1] + 1)] = g[current] + move_cost  # update the weight of the neighbour
                # f[(n, current[1] + 1)] = g[(n, current[1] + 1)] + heuristic(n[0], n[1], goal_x, goal_y)  # update f
            if (n, current[1] + 1) not in list(map(lambda x: x[1], open_set)):
                # if the neighbour is not in the open set I add it and count it as an opened state
                heapq.heappush(open_set,
                               (g[(n, current[1] + 1)] + heuristic(n[0], n[1], goal_x, goal_y), (n, current[1] + 1)))
                # open_set.add((n, current[1] + 1))
                opened_states += 1

    if incumbent is None:  # if the goal is not in g it means that it is not reachable
        return None, 0, float('inf'), 0, 0
    return reconstruct_path(init_x, init_y, parents, incumbent), current[1], g[incumbent], len(
        closed_set), opened_states


def pop_best(closed_set, f, grid, open_set):
    """Returns the item with the best f score from the open_set."""
    best_f = float('inf')
    current = None  # tuple of ((x, y), t)
    for item in open_set:  # item is a tuple of ((x, y), t)
        if f[item] <= best_f and not grid.exists(item[0][0], item[0][1]):
            # if the f score is better than the best one and the position is not an obstacle
            best_f = f[item]  # update the best f score
            current = item  # update the current position
    open_set.remove(current)  # remove the current position from the open set
    closed_set.add(current)  # add the current position to the closed set
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
    # return abs(x1 - x2) ** 2 + abs(y1 - y2) ** 2  # squared Euler's distance
    return abs(x1 - x2) + abs(y1 - y2)  # Manhattan distance


def reconstruct_path(init_x, init_y, parent, current):  # TODO: write pseudocode
    """Returns the path from the initial position to the goal position."""
    if parent[current] is None:  # if the current position is the initial position
        return [current[0]]  # return the current position
    else:
        # return the current position and the path from the initial position to the parent of the current position
        return reconstruct_path(init_x, init_y, parent, parent[current]) + [current[0]]


def dijkstra(graph, goal_x, goal_y, max_length):
    """Returns the shortest path from the initial position to the goal position."""
    parents = dict()  # parents dictionary
    spt_set = dict()  # shortest path tree set
    heap = list()  # heap
    spt_set[(goal_x, goal_y)] = (0, 0)  # weight and time (0, 0) of the goal position
    heapq.heappush(heap, (0, (goal_x, goal_y)))  # push the goal position to the heap
    parents[(goal_x, goal_y)] = None
    while len(heap) > 0:  # while the heap is not empty
        current = heapq.heappop(heap)  # (cost, (x, y))
        # if current[1] == (init_x, init_y):
        #   break
        if spt_set[current[1]][1] > max_length:  # node is too far away
            continue
        for neighbour in graph.get_me_and_neighbours(current[1][0], current[1][1]):  # for each neighbour of the current
            w = 1 if graph.is_adjacent_cell(current[1][0], current[1][1], neighbour[0], neighbour[1]) or (
                current[1][0], current[1][1]) == (neighbour[0], neighbour[1]) else math.sqrt(2)  # compute weight

            if neighbour not in spt_set or spt_set[neighbour][0] > current[0] + w:  # if the neighbour is not in the
                # shortest path tree set or the new path is better than the previous one
                spt_set[neighbour] = (current[0] + w, spt_set[current[1]][1] + 1)  # update the weight and the time
                parents[neighbour] = current[1]  # update the parent of the neighbour
                heapq.heappush(heap, (spt_set[neighbour][0], neighbour))  # push the neighbour to the heap

    return parents


def get_aux_path_and_verify(aux, grid, init, agents, tstart, max_length):  # todo: write pseudocode
    """Returns the path from the initial position to the goal position and the cost of the path, if it is valid."""
    path = []
    node = init
    time = tstart
    while node is not None:
        if time > max_length:  # path is too long (exceeds max_length)
            return None, 0, float('inf')
        path.append(node)
        time += 1
        node = aux[node]

    if is_allowed_path(path, agents, tstart, grid):  # if the path is valid
        cost = 0
        for i in range(len(path) - 1):  # compute the cost of the path
            if path[i] == path[i + 1] or grid.is_adjacent_cell(path[i][0], path[i][1], path[i + 1][0], path[i + 1][1]):
                cost += 1
            else:
                cost += math.sqrt(2)
        return path, max(0, len(path) - 1), cost  # return the path, the time and the cost

    return None, 0, float('inf')


def is_allowed_path(path, agents, tstart, grid):
    """Returns True if the path is valid, False otherwise."""
    if len(path) == 0:  # if the path is empty
        return True
    for i in range(len(path)):  # for each position of the entry agent (EA) in the path
        for agent in agents:  # for each agent
            if path[i] == agent.get_pos(tstart + i):  # if the agent is in the position
                return False
            if i < len(path) - 1 and path[i] == agent.get_pos(tstart + i + 1) and path[i + 1] == agent.get_pos(
                    tstart + i):
                # if agent and EA swap positions
                return False
        if grid.exists(path[i][0], path[i][1]):  # if the position is an obstacle
            return False
        if i < len(path) - 1 and path[i] != path[i + 1] and not grid.is_adjacent_cell(path[i][0], path[i][1],
                                                                                      path[i + 1][0], path[i + 1][1]):
            # if the positions are not adjacent
            return False

    return True
