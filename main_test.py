from algorithm.solver import reach_goal
from generation.Agent import Agent
from generation.matrix import Matrix
from generation import Parameters_check as pc

m = Matrix(6, 6)
m.add(0, 1)
m.add(1, 1)
m.add(3, 1)
m.add(4, 1)
m.add(5, 1)
print(m)
a = Agent(0, 1)
# a.moves.extend([(2, 1), (2, 0), (3, 0), (4, 0), (5, 0)])

valid, err_msg = pc.check_initial_pos(m, 0, 0, [a, Agent(1, 0)])
if not valid:
    print(err_msg)
    exit(1)

path, t, c = reach_goal(m, [a, Agent(1, 0)], 5, 0, 0, 4, 0)

if path is not None:
    print('Path found:')
    for p in path:
        print(p)
    print('Time taken:', t, '\n')
    print('Cost:', c, '\n')
else:
    print('No path found')

path, t, c = reach_goal(m, [a, Agent(1, 0)], 5, 0, 0, 0, 4, True)

if path is not None:
    print('RELAXED Path found:')
    for p in path:
        print(p)
    print('Time taken:', t, '\n')
    print('Cost:', c, '\n')
else:
    print('No RELAXED path found')
