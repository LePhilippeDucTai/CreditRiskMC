import timeit

def timing_it(f, n_reps) :
    s = timeit.timeit(f, number = n_reps)
    print(f'Execution for {n_reps} repetitions : {s * 1E3 : .3f}ms  which is {s : .3f}s.')
