def check_parameters(NROWS, NCOLS, NOBSTACLES, AGGLOMERATION_FACTOR, PI_LENGTH, NAGENTS, MAX):
    if NROWS < 1 or NROWS < 1:
        return False, "The number of rows and columns must be greater than 0"
    if NOBSTACLES < 0 or NOBSTACLES > NROWS * NCOLS:
        return False, "The number of obstacles must be between 0 and the number of cells in the grid"
    if AGGLOMERATION_FACTOR < 0 or AGGLOMERATION_FACTOR > 1:
        return False, "The agglomeration factor must be between 0 and 1"
    if PI_LENGTH < 1 or PI_LENGTH > NROWS * NCOLS:
        return False, "The length of the paths of the agents must be between 1 and the number of cells in the grid"
    if NAGENTS < 1 or NAGENTS > NROWS * NCOLS - NOBSTACLES - 1:
        return False, "The number of agents must be between 1 and the number of free cells in the grid minus 1"
    if MAX < 1:
        return False, "The maximum length of the entry agent's path must be greater than 0"

    return True, ""


def check_initial_and_final_pos(grid, init_x, init_y, goal_x, goal_y, agents):
    if grid.exists(init_x, init_y):
        return False, "The initial position of the entry agent is an obstacle"
    if init_x < 0 or init_x >= grid.width:
        return False, "The initial x coordinate of the entry agent must be between 0 and the number of rows - 1"
    if init_y < 0 or init_y >= grid.height:
        return False, "The initial y coordinate of the entry agent must be between 0 and the number of columns - 1"
    if goal_x < 0 or goal_x >= grid.width:
        return False, "The goal x coordinate of the entry agent must be between 0 and the number of rows - 1"
    if goal_y < 0 or goal_y >= grid.height:
        return False, "The goal y coordinate of the entry agent must be between 0 and the number of columns - 1"

    for a in agents:
        if a.get_pos(0)[0] == init_x and a.get_pos(0)[1] == init_y:
            return False, "The initial position of the entry agent is the same as the initial position of another agent"
    return True, ""
