import multiprocessing
import timing

class MonteCarloEngine:
    def __init__(self, n_simulations, model):
        self.n_simulations = n_simulations
        self.pool = multiprocessing.Pool(multiprocessing.cpu_count())
        self.model = model

    @timing.time_it
    def compute(self):
        result = self.pool.map(self.model.simulate, range(self.n_simulations))
        return result