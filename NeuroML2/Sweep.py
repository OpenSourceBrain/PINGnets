import sys

import pprint; pp = pprint.PrettyPrinter(depth=6)

from neuromllite.sweep.ParameterSweep import ParameterSweep
from neuromllite.sweep.ParameterSweep import NeuroMLliteRunner
        

if __name__ == '__main__':


    if '-all' in sys.argv:
        fixed = {'dt':0.025}


        vary = {'stim_amp':['%spA'%(i/10.0) for i in xrange(-10,40,10)]}
        #vary = {'stim_amp':['%spA'%(i/10.0) for i in xrange(-10,20,5)]}
        #vary = {'stim_amp':['1.5pA','2pA']}

        for type in ['Pyr', 'PV']:

            nmllr = NeuroMLliteRunner('Sim_IClamp_%s.json'%type)

            ps = ParameterSweep(nmllr, vary, fixed,
                                        num_parallel_runs=16,
                                        save_plot_all_to='traces_%s.png'%type,
                                        heatmap_all=True,
                                        save_heatmap_to='heatmap_%s.png'%type,
                                        plot_all=True, 
                                        show_plot_already=False)
            
            report = ps.run()

            #ps.plotLines('stim_amp','average_last_1percent',save_figure_to='average_last_1percent_%s.png'%type)
            ps.plotLines('stim_amp','mean_spike_frequency',save_figure_to='mean_spike_frequency_%s.png'%type)

        import matplotlib.pyplot as plt
        print("Showing plots")
        plt.show()
        
        
    elif '-dt' in sys.argv:
        
        optimal_stim = {'PV':1,'Pyr':1}
        

        vary = {'dt':[0.05,0.025,0.01,0.005,0.0025,0.001,0.0005,0.00025,0.0001]}
        #vary = {'dt':[0.1,0.05,0.025,0.01,0.005,0.0025,0.001]}
        #vary = {'dt':[0.05,0.025,0.01,0.005,0.0025,0.001]}
        #vary = {'dt':[0.1,0.05,0.025,0.01,0.005]}
        #vary = {'dt':[0.05,0.025,0.01]}

        for type in optimal_stim:

                run = True
                
                if run:
                
                    fixed = {'duration':700, 'stim_amp':'%spA'%optimal_stim[type]}
                    
                    nmllr = NeuroMLliteRunner('Sim_IClamp_%s.json'%type,
                                              simulator='jNeuroML_NEURON')
                    ps = ParameterSweep(nmllr, 
                                        vary, 
                                        fixed,
                                        num_parallel_runs=16,
                                        save_plot_all_to='dt_traces_%s.png'%type,
                                        heatmap_all=True,
                                        save_heatmap_to='heatmap_dt_%s.png'%type,
                                        plot_all=True, 
                                        show_plot_already=False)

                    report = ps.run()

                    #ps.plotLines('stim_amp','average_last_1percent',save_figure_to='average_last_1percent_%s.png'%type)
                    ps.plotLines('dt','mean_spike_frequency',save_figure_to='mean_spike_frequency_dt_%s.png'%type, logx=True)
                
                

        import matplotlib.pyplot as plt
        if not '-nogui' in sys.argv:
            print("Showing plots")
            plt.show()
        
    else:
        
        fixed = {'dt':0.025}

        quick = False
        #quick=True

        vary = {'stim_amp':['%spA'%(i/10.0) for i in xrange(-10,20,2)]}
        #vary = {'stim_amp':['%spA'%(i/10.0) for i in xrange(-10,20,5)]}
        #vary = {'stim_amp':['1pA','1.5pA','2pA']}

        type = 'Pyr'
        #type = 'PV'

        nmllr = NeuroMLliteRunner('Sim_IClamp_%s.json'%type)

        if quick:
            pass

        ps = ParameterSweep(nmllr, vary, fixed,
                                        num_parallel_runs=16,
                                        save_plot_all_to='dt_traces_%s.png'%type,
                                        heatmap_all=True,
                                        save_heatmap_to='heatmap_dt_%s.png'%type,
                                        plot_all=True, 
                                        show_plot_already=False)

        report = ps.run()
        ps.print_report()

        #ps.plotLines('stim_amp','average_last_1percent',save_figure_to='average_last_1percent_%s.png'%type)
        ps.plotLines('stim_amp','mean_spike_frequency',save_figure_to='mean_spike_frequency_%s.png'%type)

        import matplotlib.pyplot as plt
        print("Showing plots")
        plt.show()