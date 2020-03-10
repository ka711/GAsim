#imports
import pylab              # scientific computing and plotting
from random import Random # pseudorandom number generation
from inspyred import ec   # evolutionary algorithm
import json
import numpy as np
import os

import netParams_SGGA_markov               # neural network designed through netpyne, to be optimized
from netpyne import sim   # neural network design and simulation

try: 
    from __main__ import cfg
except:
    from cfg import cfg

# design parameter generator function, used in the ec evolve function --> final_pop = my_ec.evolve(generator=generate_netparams,...)
def generate_netparams(random, args):
    size = args.get('num_inputs')
    initialParams = [random.uniform(minParamValues[i], maxParamValues[i]) for i in range(size)]
    return initialParams

# design fitness function, used in the ec evolve function --> final_pop = my_ec.evolve(...,evaluator=evaluate_netparams,...)
def evaluate_netparams(candidates, args):
    global fitnessCandidates, fitness
    fitnessCandidates = []

    for icand,cand in enumerate(candidates):
        # modify network params based on this candidate params (genes)
        netParams_SGGA_markov.SGcellRule['secs']['soma']['mechs']['na11a']['gbar']    = cand[0]
        netParams_SGGA_markov.SGcellRule['secs']['soma']['mechs']['na12a']['gbar']    = cand[1]
        netParams_SGGA_markov.SGcellRule['secs']['soma']['mechs']['na13a']['gbar']    = cand[2]
        netParams_SGGA_markov.SGcellRule['secs']['soma']['mechs']['na16a']['gbar']    = cand[3]
        netParams_SGGA_markov.SGcellRule['secs']['soma']['mechs']['KDRI']['gkbar']    = cand[2]

        # create network
        sim.createSimulate(netParams=netParams_SGGA_markov.netParams, simConfig=cfg)

        # calculate FIRING RATE for comparison
        # numSpikes = float(len(sim.simData['spkt']))
        # numCells = float(len(sim.net.cells))
        # duration = cfg.duration/1000.0
        # netFiring = numSpikes/numCells/duration

        # # calculate fitness for this candidate
        # fitness = abs(targetFiring - netFiring)  # minimize absolute difference in firing rate

    ### this is the comparison of sum of current traces
        # target membrane voltage trace from the previous data
        # obs_data = open("model_output_ori_ina.json", "r")               # CHECK for the REFERENCE!!!
        # obs_data = json.load(obs_data)
        # targetCurr_ = obs_data["simData"]["B_Na"]["cell_0"]

        # # calculate MEMBRANE VOLTAGE at interesting point for comparison
        # sum_curr = np.array([])
        # for i in range(len(sim.simData["t"])):
        #     sum_curr = sim.simData["na1.1"]["cell_0"][i] + sim.simData["na1.2"]["cell_0"][i] + sim.simData["na1.6"]["cell_0"][i]
        #     diff_curr = abs(targetCurr_[i] - sum_curr)
        #     sum_curr = np.append(sum_curr, diff_curr)

        # fitness = sum(sum_curr) / 600


 # this is the comparison of membrane voltage traces 
        #target membrane voltage trace from the previous data
        obs_data = open("model_output_ori_ina_10ms.json", "r")               # CHECK for the REFERENCE!!!
        obs_data = open("./data/original/NaV_0.json", "r")    
        obs_data = json.load(obs_data)
        targetMemb_ = obs_data["simData"]["V_soma"]["cell_0"]

        # # calculate MEMBRANE VOLTAGE at interesting point for comparison
        sum_vol = []
        for i in range(len(sim.simData["t"])):
            diff_vol_ = abs(targetMemb_[i] - sim.simData["V_soma"]["cell_0"][i])
            diff_vol = np.array(diff_vol_)
            sum_vol.append(diff_vol)

        # #sum_vol_ext = sum_vol[499:999]    # extract values from 10ms to 20ms
        fitness = sum(sum_vol) / 600

        # add to list of fitness for each candidate
        fitnessCandidates.append(fitness)

        # print candidate parameters, firing rate, and fitness
        #print('\n CHILD/CANDIDATE %d: Network with na11:%.2f, na12:%.2f, na16:%.2f \n FITNESS = %.2f \n'\
        #%(icand, cand[0], cand[1], cand[2], netFiring, fitness))

        # original print candidate parameters, firing rate, and fitness
        print('\n CHILD/CANDIDATE %d: Network with na12a:%.2f, KDRI:%.2f \n  firing rate: %.1f, FITNESS = %.2f \n'\
        %(icand, cand[0], cand[1], fitness))
        #print('\n CHILD/CANDIDATE %d: Network with na11a:%.2f, na12a:%.2f, na13a:%.1f, na16a:%.1f, KDRI:%.1f \n  firing rate: %.1f, FITNESS = %.2f \n'\
        #%(icand, cand[0], cand[1], cand[2], cand[3], cand[4], netFiring, fitness))


    return fitnessCandidates

