import creditportfolio as cp
import gaussian_copula as gc
import timing as mytime

if __name__ == "__main__":
    rho = 0.2
    dim = 1
    Sig = gc.UniformCorrMatrix(rho, dim)
    X = gc.Gaussian_Vector_Simulation(dim, Sig)
    X.Simulate()
    mytime.timing_it(X.Simulate, 10000)
    
    ids = [104190 ,101044, 183410]
    exposures = [1000, 2000, 500]
    pds = [0.02, 0.03, 0.01]
    parameters = zip(ids, exposures, pds)
    fmap_contracts = lambda i_e_p : cp.CreditContract(i_e_p[0], i_e_p[1], i_e_p[2])
    List_of_contracts = map(fmap_contracts, parameters)
    
    

    # print(List_of_contracts)
    
    # Contract1 = mccr.CreditContract(104190, 1000, 0.02)
    # Contract2 = mccr.CreditContract(101044, 2000, 0.03)
    # Contract3 = mccr.CreditContract(183410, 500, 0.01)
    # Portfolio = mccr.CreditPortfolio()
    # List_of_contracts = [Contract1 , Contract2, Contract3]
    # Portfolio.add_contract_list(List_of_contracts)