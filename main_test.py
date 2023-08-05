from algorithm.solver import reach_goal
from generation.Agent import Agent
from generation.matrix import Matrix
from generation import Parameters_check as pc

m = Matrix(6, 6)
m.add(1, 0)
m.add(1, 1)
m.add(1, 3)
m.add(1, 4)
m.add(1, 5)
print(m)
a = Agent(2, 0)
a.moves.extend([(2, 1), (1, 2), (1, 2), (1, 2), (1, 2), (0, 3), (0, 4), (0, 5)])

valid, err_msg = pc.check_initial_pos(m, 0, 0, [a])
if not valid:
    print(err_msg)
    exit(1)

path, t, c = reach_goal(m, [a], 10, 0, 0, 5, 3)

if path is not None:
    print('Path found:')
    for p in path:
        print(p)
    print('Time taken:', t, '\n')
    print('Cost:', c, '\n')
else:
    print('No path found')
