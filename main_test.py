from algorithm.solver import reach_goal
from generation.Agent import Agent
from generation.matrix import Matrix
from generation import Parameters_check as pc

m = Matrix(6, 6)  # 6x6 matrix, indexed from 0 to 5
m.add(0, 1)  # add obstacle at (0, 1)
m.add(1, 1)
m.add(3, 1)
m.add(4, 1)
m.add(5, 1)
print(m)
a = Agent(0, 1)  # agent at initial position (0, 1)
a.moves.extend([(2, 1), (2, 0), (3, 0), (4, 0), (5, 0)])  # agent's path

a2 = Agent(1, 1)  # agent at initial position (0, 1)
a2.moves.extend([(2, 0), (3, 0), (4, 0), (5, 0)])  # agent's path

grid, init_x, init_y, goal_x, goal_y, agents = m, 0, 0, 4, 0, [a, a2]
valid, err_msg = pc.check_initial_and_final_pos(grid, init_x, init_y, goal_x, goal_y, agents)
if not valid:
    print(err_msg)
    exit(1)

max_length = 5
path, t, c = reach_goal(m, [a, a2], max_length, init_x, init_y, goal_x, goal_y)

if path is not None:
    print('Path found:')
    for p in path:
        print(p)
    print('Time taken:', t, '\n')
    print('Cost:', c, '\n')
else:
    print('No path found')

path, t, c = reach_goal(m, [a, a2], max_length, init_x, init_y, goal_x, goal_y, relaxed=True)

if path is not None:
    print('RELAXED Path found:')
    for p in path:
        print(p)
    print('Time taken:', t, '\n')
    print('Cost:', c, '\n')
else:
    print('No RELAXED path found')