#main

# create random seed for evolutionary computation algorithm --> my_ec = ec.EvolutionaryComputation(rand)
rand = Random()
rand.seed(1)

# target mean firing rate in Hz for comparison
targetFiring = 20

# min and max allowed value for each param optimized:
#                 na11a, na12, na13, na16, KDRI
minParamValues = [0.005, 0.005, 0.005, 0.005, 0.02]
maxParamValues = [10,   10,   10,   10,   40]

# instantiate evolutionary computation algorithm with random seed
my_ec = ec.EvolutionaryComputation(rand)

# establish parameters for the evolutionary computation algorithm, additional documentation can be found @ pythonhosted.org/inspyred/reference.html
my_ec.selector = ec.selectors.tournament_selection  # tournament sampling of individuals from population (<num_selected> individuals are chosen based on best fitness performance in tournament)

#toggle variators
my_ec.variator = [ec.variators.uniform_crossover,   # biased coin flip to determine whether 'mom' or 'dad' element is passed to offspring design
                 ec.variators.gaussian_mutation]    # gaussian mutation which makes use of bounder function as specified in --> my_ec.evolve(...,bounder=ec.BOunder(minParamValues, maxParamValues),...)

my_ec.replacer = ec.replacers.generational_replacement    # existing generation is replaced by offspring, with elitism (<num_elites> existing individuals will survive if they have better fitness than offspring)

my_ec.terminator = ec.terminators.evaluation_termination  # termination dictated by number of evaluations that have been run

#toggle observers
my_ec.observer = [ec.observers.stats_observer,  # print evolutionary computation statistics
                  ec.observers.plot_observer,   # plot output of the evolutionary computation as graph
                  ec.observers.best_observer]   # print the best individual in the population to screen

''' script for the csv file
projdir = os.path.dirname(os.getcwd())
stat_file_name = '{0}/myDHN_SCS/GAstat/ec_statistics.csv'.format(projdir)
ind_file_name  = '{0}/myDHN_SCS/GAstat/ec_individuals.csv'.format(projdir)
stat_file = open(stat_file_name, 'w')
ind_file  = open(ind_file_name, 'w')

def openFiles2SaveStats(self):
    stat_file_name = '{0}/myDHN_SCS/GAstat/ec_statistics.csv'
    ind_file_name = '{0}/myDHN_SCS/GAstat/ec_individuals.csv'
    individual = open(ind_file_name, 'w')
    stats = open(stat_file_name, 'w')
    stats.write('#gen  pop-size  worst  best  median  average  std-deviation\n')
    individual.write('#gen  #ind  fitness  [candidate]\n')
    return stats, individual
'''

#call evolution iterator
final_pop = my_ec.evolve(generator=generate_netparams,  # assign design parameter generator to iterator parameter generator
                      evaluator=evaluate_netparams,     # assign fitness function to iterator evaluator
                      pop_size=100,       #1000               # original 10 # each generation of parameter sets will consist of 10 individuals
                      maximize=False,                   # best fitness corresponds to minimum value
                      bounder=ec.Bounder(minParamValues, maxParamValues), # boundaries for parameter set ([probability, weight, delay])
                      max_evaluations=500,     #5000         # original 50 # evolutionary algorithm termination at 50 evaluations
                      num_selected=50,      #1000            # original 10 # number of generated parameter sets to be selected for next generation
                      mutation_rate=0.2,                # original 0.2 # rate of mutation
                      num_inputs=5,                     # len([na11a, na12, na13a, na16])
                      num_elites=1, #10
                      #statistics_file = stat_file,
                      #indiduals_file = ind_file
                      )                     # 1 existing individual will survive to next generation if it has better fitness than an individual selected by the tournament selection

#stat_file.close()
#ind_file.close()

#configure plotting
pylab.legend(loc='best')
pylab.show()

# plot raster of top solutions
final_pop.sort(reverse=True)                            # sort final population so best fitness (minimum difference) is first in list
bestCand = final_pop[0].candidate                       # bestCand <-- individual @ start of list
cfg.analysis['plotRaster'] = False            # plotting
netParams_SGGA_markov.SGcellRule['secs']['soma']['mechs']['na11a']['gbar']    = bestCand[0]
netParams_SGGA_markov.SGcellRule['secs']['soma']['mechs']['na12a']['gbar']    = bestCand[1]
netParams_SGGA_markov.SGcellRule['secs']['soma']['mechs']['na13a']['gbar']    = bestCand[2]
netParams_SGGA_markov.SGcellRule['secs']['soma']['mechs']['na16a']['gbar']    = bestCand[3]
netParams_SGGA_markov.SGcellRule['secs']['soma']['mechs']['KDRI']['gkbar']    = bestCand[4]
sim.createSimulateAnalyze(netParams=netParams_SGGA_markov.netParams, simConfig=cfg)   # run simulation of best candidate