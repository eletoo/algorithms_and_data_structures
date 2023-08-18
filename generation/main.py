import math
import random
import generation.gen_hilbert_curve as ghc
from generation.Agent import Agent
from generation.matrix import Matrix


def generate_instance(NROWS, NCOLS, NOBSTACLES, AGGLOMERATION_FACTOR, PI_LENGTH, NAGENTS, SEED, INITX, INITY, GOALX,
                      GOALY):
    # instead of saving the adjacency matrix, I save only the list of non-zero elements of the matrix and check every
    # time I have to make a move if the cell is empty. This way I save a lot of memory, especially for large grids with
    # few non-zero elements.
    grid = Matrix(NROWS, NCOLS)
    n_obstacles = NOBSTACLES
    random.seed(SEED)

    offset_x = random.randint(0, NROWS - 1)
    offset_y = random.randint(0, NCOLS - 1)
    for x, y in ghc.gilbert2d(NROWS, NCOLS):  # using the generalized Hilbert curve to fill the grid with obstacles
        if random.random() < AGGLOMERATION_FACTOR:
            if grid.exists((x + offset_x) % NCOLS, (y + offset_y) % NROWS):
                continue  # if the cell is already occupied, skip it
            grid.add((x + offset_x) % NCOLS, (y + offset_y) % NROWS)
            n_obstacles -= 1
            if n_obstacles == 0:
                break

    # To guarantee that the agglomeration factor is exactly the one specified in the parameters.ini file, we'd need to
    # add obstacles until the agglomeration factor is reached. However, this would contradict the requirement for a
    # specific number of obstacles. Therefore, we add obstacles until the number is equal to the one specified in the
    # parameters.ini file, and consider the agglomeration factor as a "secondary" parameter. This means that the
    # agglomeration factor will be slightly lower than the required value.
    # Specifically, the agglomeration factor will be correct for the cells of the grid that are internal to the
    # clusters, while it will be lower than the required value for the cells that are on the border of the clusters.
    # to prove that the agglomeration factor is correct if no constraint is added to the number of obstacles, remove the
    # if n_obstacles == 0: break statement and uncomment the following lines:
    # print(grid.calc_agg_fac())
    # print(AGGLOMERATION_FACTOR)
    # print(grid)

    agents = []
    for i in range(NAGENTS):
        agents.append(Agent(*grid.pick_random_cell([i.get_pos() for i in agents])))
    for t in range(PI_LENGTH):
        for i in range(NAGENTS):
            agents[i].move(grid, [agents[j].get_pos() for j in range(NAGENTS) if j != i])

    init_x, init_y = grid.pick_random_cell([a.get_pos(0) for a in agents]) if INITX is None or INITY is None else (
        INITX, INITY)
    goal_x, goal_y = grid.pick_random_cell(
        [a.get_pos(None) for a in agents] + [(init_x, init_y)]) if GOALX is None or GOALY is None else (
        GOALX, GOALY)

    return grid, agents, init_x, init_y, goal_x, goal_y
