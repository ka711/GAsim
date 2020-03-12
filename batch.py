from netpyne import specs
from netpyne.batch import Batch

''' Example of evolutionary algorithm optimization of a network using NetPyNE
2 examples are provided: 'simple' and 'complex'
In 'simple', 3 parameters are optimized to match target firing rates in 2 populations
In 'complex', 6 parameters are optimized to match target firing rates in 6 populations

To run use: mpiexec -np [num_cores] nrniv -mpi batchRun.py
'''

def batchEvol():
    # parameters space to explore
    
    ## simple net
    params = specs.ODict()
    params['na11a'] = [0.001, 0.2]
    params['na12a'] = [0.001, 0.2]
    params['na13a'] = [0.001, 0.2]
    params['na16a'] = [0.001, 0.2]


    # fitness function
    fitnessFuncArgs = {}	

    def fitnessFunc(simData, **kwargs):
        import numpy as np
        import json

        with open("./data/original/NaV_0.json", "r") as f:
            obs_data = json.load(f)
        targetMemb_ = obs_data["simData"]["V_soma"]["cell_0"]

        # # calculate MEMBRANE VOLTAGE at interesting point for comparison
        sum_vol = []
        for i in range(len(simData["t"])):
            diff_vol_ = abs(targetMemb_[i] - simData["V_soma"]["cell_0"][i])
            diff_vol = np.array(diff_vol_)
            sum_vol.append(diff_vol)

        fitness = sum(sum_vol) / 600
        return fitness

        
    # create Batch object with paramaters to modify, and specifying files to use
    b = Batch(params=params)
    
    # Set output folder, grid method (all param combinations), and run configuration
    b.batchLabel = 'na_evol'
    b.saveFolder = './'+b.batchLabel
    b.method = 'evol'
    b.runCfg = {
        'type': 'mpi_bulletin',#'hpc_slurm', 
        'script': 'init_SG.py',
        # options required only for hpc
        'mpiCommand': 'mpirun',  
        'nodes': 1,
        'coresPerNode': 2,
        'allocation': 'default',
        'email': 'salvadordura@gmail.com',
        'reservation': None,
        'folder': '/home/salvadord/evol'
        #'custom': 'export LD_LIBRARY_PATH="$HOME/.openmpi/lib"' # only for conda users
    }
    b.evolCfg = {
        'evolAlgorithm': 'custom',
        'fitnessFunc': fitnessFunc, # fitness expression (should read simData)
        'fitnessFuncArgs': fitnessFuncArgs,
        'pop_size': 2,
        'num_elites': 1, # keep this number of parents for next generation if they are fitter than children
        'mutation_rate': 0.4,
        'crossover': 0.5,
        'maximize': False, # maximize fitness function?
        'max_generations': 2,
        'time_sleep': 5, # wait this time before checking again if sim is completed (for each generation)
        'maxiter_wait': 40, # max number of times to check if sim is completed (for each generation)
        'defaultFitness': 10000 # set fitness value in case simulation time is over
    }
    # Run batch simulations
    b.run()

# Main code
if __name__ == '__main__':
    batchEvol() 
