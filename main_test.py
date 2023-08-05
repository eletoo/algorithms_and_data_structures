from algorithm.solver import reach_goal
from generation.Agent import Agent
from generation.matrix import Matrix

m = Matrix(6, 6)
m.add(1, 0)
m.add(1, 1)
m.add(1, 3)
m.add(1, 4)
m.add(1, 5)
print(m)
a = Agent(2, 0)
a.moves.extend([(2, 1), (1, 2), (1, 2), (1, 2), (1, 2), (0, 3), (0, 4), (0, 5)])
path, t, c = reach_goal(m, [a], 10, 0, 0, 5, 5)

if path is not None:
    print('Path found:')
    str_path = ''
    for p in path:
        str_path += p.__str__()
    print(str_path)
    print('Time taken:', t, '\n')
    print('Cost:', c, '\n')
else:
    print('No path found')
