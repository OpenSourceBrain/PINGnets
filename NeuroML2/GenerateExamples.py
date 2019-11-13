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
        parameters['stim_amp'] = '3pA'
        parameters['stim_delay'] = '100ms'
        parameters['stim_dur'] = '500ms'
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
                     
                     
    return sim, net



if __name__ == "__main__":
    
    if '-all' in sys.argv:
        
        generate('PV',700,'IClamp')
        generate('Pyr',700,'IClamp')
        
    else:
        #generate('IFcurve_PV')
        #sim, net = generate('PV',700,'IClamp')
        sim, net = generate('Pyr',700,'IClamp')
        #generate('IClamp_Pyr')
        
        check_to_generate_or_run(sys.argv, sim)
    