from multiprocessing import Pool

# Define a function that does a lot of calculation...
def f(n: int) -> int:
    match n:
        case 0:
            return 0
        case 1 | 2:
            return 1
        case _:
            return f(n - 1) + f(n - 2)

# Now we can run the computation in parallel.
with Pool(4) as p: # Use four cores.
    # This call blocks until all processes are finished.
    result = p.map(f, [100, 110, 120, 130])

    # Show the result at the end.
    print(f"{result=}")
