import json
import os

import matplotlib.pyplot as plt

output_folder = 'outputs/'
if 'graphs' not in os.listdir(output_folder):
    os.mkdir(output_folder + 'graphs/')

# memoria occupata in funzione delle dimensioni della griglia
xAxis = [x for x in range(5, 51, 5)]
yAxis = []
for i in range(5, 51, 5):
    str_i = str(i)
    if i < 10:
        str_i = '0' + str(i)
    with open(output_folder + 'iteration_grid_size_' + str_i + '.json', 'r') as file:
        data = json.load(file)
        yAxis.append(data['solution_additional_info']['occupied_memory']['peak'])

yAxisRel = []
for i in range(5, 51, 5):
    str_i = str(i)
    if i < 10:
        str_i = '0' + str(i)
    with open(output_folder + 'iteration_grid_size_' + str_i + '_relaxed.json', 'r') as file:
        data = json.load(file)
        yAxisRel.append(data['solution_additional_info']['occupied_memory']['peak'])

plt.plot(xAxis, yAxis, xAxis, yAxisRel)
plt.legend(['ReachGoal', 'ReachGoal Rilassato'])
plt.xlabel('Dimensioni Griglia')
plt.ylabel('Memoria occupata (B)')
plt.title('Memoria occupata in funzione delle dimensioni della griglia')
plt.grid(True)
plt.savefig(output_folder + 'graphs/dimensioni_griglia_mem.pdf')
plt.clf()

# tempo di esecuzione in funzione delle dimensioni della griglia
xAxis = [x for x in range(5, 51, 5)]
yAxis = []
for i in range(5, 51, 5):
    str_i = str(i)
    if i < 10:
        str_i = '0' + str(i)
    with open(output_folder + 'iteration_grid_size_' + str_i + '.json', 'r') as file:
        data = json.load(file)
        yAxis.append(data['solution_additional_info']['execution_time'])

yAxisRel = []
for i in range(5, 51, 5):
    str_i = str(i)
    if i < 10:
        str_i = '0' + str(i)
    with open(output_folder + 'iteration_grid_size_' + str_i + '_relaxed.json', 'r') as file:
        data = json.load(file)
        yAxisRel.append(data['solution_additional_info']['execution_time'])

plt.plot(xAxis, yAxis, xAxis, yAxisRel)
plt.legend(['ReachGoal', 'ReachGoal Rilassato'])
plt.xlabel('Dimensioni Griglia')
plt.ylabel('Tempo di esecuzione (s)')
plt.title('Tempo di esecuzione in funzione delle dimensioni della griglia')
plt.grid(True)
plt.savefig(output_folder + 'graphs/dimensioni_griglia_time.pdf')
plt.clf()

# numero di stati espansi in funzione delle dimensioni della griglia
xAxis = [x for x in range(5, 51, 5)]
yAxis = []
for i in range(5, 51, 5):
    str_i = str(i)
    if i < 10:
        str_i = '0' + str(i)
    with open(output_folder + 'iteration_grid_size_' + str_i + '.json', 'r') as file:
        data = json.load(file)
        yAxis.append(data['instance_additional_info']['closed_states'])

yAxisRel = []
for i in range(5, 51, 5):
    str_i = str(i)
    if i < 10:
        str_i = '0' + str(i)
    with open(output_folder + 'iteration_grid_size_' + str_i + '_relaxed.json', 'r') as file:
        data = json.load(file)
        yAxisRel.append(data['instance_additional_info']['closed_states'])

y = []
for i in range(len(yAxis)):
    y.append(yAxis[i] - yAxisRel[i])
plt.plot(xAxis, y)
plt.legend(['ReachGoal - ReachGoal Rilassato'])
plt.xlabel('Dimensioni Griglia')
plt.ylabel('Stati Espansi - Stati Espansi Rilassato')
plt.title('Differenza degli Stati Espansi in funzione delle dimensioni della griglia')
plt.grid(True)
plt.savefig(output_folder + 'graphs/dimensioni_griglia_exp.pdf')
plt.clf()

# numero di stati aperti in funzione delle dimensioni della griglia
xAxis = [x for x in range(5, 51, 5)]
yAxis = []
for i in range(5, 51, 5):
    str_i = str(i)
    if i < 10:
        str_i = '0' + str(i)
    with open(output_folder + 'iteration_grid_size_' + str_i + '.json', 'r') as file:
        data = json.load(file)
        yAxis.append(data['instance_additional_info']['opened_states'])

yAxisRel = []
for i in range(5, 51, 5):
    str_i = str(i)
    if i < 10:
        str_i = '0' + str(i)
    with open(output_folder + 'iteration_grid_size_' + str_i + '_relaxed.json', 'r') as file:
        data = json.load(file)
        yAxisRel.append(data['instance_additional_info']['opened_states'])
y = []
for i in range(len(yAxis)):
    y.append(yAxis[i] - yAxisRel[i])
plt.plot(xAxis, y)
plt.legend(['ReachGoal - ReachGoal Rilassato'])
plt.xlabel('Dimensioni Griglia')
plt.ylabel('Stati Aperti - Stati Aperti Rilassato')
plt.title('Differenza degli Stati Aperti in funzione delle dimensioni della griglia')
plt.grid(True)
plt.savefig(output_folder + 'graphs/dimensioni_griglia_open.pdf')
plt.clf()

# tempo impiegato al variare della lunghezza dei percorsi preesistenti
xAxis = [x for x in range(10, 51, 5)]
yAxis = []
for i in range(10, 51, 5):
    with open(output_folder + 'iteration_pi_length_' + str(i) + '.json', 'r') as file:
        data = json.load(file)
        yAxis.append(data['solution_additional_info']['execution_time'])

yAxisRel = []
for i in range(10, 51, 5):
    with open(output_folder + 'iteration_pi_length_' + str(i) + '_relaxed.json', 'r') as file:
        data = json.load(file)
        yAxisRel.append(data['solution_additional_info']['execution_time'])

plt.plot(xAxis, yAxis, xAxis, yAxisRel)
plt.legend(['ReachGoal', 'ReachGoal Rilassato'])
plt.xlabel('Lunghezza Percorsi Preesistenti')
plt.ylabel('Tempo di esecuzione (s)')
plt.title('Tempo di esecuzione in funzione della lunghezza dei percorsi preesistenti')
plt.grid(True)
plt.savefig(output_folder + 'graphs/pi_length_time.pdf')
plt.clf()

# tempo di esecuzione in funzione del numero di ostacoli
xAxis = [x for x in range(10, 1251, 125)]
yAxis = []
for i in range(10, 1251, 125):
    with open(output_folder + 'iteration_n_obstacles_' + str(i) + '.json', 'r') as file:
        data = json.load(file)
        yAxis.append(data['solution_additional_info']['execution_time'])

yAxisRel = []
for i in range(10, 1251, 125):
    with open(output_folder + 'iteration_n_obstacles_' + str(i) + '_relaxed.json', 'r') as file:
        data = json.load(file)
        yAxisRel.append(data['solution_additional_info']['execution_time'])

plt.plot(xAxis, yAxis, xAxis, yAxisRel)
plt.legend(['ReachGoal', 'ReachGoal Rilassato'])
plt.xlabel('Numero di ostacoli')
plt.ylabel('Lunghezza del percorso')
plt.title('Lunghezza del percorso in funzione del numero di ostacoli')
plt.grid(True)
plt.savefig(output_folder + 'graphs/n_obstacles_path_length.pdf')
plt.clf()
