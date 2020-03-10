from netpyne import specs, sim
from netpyne.specs import Dict, ODict

cfg = specs.SimConfig()	                          # object of class SimConfig to store simulation configuration


## Nav conductivity
#cfg.nascale = 0.23
cfg.na11   = 0.02#0.002              # Nav1.1, 1.2, 1.3, 1.6 : 1:5:5:1 in wister rat expression
cfg.na12   = 30
cfg.na13   = 7  #0.007
cfg.na16   = 2#0.002

cfg.KDRI    = 0.30#0.52

# variables for markov channels
cfg.na11a   = 0 #0.05     #0.001    #0.002             
cfg.na12a   = 0     #0.01335 is the best for alone     #0.03
cfg.na13a   = 0.189     #0.189 best #0.188    #0.007
cfg.na16a   = 0     #0.001    #0.002


# Duration of stimulus
cfg.stim_amp = 0.01

## other configuration
cfg.duration = 600 				    # Duration of the simulation, in ms
cfg.dt = 0.02 							# Internal integration timestep to use
cfg.verbose = 1							# Show detailed messages 
cfg.recordTraces = {'V_soma' :{'sec': 'soma', 'loc' : 0.5,'var' : 'v'        }, 
                    #'B_Na'  :{'sec': 'soma', 'loc' : 0.5,'var' : 'ina_B_Na' },
                    'na1.1'  :{'sec': 'soma', 'loc' : 0.5,'var' : 'ina_ina2005'},
                    'na1.2'  :{'sec': 'soma', 'loc' : 0.5,'var' : 'ina_na12'},
                    'na1.3'  :{'sec': 'soma', 'loc' : 0.5,'var' : 'ina_nav13'},
                    'na1.6'  :{'sec': 'soma', 'loc' : 0.5,'var' : 'ina_na16'},
                    #'na1.1'  :{'sec': 'soma', 'loc' : 0.5,'var' : 'ina_na11a'},
                    #'na1.2'  :{'sec': 'soma', 'loc' : 0.5,'var' : 'ina_na12a'},
                    #'na1.3'  :{'sec': 'soma', 'loc' : 0.5,'var' : 'ina_na13a'},
                    #'na1.6'  :{'sec': 'soma', 'loc' : 0.5,'var' : 'ina_na16a'},
                    }  # Dict with traces to record
cfg.recordStep = 0.02 			
cfg.filename = 'model_output'  			# Set file output name
#cfg.saveJson = True
#cfg.analysis['plotTraces'] = {'include': [0], 'overlay': True, 'oneFigPer': 'cell', 'saveFig': 'sim_%s' %(cfg.stim_amp)} # Plot recorded traces for this list of cells
cfg.analysis['plotTraces'] = {'include': [0, 1], 'saveFig': True} # Plot recorded traces for this list of cells
cfg.hParams['celsius'] = 37

# Saving
cfg.simLabel = 'sim'
cfg.saveFolder = 'data'
cfg.savePickle = False
cfg.saveJson = True
cfg.saveDataInclude = ['simData', 'simConfig', 'netParams']