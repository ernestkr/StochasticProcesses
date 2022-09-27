import numpy as np
from .abssimulator import StochasticSimulator,SPManager

# For now I assume distributions are
# np.random
#
class BinomialSP(StochasticSimulator):
    # n an p binomial parameters
    def __init__(length,n,p):
        super().__init__(length)
        self.n = n ; self.p = p;

    def generate_history():
        # Always generate new tape
        tape = np.random.binomial(self.n,self.p,self.length)

    # Add functions that are binomial stochastic process spicific
    def bp_specific():
        pass
   

class ExponentialSumSP(StochasticSimulator):
    def __init__(self,length, rate):
        super().__init__(length)
        self.rate = rate

    def generate_history():
        # Always generate new tape
        tape = np.random.exponential(self.n,self.p,self.length)

    # Add functions that are binomial stochastic process spicific
    def _specific():
        pass
   

class ExponentialMinP(StochasticSimulator):
    def __init__(length,rates : list):
        super().__init__(length)
        self.rates = rates


    def generate_history():
        # Always generate new tape
        tape = np.array([self.length,len(self.rates)])
        for i,rate in enumerate(self.rates):
            tape[:,i]= np.random.exponential(self.n,self.p,self.length)
        final_tape = np.min(tapes,1)# Get the minimum exponential at each instance
        # This should be equal in distribution to the holdin gtimes


    # Add functions that are binomial stochastic process spicific
    def _specific():
        pass
 


# SP manager would manage different stochastic processs
# Embedded Markov Chain Uses 
#   * A single holding time e
class EmbeddedMarkC_BD(SPManager):

    # Can we have an api for distributions?
    # we will assume for now all variables are identically distributed.
    def __init__(self, length,rates):
        self.length = length

        self.a_rate = rates['lambda']
        self.s_rate = rates['mu']

        self.a_prob = self.a_rate/(self.a_rate+self.s_rate)
        self.s_prob = self.s_rate/(self.a_rate+self.s_rate)

        self.holding_times = ExponentialSumSP(length,self.a_rate+self.s_rate)

    # We also need our state transitions
    def generate_history(self, initial_state):
        # This initial State will be Discrete
        
        # We can initialize this before hand because the probability 
        # distribution at every point is the same
        bds = np.random.choice([-1,1],self.length-1,p=[self.s_prob, self.a_prob])
        states = [initial_state]

        for i in range(self.length-1):
            states.append(states[-1] + bds[i])

        #This returns our tape to be later managed by statistics
        return (self.holding_times,states);
    def simulate_n_processes(self):
        pass

class RaceOfExponentials(SPManager):

    def __init__(self, length,rates):
        self.length = length
        self.a_rate = rates['lambda']
        self.s_rate = rates['mu']

    def generate_history(self,initial_state):
        # Create two clocks racing for length
        race = np.zeros(shape=[self.length-1,2])
        # Birth
        race[:,0] = np.random.exponential(scale=(1/self.a_rate),size=self.length-1)
        # Death
        race[:,1] = np.random.exponential(scale=(1/self.s_rate),size=self.length-1)
        
        # Now get min and the index
        holding_times = np.min(race,axis=1)# Values
        bd = np.argmin(race,axis=1)
        bd[bd==0] = -1# Set to deaths

        states = [initial_state]

        # Generate the Path
        for i in range(self.length-1):
            cur_state = states[-1]
            change = bd[i]
            if cur_state == 0:# We only take birth 
                holding_times[i] = race[i,0]
                change = 1
            states.append(cur_state + change)

        return holding_times,states

    def simulate_n_processes(self):
        pass
        
class FightOfBinomials(SPManager):

    # These are determined by # deaths and # of births controlled by two binomial distributions
    def __init__(self,length):
        pass
