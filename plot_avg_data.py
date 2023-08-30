import os
import json

import numpy as np
from matplotlib import pyplot as plt

paths = ['outputs/', 'outputs1/', 'outputs2/', 'outputs3/', 'outputs4/', 'outputs5/', 'outputs6/', 'outputs7/',
         'outputs8/', 'outputs9/', 'outputs10/', 'outputs11/', 'outputs12/', 'outputs13/', 'outputs14/']

files = dict()
files_relaxed = dict()
for i in range(len(paths)):
    files_relaxed[i] = [f for f in os.listdir(paths[i]) if
                        f.startswith('iteration_grid_size_') and f.endswith('relaxed.json')]
    files[i] = [f for f in os.listdir(paths[i]) if
                f.startswith('iteration_grid_size_') and not f.endswith('relaxed.json')]

# occupazione di memoria in funzione delle dimensioni della griglia
xAxis = [x for x in range(5, 51, 5)]
yaxis = dict()
# for every row in yaxis, fill the row with the values of the corresponding file
for i in range(len(files)):
    yaxis[i] = [0 for x in range(len(files[i]))]
    for j in range(len(files[i])):
        f = files[i][j]
        file = open(paths[i] + '/' + f, 'r')
        data = json.load(file)
        yaxis[i][j] = data['solution_additional_info']['occupied_memory']['peak']
        file.close()

y = []
# compute the average value of each column of yaxis and put it in y
for i in range(len(xAxis)):
    y.append(0)
    for j in range(len(yaxis)):
        y[i] += yaxis[j][i]
    y[i] /= len(yaxis)

# occupazione di memoria in funzione delle dimensioni della griglia (rilassato)
yaxis_relaxed = dict()
for i in range(len(files_relaxed)):
    yaxis_relaxed[i] = [0 for x in range(len(files_relaxed[i]))]
    for j in range(len(files_relaxed[i])):
        f = files_relaxed[i][j]
        file = open(paths[i] + '/' + f, 'r')
        data = json.load(file)
        yaxis_relaxed[i][j] = data['solution_additional_info']['occupied_memory']['peak']
        file.close()

yRel = []
for i in range(len(xAxis)):
    yRel.append(0)
    for j in range(len(yaxis_relaxed)):
        yRel[i] += yaxis_relaxed[j][i]
    yRel[i] /= len(yaxis_relaxed)

fit = np.polyfit(xAxis, y, 2)
fit_fn = np.poly1d(fit)
fit2 = np.polyfit(xAxis, yRel, 2)
fit_fn2 = np.poly1d(fit2)
yfn = fit_fn(xAxis)
for i in range(len(yfn)):
    if yfn[i] < 0:
        yfn[i] = 0

yfn2 = fit_fn2(xAxis)
for i in range(len(yfn2)):
    if yfn2[i] < 0:
        yfn2[i] = 0

plt.plot(xAxis, y, xAxis, yRel, xAxis, yfn, '--k', xAxis, yfn2, '--r')
plt.legend(['ReachGoal', 'ReachGoal Rilassato', 'Funzione approx ReachGoal (deg 2)',
            'Funzione approx ReachGoal Rilassato (deg 2)'])
plt.xlabel('Dimensioni Griglia')
plt.ylabel('Memoria Media Occupata (B) [su ' + str(len(files)) + ' simulazioni]')
plt.title('Memoria media occupata in funzione delle dimensioni della griglia')
plt.grid(True)
plt.savefig('avg_dimensioni_griglia_mem.pdf')
plt.clf()
