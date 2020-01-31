import creditportfolio as cp
import gaussian_copula as gc
import timing as mytime
import pandas as pd
import collections
if __name__ == "__main__":
    rho = 0.2
    dim = 1
    Sig = gc.UniformCorrMatrix(rho, dim)
    X = gc.Gaussian_Vector_Simulation(dim, Sig)
    X.Simulate()
    mytime.timing_it(X.Simulate, 100)
    
    ids = [104190 ,101044, 183410, 104190]
    exposures = [1000, 2000, 500, 444]
    pds = [0.02, 0.03, 0.01, 0.2]
    
    CreditContract = collections.namedtuple('CreditContract', 'id exposure pd')
    cc1 = CreditContract(104190, 1000, 0.02)
    cc2 = CreditContract(101044, 2000, 0.03)
    print(cc1, cc2)

    param_dict = {'id' : ids, 
                  'exposure' : exposures, 
                  'pd' : pds,
                }
    
    my_pf = pd.DataFrame(param_dict)
    
    aggregate_by =  my_pf.groupby('id').agg({'exposure' : ['sum']})
    print(aggregate_by)


    parameters = zip(ids, exposures, pds)
    fmap_contracts = lambda i_e_p : cp.CreditContract(i_e_p[0], i_e_p[1], i_e_p[2])
    List_of_contracts = map(fmap_contracts, parameters)
    
   


    Portfolio = cp.CreditPortfolio()
    # Portfolio.add_contract_list(List_of_contracts)
    print(Portfolio)
        
    