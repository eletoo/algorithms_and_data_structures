import configparser
import os
import time
import tracemalloc
import json

from generation import main
from algorithm import solver
from generation import Parameters_check as pc


def print_to_file(iteration_number=0, relaxed=False, generation_method="Pseudo-random",
                  heuristic="Squared Euler's distance"):
    name = "iteration_" + str(iteration_number) + relaxed * "_relaxed"
    data = {
        'name': name + '.json',
        'GENERATION_INFO': {
            'seed': SEED,
            'n_rows': NROWS,
            'n_columns': NCOLS,
            'n_obstacles': NOBSTACLES,
            'traversable_cells': NROWS * NCOLS - NOBSTACLES,
            'agglomeration_factor': AGGLOMERATION_FACTOR,
            'relaxed_path_enabled': relaxed,
        },
        'ENTRY_AGENT_INFO': {
            'max_entry_agent_path_length': MAX,
            'initial_x': INITX,
            'initial_y': INITY,
            'goal_x': GOALX,
            'goal_y': GOALY,
        },
        'EXISTING_AGENTS_INFO': {
            'agents_path_length': PI_LENGTH,
            'n_agents': NAGENTS,
        },
        'grid': str(grid),
        'agents':
            [{
                'initial_position': (a.x, a.y),
                'path': [a.moves for a in agents]
            } for a in agents],
        'instance_additional_info': {
            'path_found': path is not None,
            'time_taken': time_taken,
            'cost': cost,
            'closed_states': expanded_states,
            'opened_states': opened_states,
            'agents_path_generation_method': generation_method,
        },
        'solution_additional_info': {
            'entry_agent_path': {
                'initial_position': (INITX, INITY),
                'goal_position': (GOALX, GOALY),
                'path': str(path)
            },
            'visited_states': 'todo',  # todo: add visited states
            'heuristic': heuristic,
            'path_length': len(path) if path is not None else 'No path found',
            'cost': cost,
            'execution_time': elapsed_time,
            'occupied_memory': {
                'current': allocated_mem[0],
                'peak': allocated_mem[1],
                'unit': 'bytes'
            }
        }
    }
    if 'outputs' not in os.listdir():
        os.mkdir('outputs')
    with open('outputs/' + name + '.json', 'w') as f:
        json.dump(data, f)


if __name__ == '__main__':
    # read parameters from .ini file
    config = configparser.ConfigParser()
    config.read('parameters.ini')

    SEED = int(config['GENERATION']['SEED'])  # for reproducibility
    NROWS = int(config['GENERATION']['NROWS'])
    NCOLS = int(config['GENERATION']['NCOLS'])
    NOBSTACLES = int(config['GENERATION']['NOBSTACLES'])
    AGGLOMERATION_FACTOR = float(config['GENERATION']['AGGLOMERATION_FACTOR'])

    PI_LENGTH = int(config['EXISTING_AGENTS']['PI_LENGTH'])  # constant length of the Pi route of the existing agents
    NAGENTS = int(config['EXISTING_AGENTS']['NAGENTS'])

    MAX = int(config['ENTRY_AGENT']['MAX'])  # maximum length of the route of the entry agent
    INITX = int(config['ENTRY_AGENT']['INITX'])  # initial x position of the entry agent
    INITY = int(config['ENTRY_AGENT']['INITY'])  # initial y position of the entry agent
    GOALX = int(config['ENTRY_AGENT']['GOALX'])  # goal x position of the entry agent
    GOALY = int(config['ENTRY_AGENT']['GOALY'])  # goal y position of the entry agent

    valid, err_msg = pc.check_parameters(NROWS, NCOLS, NOBSTACLES, AGGLOMERATION_FACTOR, PI_LENGTH, NAGENTS, MAX,
                                         INITX, INITY, GOALX, GOALY)
    if not valid:
        print(err_msg)
        exit(1)

    grid, agents = main.generate_instance(NROWS, NCOLS, NOBSTACLES, AGGLOMERATION_FACTOR, PI_LENGTH, NAGENTS, SEED)

    valid, err_msg = pc.check_initial_pos(grid, INITX, INITY, agents)
    if not valid:
        print(err_msg)
        exit(1)

    print(grid)
    start = time.time()
    tracemalloc.start()
    path, time_taken, cost, expanded_states, opened_states = solver.reach_goal(grid, agents, MAX, INITX,
                                                                               INITY, GOALX, GOALY)
    elapsed_time = time.time() - start
    allocated_mem = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print_to_file(iteration_number=1)

    if path is not None:
        print('Path found:')
        for p in path:
            print(p)
        print('Time taken:', time_taken, '\n')
        print('Cost:', cost, '\n')
    else:
        print('No path found')

    # todo: checks on the input parameters (e.g. if the initial and goal positions are valid)

    start = time.time()
    tracemalloc.start()
    path, time_taken, cost, expanded_states, opened_states = solver.reach_goal(grid, agents, MAX, INITX,
                                                                               INITY, GOALX, GOALY, True)
    elapsed_time = time.time() - start
    allocated_mem = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print_to_file(iteration_number=1, relaxed=True)

    if path is not None:
        print('RELAXED Path found:')
        for p in path:
            print(p)
        print('Time taken:', time_taken, '\n')
        print('Cost:', cost, '\n')
    else:
        print('No RELAXED path found')
