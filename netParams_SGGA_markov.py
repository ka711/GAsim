# this is the code for the parameter of SG_test having the markov Na channels
# can be used for creation of SGtest neuron for parameter optimization with GA
# modified by K. Sekiguchi
from netpyne import specs, sim
from neuron import h

try: 
    from __main__ import cfg
except:
    from cfg import cfg

netParams = specs.NetParams() 


# conductance of each Nav channels
cond = {'na11a'  : cfg.na11a, 
        'na12a'  : cfg.na12a, 
        'na13a'  : cfg.na13a,
        'na16a'  : cfg.na16a,
        'KDRI'  : cfg.KDRI
        }


## IMPORT CELL
#netParams.popParams['SG_pop'] = {'cellType': 'SG', 'cellModel': '_SG', 'numCells': 1}
netParams.popParams['testSG_pop'] = {'cellType': 'SG_test', 'cellModel': '_SG_test', 'numCells': 1}

#SGcellRule  = netParams.importCellParams(label='SGrule' , conds={'cellType': 'SG'  ,'cellModel': '_SG'}, fileName='SG.tem' , cellName='SG')
#netParams.cellParams['SGRule' ] = SGcellRule
SGcellRule  = netParams.importCellParams(label='SGrule_test' , conds={'cellType': 'SG_test'  ,'cellModel': '_SG_test'}, fileName='SG_markov.tem' , cellName='SG_test')


# setting of conductance of each Nav channels
SGcellRule['secs']['soma']['mechs']['na11a']['gbar']      = cond['na11a']
SGcellRule['secs']['soma']['mechs']['na12a']['gbar']      = cond['na12a']
SGcellRule['secs']['soma']['mechs']['na13a']['gbar']      = cond['na13a']
SGcellRule['secs']['soma']['mechs']['na16a']['gbar']      = cond['na16a']
SGcellRule['secs']['soma']['mechs']['KDRI']['gkbar']      = cond['KDRI']

SGcellRule['secs']['hillock']['mechs']['na11a']['gbar']   = cond['na11a'] * 430   # roughly based on the conductance at soma and hillock in SG.tem
SGcellRule['secs']['hillock']['mechs']['na12a']['gbar']   = cond['na12a'] * 430
SGcellRule['secs']['hillock']['mechs']['na13a']['gbar']   = cond['na13a'] * 430
SGcellRule['secs']['hillock']['mechs']['na16a']['gbar']   = cond['na16a'] * 430
SGcellRule['secs']['hillock']['mechs']['KDRI']['gkbar']   = cond['KDRI'] * 17.6

SGcellRule['secs']['dend']['mechs']['KDRI']['gkbar']   = cond['KDRI'] * 7.9

netParams.cellParams['SGRule_test' ] = SGcellRule

########################################
## ADD in STIMULATION SOURCE (IClamp) to SG and SGtest neurons
netParams.stimSourceParams['Input'] = {'type': 'IClamp', 'del': 10, 'dur': 500, 'amp':cfg.stim_amp}   # original = {'type': 'IClamp', 'del': 50, 'dur': 5, 'amp':0.5}
#netParams.stimTargetParams['Input->SG_pop'] = {'source': 'Input', 'sec':'soma', 'loc': 0.5, 'conds': {'pop':'SG_pop'}}
netParams.stimTargetParams['Input->testSG_pop'] = {'source': 'Input', 'sec':'soma', 'loc': 0.5, 'conds': {'pop':'testSG_pop'}}

########################################


