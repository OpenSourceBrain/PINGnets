
import sys

from neuromllite.utils import load_simulation_json,load_network_json
from neuromllite.NetworkGenerator import generate_and_run

from pyneuroml import pynml

class ParameterSweep():

    def __init__(self, runner, vary, fixed={}):

        print("Initialising ParameterSweep with %s, %s" % (vary, fixed))
        self.runner = runner
        self.fixed = fixed
        self.vary = vary
        self.complete = 0
        self.total_todo = 1
        for v in vary:
            self.total_todo *= len(vary[v])


    def _rem_key(self, d, key):
        r = dict(d)
        del r[key]
        return r


    def _run_instance(self, ** kwargs):

        print('============================================================= \n     Instance (%s/%s): %s' % (self.complete, self.total_todo, kwargs))
        '''     '''
        self.runner.run_once( ** kwargs)


    def _sweep(self, v, f, reference=''):

        #print("  VAR: <%s>\n  FIX <%s>"%(v,f))
        keys = list(v)

        if len(keys) > 1:
            vals = v[keys[0]]
            others = v
            others = self._rem_key(others, keys[0])
            for val in vals:
                all_params = f
                all_params[keys[0]] = val

                self._sweep(others, all_params, reference='%s-%s%s' % (reference, keys[0], val))

        else:
            vals = v[keys[0]]
            for val in vals:
                all_params = f
                all_params[keys[0]] = val
                r = '%s_%s%s' % (reference, keys[0], val)
                all_params['reference'] = 'REFb%s%s' % (self.complete, r)
                self._run_instance( ** all_params)
                self.complete += 1
                
        self.runner.finish()


    def run(self):

        print("Running")
        self._sweep(self.vary, self.fixed)
        
        
class NeuroMLliteRunner():
    
    def __init__(self, nmlliteSim, plot_all=True):
        self.plot_all = plot_all
        self.sim = load_simulation_json(nmlliteSim)
        print self.sim
        
        if self.plot_all:
            self.ax = pynml.generate_plot([],                    
                         [],                   # Add 2 sets of y values
                         "Some traces...",                  # Title
                         labels = [],
                         xaxis = 'Time (ms)',            # x axis legend
                         yaxis = '???',   # y axis legend
                         show_plot_already=False)     # Save figure

        
        
    def run_once(self, ** kwargs):
        print('Running NeuroMLlite simulation...')
        
        network = load_network_json(self.sim.network)
        for a in kwargs:
            network.parameters[a] = kwargs[a]
        
        print network
        traces, events = generate_and_run(self.sim, simulator='jNeuroML', network=network, return_results=True)
        print("Returned traces: %s, events: %s"%(traces.keys(), events.keys()))
        
        if self.plot_all:
            for y in traces.keys():
                if y!='t':
                    label = '%s (%s)'%(y, kwargs)
                    self.ax.plot(traces['t'],traces[y],label=label)
                    
    def finish(self):
        
        if self.plot_all:
            from matplotlib import pyplot as plt
            plt.show()
        

if __name__ == '__main__':


    fixed = {'dt':0.025}
    fixed = {}

    quick = False
    #quick=True


    vary = {'stim_amp':['%spA'%(i/10.0) for i in xrange(-10,20,2)]}
    #vary = {'stim_amp':['1.5pA']}
    
    nmllr = NeuroMLliteRunner('Sim_IClamp_PV.json')

    if quick:
        pass

    ps = ParameterSweep(nmllr, vary, fixed)

    ps.run()
    '''
    vary['i'] = [1,2,3]

    ps = ParameterSweep(vary,fixed)

    ps.run()'''