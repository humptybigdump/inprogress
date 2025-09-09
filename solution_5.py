##main_PFOA.py
from pubchem_functions import run_analysis
from multiprocessing_speedup import measure_speedup, plot_speedup

def main():
    url = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/9554/json"
    
    # Run a single analysis
    results = run_analysis(url)
    print("Analysis Results:")
    print(results)
    
    # Run the multiprocessing speedup test
    processes = [1]
    total_iterations = 0
    procs, times = measure_speedup(url, total_iterations, processes)
    if times is not None:
        print("Multiprocessing speedup test results:")
        for p, t in zip(procs, times):
            print(f"Processes: {p}, Time taken: {t:.4f} seconds")
        plot_speedup(procs, times)

if __name__ == "__main__":
    
    main()

