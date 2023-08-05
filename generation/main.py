import math
import random
import generation.gen_hilbert_curve as ghc
from generation.Agent import Agent
from generation.matrix import Matrix


def generate_instance(NROWS, NCOLS, NOBSTACLES, AGGLOMERATION_FACTOR, PI_LENGTH, NAGENTS, SEED):
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

    #    moves = dict()
    #    costs = [0 for _ in range(NAGENTS)]
    #    for t in range(PI_LENGTH):
    #        moves[t] = dict()
    #        for i in range(NAGENTS):
    #            if t == 0:  # initial position
    #                pos = (random.randint(0, NROWS - 1), random.randint(0, NCOLS - 1))
    #
    #                while grid.get(pos[0], pos[1]) or pos in moves[t].values():
    #                    # if the position is occupied by an obstacle or by another agent, choose another one
    #                    pos = (random.randint(0, NROWS - 1), random.randint(0, NCOLS - 1))
    #                moves[t][i] = pos
    #            else:
    #                next_move = random.choice(
    #                    grid.get_neighbours(moves[t - 1][i][0], moves[t - 1][i][1]) + [moves[t - 1][i]])
    #
    #                while next_move in moves[t].values() or grid.get(next_move[0], next_move[1]):
    #                    # if the position is occupied by an obstacle or by another agent choose another one
    #                    next_move = random.choice(
    #                        grid.get_neighbours(moves[t - 1][i][0], moves[t - 1][i][1]) + [moves[t - 1][i]])
    #                moves[t][i] = next_move
    #                if grid.is_adjacent_cell(moves[t - 1][i][0], moves[t - 1][i][1], moves[t][i][0], moves[t][i][1]):
    #                    costs[i] += 1
    #                elif grid.is_diagonal_cell(moves[t - 1][i][0], moves[t - 1][i][1], moves[t][i][0], moves[t][i][1]):
    #                    costs[i] += math.sqrt(2)

    return grid, agents

