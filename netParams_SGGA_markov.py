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

## IMPORT CELL
netParams.popParams['testSG_pop'] = {'cellType': 'SG_test', 'cellModel': '_SG_test', 'numCells': 1}
SGcellRule  = netParams.importCellParams(label='SGrule_test' , conds={'cellType': 'SG_test'  ,'cellModel': '_SG_test'}, fileName='SG_markov.tem' , cellName='SG_test')

# setting of conductance of each Nav channels
cond = {'na11a'  : cfg.na11a, 'na12a'  : cfg.na12a, 'na13a'  : cfg.na13a, 'na16a'  : cfg.na16a, 'KDRI'  : cfg.KDRI}

#original value for na, khil and kdend; 430, 17.6, 7.9
sec_ratio_na = 350
sec_ratio_na12 = 100    
sec_ratio_khil = 60
sec_ratio_kdend = 7.9

SGcellRule['secs']['soma']['mechs']    = {'na11a': {'gbar': cond['na11a']},
                                          'na12a': {'gbar': cond['na12a']},
                                          'na13a': {'gbar': cond['na13a']},
                                          'na16a': {'gbar': cond['na16a']},
                                          'KDRI' : {'gkbar': cond['KDRI' ]}}

SGcellRule['secs']['hillock']['mechs'] = {'na11a': {'gbar': cond['na11a'] * sec_ratio_na},
                                          'na12a': {'gbar': cond['na12a'] * sec_ratio_na12},
                                          'na13a': {'gbar': cond['na13a'] * sec_ratio_na},
                                          'na16a': {'gbar': cond['na16a'] * sec_ratio_na},
                                          'KDRI' : {'gkbar': cond['KDRI' ] * sec_ratio_khil}}

SGcellRule['secs']['dend']['mechs']    = {'KDRI' : {'gkbar': cond['KDRI']  * sec_ratio_kdend}}

netParams.cellParams['SGRule_test' ] = SGcellRule

########################################
## ADD in STIMULATION SOURCE (IClamp) to SG and SGtest neurons
netParams.stimSourceParams['Input'] = {'type': 'IClamp', 'del': 10, 'dur': cfg.stim_dur, 'amp':0.0}
netParams.stimTargetParams['Input->testSG_pop'] = {'source': 'Input', 'sec':'soma', 'loc': 0.5, 'conds': {'pop':'testSG_pop'}}

########################################


