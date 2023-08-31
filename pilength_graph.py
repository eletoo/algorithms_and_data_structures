import os
import json
from matplotlib import pyplot as plt

output_folder = 'outputs/'
if 'graphs' not in os.listdir(output_folder):
    os.mkdir(output_folder + 'graphs/')

# tempo impiegato al variare della lunghezza dei percorsi preesistenti
xAxis = []
yAxis = []
for i in range(10, 51, 5):
    fn = output_folder + 'iteration_pi_length_' + str(i) + '.json'
    if fn in os.listdir(output_folder):
        xAxis.append(i)
        with open(fn, 'r') as file:
            data = json.load(file)
            yAxis.append(data['solution_additional_info']['execution_time'])

yAxisRel = []
for i in range(10, 51, 5):
    fn = output_folder + 'iteration_pi_length_' + str(i) + '.json'
    if fn in os.listdir(output_folder):
        with open(fn, 'r') as file:
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
