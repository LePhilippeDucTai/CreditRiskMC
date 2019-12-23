import timeit
import time
import attotime
def timing_it(f, n_reps) :
    s = timeit.timeit(f, number = n_reps)
    print(f'Execution for {n_reps} repetitions : {s * 1E3 : .3f}ms  which is {s : .3f}s.')

def time_it(func) :
    def wrapper(*args, **kwargs):
        print(f'\n### Entering in {func.__name__}. ###')
        t1 = time.perf_counter()
        s = func(*args, **kwargs)
        t2 = time.perf_counter()
        elapsed = t2 - t1
        print(f'### Quitting function {func.__name__}. ###')
        print(f'### Elapsed time : {elapsed : .10f} seconds. ### \n')
        return(s)
    return(wrapper)

@time_it
def adder(x,y, dict):
    for key, value in dict.items():
        print(key + ' -> ' + str(value))

