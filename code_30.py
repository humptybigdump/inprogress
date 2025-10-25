from joblib import Parallel, delayed

# Define a function that does a lot of calculation...
def f(n: int) -> int:
    match n:
        case 0:
            return 0
        case 1 | 2:
            return 1
        case _:
            return f(n - 1) + f(n - 2)

with Parallel(n_jobs=4) as parallel: # Again use four cores.
    # Start jobs in parallel.
    result = parallel(delayed(f)(n) for n in [100, 110, 120, 130])

    # Print the result at the end.
    print(f"{result=}")
