from neuromllite import *
from neuromllite.NetworkGenerator import *
from neuromllite.utils import create_new_model
import sys

colors = {'HH':'0 0 .8',"PV":"0.1254902 0.69803922 0.66666667","Pyr":"0.25490196 0.41176471 0.88235294"}

def generate(cell, duration, config='IClamp'):
    
    reference = "%s_%s"%(config, cell)

    cell_id = '%s'%cell
    if cell=='PV':
        cell_nmll = Cell(id=cell_id, neuroml2_source_file='WangBuzsaki.cell.nml')
    if cell=='Pyr':
        cell_nmll = Cell(id=cell_id, neuroml2_source_file='PyramidalCell.cell.nml')
    synapses = []
    
    ################################################################################
    ###   Add some inputs
    
    if 'IClamp' in config:
        parameters = {}
        parameters['stim_amp'] = '1pA'
        parameters['stim_delay'] = '50ms'
        parameters['stim_dur'] = '200ms'
        input_source = InputSource(id='iclamp_0', 
                                   neuroml2_input='PulseGenerator', 
                                   parameters={'amplitude':'stim_amp', 'delay':'stim_delay', 'duration':'stim_dur'})
      
        
    elif 'PoissonFiringSynapse' in config:
        
        syn_exc = Synapse(id='wbs1', 
                      neuroml2_source_file='WangBuzsakiSynapse.synapse.nml')
    
        synapses.append(syn_exc)

        parameters = {}
        parameters['average_rate'] = '100 Hz'
        parameters['number_per_cell'] = '10'
        input_source = InputSource(id='pfs0', 
                                   neuroml2_input='PoissonFiringSynapse', 
                                   parameters={'average_rate':'average_rate', 
                                               'synapse':syn_exc.id, 
                                               'spike_target':"./%s"%syn_exc.id})
        

    network_filename = '%s.json'%reference         
    
    sim, net = create_new_model(reference,
                     duration, 
                     dt=0.01, # ms 
                     temperature=34, # degC
                     default_region='CA1',
                     parameters = parameters,
                     cell_for_default_population=cell_nmll,
                     color_for_default_population=colors[cell],
                     input_for_default_population=input_source,
                     synapses=synapses,
                     network_filename=network_filename)
             
                    
    chan_id_suffix = ''
    if cell=='Pyr':
        chan_id_suffix = '_pyr'
    sim.recordVariables={'biophys/membraneProperties/na_all/na_chan%s/m/q'%chan_id_suffix:{'all':'*'},
                         'biophys/membraneProperties/na_all/na_chan%s/h/q'%chan_id_suffix:{'all':'*'},
                         'biophys/membraneProperties/k_all/k_chan%s/n/q'%chan_id_suffix:{'all':'*'},}
    sim.to_json_file()
                     
                     
    return sim, net



if __name__ == "__main__":
    
    if '-all' in sys.argv:
        
        generate('PV',300,'IClamp')
        generate('Pyr',300,'IClamp')
        
    else:
        #generate('IFcurve_PV')
        #sim, net = generate('PV',700,'IClamp')
        sim, net = generate('Pyr',300,'IClamp')
        #generate('IClamp_Pyr')
        
        check_to_generate_or_run(sys.argv, sim)
    