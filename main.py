import configparser
import math
import os
import random
import time
import tracemalloc
import json
import gc

from generation import main
from algorithm import solver
from generation import Parameters_check as pc


def print_to_file(seed, init_x, init_y, goal_x, goal_y, iteration_number=0, relaxed=False,
                  generation_method="Pseudo-random",
                  heuristic="Chebyshev distance"):
    name = "iteration_" + str(iteration_number) + relaxed * "_relaxed"
    data = {
        'name': name + '.json',
        'GENERATION_INFO': {
            'master_seed': SEED,
            'seed': seed,
            'n_rows': NROWS,
            'n_columns': NCOLS,
            'n_obstacles': NOBSTACLES,
            'traversable_cells': NROWS * NCOLS - NOBSTACLES,
            'agglomeration_factor': AGGLOMERATION_FACTOR,
            'relaxed_path_enabled': relaxed,
        },
        'ENTRY_AGENT_INFO': {
            'max_entry_agent_path_length': MAX,
            'initial_x': init_x,
            'initial_y': init_y,
            'goal_x': goal_x,
            'goal_y': goal_y,
        },
        'EXISTING_AGENTS_INFO': {
            'agents_path_length': PI_LENGTH,
            'n_agents': NAGENTS,
        },
        'agents':
            [{
                'initial_position': (a.x, a.y),
                'path': a.moves
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
                'initial_position': (init_x, init_y),
                'goal_position': (goal_x, goal_y),
                'path': str(path)
            },
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


def run_simulation(seed, sim_name):
    global grid, agents, valid, err_msg, path, time_taken, cost, expanded_states, opened_states, elapsed_time, allocated_mem

    valid, err_msg = pc.check_parameters(NROWS, NCOLS, NOBSTACLES, AGGLOMERATION_FACTOR, PI_LENGTH, NAGENTS, MAX)
    if not valid:
        print(err_msg)
        return

    grid, agents, init_x, init_y, goal_x, goal_y = main.generate_instance(NROWS, NCOLS, NOBSTACLES,
                                                                          AGGLOMERATION_FACTOR, PI_LENGTH, NAGENTS,
                                                                          seed, INITX, INITY, GOALX, GOALY)

    valid, err_msg = pc.check_initial_and_final_pos(grid, init_x, init_y, goal_x, goal_y, agents)
    if not valid:
        print(err_msg)
        return

    print(grid)
    print('Initial position:', init_x, init_y)
    print('Goal position:', goal_x, goal_y)

    start = time.monotonic()  # to measure execution time
    tracemalloc.start()  # to measure memory usage
    path, time_taken, cost, expanded_states, opened_states = solver.reach_goal(grid, agents, MAX, init_x,
                                                                               init_y, goal_x, goal_y)  # to find path
    elapsed_time = time.monotonic() - start
    allocated_mem = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    print_to_file(seed, init_x, init_y, goal_x, goal_y, iteration_number=sim_name)
    gc.collect()  # garbage collector to free memory

    if path is not None:
        print('Path found:')
        print('->'.join([str(p) for p in path]))
        print('Time taken:', time_taken, '\n')
        print('Cost:', cost, '\n')
    else:
        print('No path found')

    start = time.monotonic()
    tracemalloc.start()
    path, time_taken, cost, expanded_states, opened_states = solver.reach_goal(grid, agents, MAX, init_x,
                                                                               init_y, goal_x, goal_y, True)
    # to find relaxed path
    elapsed_time = time.monotonic() - start
    allocated_mem = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    print_to_file(seed, init_x, init_y, goal_x, goal_y, iteration_number=sim_name, relaxed=True)
    gc.collect()  # to free memory

    if path is not None:
        print('RELAXED Path found:')
        print('->'.join([str(p) for p in path]))
        print('Time taken:', time_taken, '\n')
        print('Cost:', cost, '\n')
    else:
        print('No RELAXED path found')


if __name__ == '__main__':
    # to read parameters from .ini file
    config = configparser.ConfigParser()
    config.read('parameters.ini')
    SEED = int(config['GENERATION']['SEED'])  # for reproducibility; global seed
    master_random = random.Random(SEED)  # master random object, used to generate all other random numbers

    AGGLOMERATION_FACTOR = float(config['GENERATION']['AGGLOMERATION_FACTOR'])

    INITX = None
    INITY = None
    GOALX = None
    GOALY = None

    # ask user if they want to read parameters from file or run simulations
    print('Do you want to read the configuration parameters from manually-edited file? (y/N)'
          '\nIf not, the simulations will be run with automatic parameters')
    answer = input()

    if answer == 'y' or answer == 'Y':
        NROWS = int(config['GENERATION']['NROWS'])
        NCOLS = int(config['GENERATION']['NCOLS'])
        NOBSTACLES = int(config['GENERATION']['NOBSTACLES'])
        INITX = int(config['ENTRY_AGENT']['INITX'])
        INITY = int(config['ENTRY_AGENT']['INITY'])
        GOALX = int(config['ENTRY_AGENT']['GOALX'])
        GOALY = int(config['ENTRY_AGENT']['GOALY'])

        PI_LENGTH = int(
            config['EXISTING_AGENTS']['PI_LENGTH'])  # constant length of the Pi route of the existing agents
        NAGENTS = int(config['EXISTING_AGENTS']['NAGENTS'])

        MAX = int(config['ENTRY_AGENT']['MAX'])

        run_simulation(master_random.randint(0, 2 ** 32), 0)
        # the random seed is produced using the master random object, ensuring that no matter how many times we run the
        # script, the same random numbers will be drawn and all simulations will be reproducible
    elif answer == 'n' or answer == 'N' or answer == '':  # automatic simulations
        print('Varying grid size...')
        for i in range(5, 51, 5):  # grid size varies from 10x10 to 50x50, 10 simulations
            NROWS = i
            NCOLS = i

            NAGENTS = math.floor(0.2 * NROWS * NCOLS)  # 20% of the grid is occupied by agents
            NOBSTACLES = math.floor(NROWS * NCOLS * 0.5)  # 50% grid occupied by obstacles
            PI_LENGTH = math.floor((NROWS * NCOLS - NOBSTACLES - NAGENTS - 1) * 0.5)  # 50% of the remaining cells
            MAX = math.floor(0.5 * (NROWS * NCOLS - NOBSTACLES - PI_LENGTH))  # as per the instructions by the professor

            run_simulation(master_random.randint(0, 2 ** 32), 'grid_size_' + str(i if i > 9 else '0' + str(i)))
        print('Varying number of obstacles...')
        for i in range(10, 1251, 125):  # number of obstacles varies from 10 to 1250, 10 simulations
            NOBSTACLES = i

            NROWS = math.floor(math.sqrt(NOBSTACLES * 2))  # to make sure that obstacles are 50% of the grid
            NCOLS = math.floor(math.sqrt(NOBSTACLES * 2))
            NAGENTS = math.floor(0.2 * NROWS * NCOLS)  # 20% of the grid is occupied by agents
            PI_LENGTH = math.floor((NROWS * NCOLS - NOBSTACLES - NAGENTS - 1) * 0.5)
            MAX = math.floor(0.5 * (NROWS * NCOLS - NOBSTACLES - PI_LENGTH))

            run_simulation(master_random.randint(0, 2 ** 32), 'n_obstacles_' + str(i))
        print('Varying number of existing agents...')
        for i in range(10, 501, 50):  # number of existing agents varies from 10 to 500, 10 simulations
            NAGENTS = i

            NROWS = math.floor(math.sqrt(NAGENTS / 0.2))  # to make sure that agents are 20% of the grid
            NCOLS = math.floor(math.sqrt(NAGENTS / 0.2))
            NOBSTACLES = math.floor(NROWS * NCOLS * 0.5)
            PI_LENGTH = math.floor((NROWS * NCOLS - NOBSTACLES - NAGENTS - 1) * 0.5)
            MAX = math.floor(0.5 * (NROWS * NCOLS - NOBSTACLES - PI_LENGTH))

            run_simulation(master_random.randint(0, 2 ** 32), 'n_agents_' + str(i))
        print('Varying length of existing agents paths...')
        for i in range(10, 51, 5):  # length of existing agents paths varies from 10 to 50, 10 simulations
            PI_LENGTH = i

            NROWS = math.floor(PI_LENGTH)
            NCOLS = math.floor(PI_LENGTH)
            NOBSTACLES = math.floor(NROWS * NCOLS * 0.5)
            NAGENTS = math.floor(0.2 * NROWS * NCOLS)
            MAX = math.floor(0.5 * (NROWS * NCOLS - NOBSTACLES - PI_LENGTH))

            run_simulation(master_random.randint(0, 2 ** 32), 'pi_length_' + str(i))
        print('Varying maximum length of entry agent path...')
        for i in range(10, 51, 5):  # maximum length of entry agent path varies from 10 to 50, 10 simulations
            MAX = i

            NROWS = math.floor(MAX)
            NCOLS = math.floor(MAX)
            NOBSTACLES = math.floor(NROWS * NCOLS * 0.6)
            NAGENTS = math.floor(0.2 * NROWS * NCOLS)
            PI_LENGTH = math.floor((NROWS * NCOLS - NOBSTACLES - NAGENTS - 1) * 0.5)
            run_simulation(master_random.randint(0, 2 ** 32), 'max_' + str(i))
    else:
        print('Invalid input')
        exit(0)
