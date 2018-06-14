from neuromllite import *
from neuromllite.NetworkGenerator import *

colors = {'Pyr':'.8 0 0','PV':'0 0 .8'}

def generate(ref):
    
    ################################################################################
    ###   Build a new network

    net = Network(id=ref)
    net.notes = "A simple network: %s."%ref
    net.temperature = 37 # degC


    ################################################################################
    ###   Add some cells

    net.cells.append(Cell(id='PV', neuroml2_source_file='WangBuzsaki.cell.nml'))


    ################################################################################
    ###   Add some populations

    comp = 'PV'
    pop_pv = Population(id='pop_%s'%comp, size=1, component=comp, properties={'color':colors[comp]})

    net.populations.append(pop_pv)


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


    input_source = InputSource(id='iclamp0', 
                               pynn_input='DCSource', 
                               parameters={'amplitude':0.0025, 'start':50., 'stop':250.})
                               
    net.input_sources.append(input_source)

    net.inputs.append(Input(id='stim',
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
                     duration='300',
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
    
    generate('IClamp_PV')
    