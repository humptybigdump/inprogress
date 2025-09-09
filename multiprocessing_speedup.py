##multiprocessing_speedup.py
import time
import multiprocessing
import matplotlib.pyplot as plt
from pubchem_functions import molecular_weight, smiles, hydrogen_bond_donors, hydrogen_bond_acceptors, fetch_data

def process_analysis(args):
    """
    Worker function that repeatedly calls analysis functions.
    :param args: Tuple (data, iterations) to run the functions.
    """
    data, iterations = args
    for _ in range(iterations):
        molecular_weight(data)
        smiles(data)
        hydrogen_bond_donors(data)
        hydrogen_bond_acceptors(data)
    return True

def measure_speedup(data, total_iterations, processes_list):
    """
    Measures execution time for running analysis repeatedly using different numbers of processes.
    :param url: URL to fetch the compound data.
    :param total_iterations: Total number of iterations for the workload.
    :param processes_list: List of process counts to test.
    :return: Tuple (processes_list, times) where times is a list of execution times.
    """

    times = []
    for p in processes_list:
        start = time.perf_counter()
        pool = multiprocessing.Pool(processes=p)
        iterations_per_process = total_iterations // p
        tasks = [(data, iterations_per_process) for _ in range(p)]
        pool.map(process_analysis, tasks)
        pool.close()
        pool.join() # wait for all 
        end = time.perf_counter()
        times.append(end - start)
    return processes_list, times

def plot_speedup(processes, times):
    """
    Plots speedup results.
    :param processes: List of process counts.
    :param times: Corresponding execution times.
    """
    plt.figure()
    plt.plot(processes, times, marker='o')
    plt.xlabel("Number of Processes")
    plt.ylabel("Time Taken (seconds)")
    plt.title("Multiprocessing Speedup")
    plt.grid(True)
    plt.show()

