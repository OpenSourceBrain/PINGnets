import sys

import pprint; pp = pprint.PrettyPrinter(depth=6)

from neuromllite.sweep.ParameterSweep import ParameterSweep
from neuromllite.sweep.ParameterSweep import NeuroMLliteRunner
        

if __name__ == '__main__':


    fixed = {'dt':0.025}
    fixed = {}

    quick = False
    #quick=True

    vary = {'stim_amp':['%spA'%(i/10.0) for i in xrange(-10,20,2)]}
    vary = {'stim_amp':['%spA'%(i/10.0) for i in xrange(-10,20,5)]}
    #vary = {'stim_amp':['1.5pA','2pA']}
    
    type = 'Pyr'
    type = 'PV'
    
    nmllr = NeuroMLliteRunner('Sim_IClamp_%s.json'%type,
                              plot_all=True, 
                              show_plot_already=False)

    if quick:
        pass

    ps = ParameterSweep(nmllr, vary, fixed)

    report = ps.run()
    pp.pprint(dict(report))
    
    #ps.plotLines('stim_amp','average_last_1percent',save_figure_to='average_last_1percent_%s.png'%type)
    ps.plotLines('stim_amp','mean_spike_frequency',save_figure_to='mean_spike_frequency_%s.png'%type)
    
    import matplotlib.pyplot as plt
    print("Showing plots")
    plt.show()
    
    '''
    vary['i'] = [1,2,3]

    ps = ParameterSweep(vary,fixed)

    ps.run()'''