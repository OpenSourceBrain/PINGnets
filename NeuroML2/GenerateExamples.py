from neuromllite import *
from neuromllite.NetworkGenerator import *

colors = {'Pyr':'.8 0 0','PV':'0 0 .8'}

def generate(ref):
    
    ################################################################################
    ###   Build a new network

    net = Network(id=ref)
    net.notes = "A simple network: %s."%ref
    net.temperature = 37 # degC
    net.parameters = {}
    

    ################################################################################
    ###   Add some regions
    
    r1 = RectangularRegion(id='region1', x=0,y=0,z=0,width=1000,height=100,depth=1000)
    net.regions.append(r1)


    ################################################################################
    ###   Add some cells

    if 'PV' in ref:
        net.cells.append(Cell(id='PV', neuroml2_source_file='WangBuzsaki.cell.nml'))
    if 'Pyr' in ref:
        net.cells.append(Cell(id='Pyr', neuroml2_source_file='PyramidalCell.cell.nml'))
    


    ################################################################################
    ###   Add some synapses
    
    ampa = 'wbsFake'
    net.synapses.append(Synapse(id=ampa, 
                                lems_source_file='WangBuzsakiSynapse.xml'))



    ################################################################################
    ###   Add some populations

    if 'PV' in ref:
        comp = 'PV'
        duration = 3000
        size = 1 if 'IClamp' in ref else 10
        
        pop_pv = Population(id='pop_%s'%comp, 
                            size=size, 
                            component=comp, 
                            properties={'color':colors[comp]},
                            random_layout = RandomLayout(region=r1.id))


        net.populations.append(pop_pv)
        
    if 'Pyr' in ref:
        comp = 'Pyr'
        duration = 3000
        size = 1 if 'IClamp' in ref else 10
        
        pop_pyr = Population(id='pop_%s'%comp, 
                            size=size, 
                            component=comp, 
                            properties={'color':colors[comp]},
                            random_layout = RandomLayout(region=r1.id))


        net.populations.append(pop_pyr)


    ################################################################################
    ###   Add a projection

    '''
    net.projections.append(Projection(id='proj0',
                                      presynaptic=p0.id, 
                                      postsynaptic=p1.id,
                                      synapse='ampa'))

    net.projections[0].random_connectivity=RandomConnectivity(probability=0.5)'''
    
 
    ################################################################################
    ###   Add some inputs
    
    if 'IClamp' in ref:
        net.parameters['stim_amp'] = '1.25pA'
        input_source = InputSource(id='iclamp_0', 
                                   neuroml2_input='PulseGenerator', 
                                   parameters={'amplitude':'stim_amp', 'delay':'0ms', 'duration':'%sms'%duration})

        net.input_sources.append(input_source)

        pop = pop_pyr if 'Pyr' in ref else pop_pv
        net.inputs.append(Input(id='Stim0',
                                input_source=input_source.id,
                                population=pop.id,
                                percentage=100))
        
    else:

        input_source = InputSource(id='pfs0', 
                                   neuroml2_input='PoissonFiringSynapse', 
                                   parameters={'average_rate':'50 Hz', 'synapse':ampa, 'spike_target':"./%s"%ampa})

        net.input_sources.append(input_source)


        net.inputs.append(Input(id='Stim0',
                                input_source=input_source.id,
                                population=pop_pv.id,
                                percentage=100))


    ################################################################################
    ###   Save to JSON format

    net.id = ref

    print(net.to_json())
    new_file = net.to_json_file('Example_%s.json'%net.id)
    

    ################################################################################
    ###   Build Simulation object & save as JSON

    sim = Simulation(id='Sim_%s'%ref,
                     network=new_file,
                     duration=duration,
                     dt='0.025',
                     recordTraces={'all':'*'})

    sim.to_json_file()


    ################################################################################
    ###   Export to some formats
    ###   Try:
    ###        python Example1.py -graph2

    import sys
    check_to_generate_or_run(sys.argv, sim)



if __name__ == "__main__":
    
    #generate('IFcurve_PV')
    generate('IClamp_PV')
    #generate('IClamp_Pyr')
    