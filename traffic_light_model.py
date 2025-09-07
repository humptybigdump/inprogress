import simpy
import random
import matplotlib.pyplot as plt
import itertools
import numpy as np

class Intersection:
    def __init__(self, env, arrival_rate, green_duration, departure_interval):
        self.env = env
        self.NS_green = True  # Start with North-South green
        self.EW_green = False  # East-West red
        self.N_queue = simpy.Store(env)
        self.S_queue = simpy.Store(env)
        self.E_queue = simpy.Store(env)
        self.W_queue = simpy.Store(env)
        self.arrival_rate = arrival_rate
        self.green_duration = green_duration
        self.departure_interval = departure_interval
        self.history = [(0., 0, 0, 0, 0)] # N, S, E, W
        self.switched = [0, 0, 0, 0]
        self.waiting_times = []
        
    def traffic_control(self):
        """Toggle traffic lights between NS and EW."""
        while True:
            self.NS_green = not self.NS_green
            self.EW_green = not self.EW_green
            self.switched = [1, 1, 1, 1]
            yield self.env.timeout(self.green_duration)  # Switch lights every GREEN_DURATION seconds

    def car_arrival(self, direction):
        """Simulate car arrivals at the intersection using a Poisson process."""        
        while True:
            yield self.env.timeout(random.expovariate(1 / self.arrival_rate))
            if direction == 'N':
                if len(self.N_queue.items) == 0 and self.NS_green:
                    self.waiting_times.append((0))
                else:
                    yield self.N_queue.put(self.env.now)
            elif direction == 'S':                                 
                if len(self.S_queue.items) == 0 and self.NS_green:
                    self.waiting_times.append((0))
                else:
                    yield self.S_queue.put(self.env.now)
            elif direction == 'E':                                 
                if len(self.E_queue.items) == 0 and self.EW_green:
                    self.waiting_times.append((0))
                else:
                    yield self.E_queue.put(self.env.now)
            elif direction == 'W':                                 
                if len(self.W_queue.items) == 0 and self.EW_green:
                    self.waiting_times.append((0))
                else:
                    yield self.W_queue.put(self.env.now)
            else:  
                print("Unknown direction ... {direction}")
            self.history.append((self.env.now, len(self.N_queue.items), len(self.S_queue.items), len(self.E_queue.items), len(self.W_queue.items)))

    def car_departure(self, direction):
        """Allow cars to depart when the light is green."""
        while True:            
            if (direction == 'N' and self.NS_green and len(self.N_queue.items) > 0):                            
                if self.switched[0] > 0:
                    self.switched[0] = 0
                    yield self.env.timeout(self.departure_interval)
                else:
                    entrance_time = yield self.N_queue.get()
                    self.waiting_times.append((self.env.now - entrance_time))                
                    yield self.env.timeout(self.departure_interval)  # Time for a car to pass the intersection                
            elif (direction == 'S' and self.NS_green and len(self.S_queue.items) > 0):
                if self.switched[1] > 0:
                    self.switched[1] = 0
                    yield self.env.timeout(self.departure_interval)
                else:
                    entrance_time = yield self.S_queue.get()
                    self.waiting_times.append((self.env.now - entrance_time))
                    yield self.env.timeout(self.departure_interval)  # Time for a car to pass the intersection                
            elif (direction == 'E' and self.EW_green and len(self.E_queue.items) > 0):
                if self.switched[2] > 0:
                    self.switched[2] = 0
                    yield self.env.timeout(self.departure_interval)
                else:
                    entrance_time = yield self.E_queue.get()
                    self.waiting_times.append((self.env.now - entrance_time))
                    yield self.env.timeout(self.departure_interval)  # Time for a car to pass the intersection                
            elif (direction == 'W' and self.EW_green and len(self.W_queue.items) > 0):
                if self.switched[3] > 0:
                    self.switched[3] = 0
                    yield self.env.timeout(self.departure_interval)
                else:
                    entrance_time = yield self.W_queue.get()
                    self.waiting_times.append((self.env.now - entrance_time))
                    yield self.env.timeout(self.departure_interval)  # Time for a car to pass the intersection                
            else:                
                yield self.env.timeout(1)  # Check again in 1 second
        self.history.append((self.env.now, len(self.N_queue.items), len(self.S_queue.items), len(self.E_queue.items), len(self.W_queue.items)))

def step_graph(intersection):
    """ Displays a step line chart of inventory level """
    # create subplot
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.grid(which = 'major', alpha = .4)    
    # plot simulation data
    x_val = [x[0] for x in intersection.history]
    n_val = [x[1] for x in intersection.history]
    s_val = [x[2] for x in intersection.history]
    e_val = [x[3] for x in intersection.history]
    w_val = [x[4] for x in intersection.history]
    plt.step(x_val, n_val, where = 'post', label='North')    
    plt.step(x_val, s_val, where = 'post', label='South')   
    plt.step(x_val, e_val, where = 'post', label='East')   
    plt.step(x_val, w_val, where = 'post', label='West')   
    # titles and legends
    plt.xlabel('Seconds')
    plt.ylabel('Cars in queue')
    plt.title(f'Simulation output for system with (Arrival, Green Duration, Departure) = {intersection.arrival_rate}, {intersection.green_duration}, {intersection.departure_interval}')
    plt.gca().legend()
    #plt.savefig(f'Step_graph_{inventory.reorder_point}.{inventory.order_size}.png')
    plt.show()  

def max_queue_length(intersection):
    n_val = [x[1] for x in intersection.history]
    max_val = max(n_val)
    s_val = [x[2] for x in intersection.history]
    s_val.append((max_val))
    max_val = max(s_val)
    e_val = [x[3] for x in intersection.history]
    e_val.append((max_val))
    max_val = max(e_val)
    w_val = [x[4] for x in intersection.history]
    w_val.append((max_val))
    max_val = max(w_val)

    return max_val

def max_waiting_time(intersection):
    return max(intersection.waiting_times)

def mean_waiting_time(intersection):
    return np.average(intersection.waiting_times)
    #return min([, 100])    

def run(arrival_rate, green_duration, departure_interval, sim_length = 500):
    # Create the SimPy environment
    env = simpy.Environment()
    intersection = Intersection(env, arrival_rate, green_duration, departure_interval)

    # Start the processes
    env.process(intersection.traffic_control())
    for direction in ['N', 'S', 'E', 'W']:
        env.process(intersection.car_arrival(direction))
        env.process(intersection.car_departure(direction))

    # Run the simulation
    env.run(until=sim_length)

    return intersection

def run_experiments(arrival_rates, green_duration, num_rep, run_length, objective):
    """ Runs inventory simulation with every combination of reorder points and
    order sizes, and assembles results in a list of dictionaries
    
    Args:
        - reorder_points: list of reorder points parameters to simulate 
        - order_sizes:list of order size parameters to simulate
        - num_rep: number of replications to run for each design point 
    """   
    # validate user inputs:   
    if num_rep <=0:
        raise ValueError('Number of replications must be greater than zero') 
    # initiate variables
    len1 = len(arrival_rates)
    len2 = len(green_duration)
    iter_count = 0
    results = [] 
    # iterate over all design points
    for g in green_duration:
        temp = []
        print(f'Green duration {g}')
        for a in arrival_rates:
            for k in range(num_rep):
                temp.append((objective(run(a, g, 2, run_length))))
        results.append((g, np.average(temp)))
    
    return results

# run simulation
if __name__ == '__main__':
    intersection = run(5, 30, 2, 2000)
    print(max_queue_length(intersection))
    print(mean_waiting_time(intersection))