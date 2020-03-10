#import netParams_SG # import parameters file
#import netParams_SGGA # import parameters file
import netParams_SGGA_markov # import parameters file

import cfg

from netpyne import sim  # import netpyne init module
from neuron import h

#simConfig, netParams = sim.readCmdLineArgs(simConfigDefault='cfg.py', netParamsDefault='netParams_SG.py')
#simConfig, netParams = sim.readCmdLineArgs(simConfigDefault='cfg.py', netParamsDefault='netParams_SGGA.py')
simConfig, netParams = sim.readCmdLineArgs(simConfigDefault='cfg.py', netParamsDefault='netParams_SGGA_markov.py')

###############################################################################
# create, simulate, and analyse network
###############################################################################
sim.createSimulateAnalyze(netParams = netParams, simConfig = simConfig)


## load the SG neuron profile ##
import json
#data = open('model_output_ori_ina_10ms.json', 'rb')
data = open('./data/original/NaV_0.json', 'rb')
data = json.load(data)

import matplotlib.pyplot as plt

data = open('./data/original/NaV_0.json', 'rb')
data = json.load(data)

plt.plot(data['simData']['t'], data['simData']['V_soma']['cell_0'], label = 'V_soma_B_Na', linestyle = 'dotted')
plt.plot(sim.simData['t'], sim.simData['V_soma']['cell_0'], label = 'V_soma_Na1.3a', linewidth = 2)
plt.xlabel('Time(ms)')
plt.ylabel('voltage (mV)')

plt.legend()
plt.show()


# sum_curr = []
# for i in range(len(sim.simData['na1.1']['cell_0'])):
#     sum_curr_ = sim.simData['na1.1']['cell_0'][i] + sim.simData['na1.2']['cell_0'][i] + sim.simData['na1.3']['cell_0'][i] + sim.simData['na1.6']['cell_0'][i]
#     sum_curr.append(sum_curr_)
# fig, (ax1, ax2) = plt.subplots(2, 1, sharex = True)
# ax1.plot(data['simData']['t'], data['simData']['V_soma']['cell_0'], label = 'V_soma_B_Na', linestyle = 'dotted')
# ax1.plot(sim.simData['t'], sim.simData['V_soma']['cell_0'], label = 'V_soma_sim', linewidth = 2)
# ax1.set(title = 'firing pattern at SG neurons', ylabel = 'voltage (mV)')
# #ax2.plot((data['simData']['t']), (data['simData']['B_Na']['cell_0']), label = 'current_B_Na', linestyle = 'dotted')
# ax2.plot(sim.simData['t'], sum_curr, label = 'ina_total_sim', linewidth = 2)
# ax2.set(xlabel = 'Time (ms)', ylabel = 'current')

# plt.legend()
# plt.show()
