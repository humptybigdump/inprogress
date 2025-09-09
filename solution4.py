# Task 1: Generator function for Freundlich isotherm
def freundlich_isotherm(Kf, n, Cw_values):
    """Generator for Freundlich sorption isotherm."""
    for C_w in Cw_values:
        C_s = Kf * (C_w**(1/n)) 
        yield C_w, C_s  # Yield equilibrium concentration and sorbed amount

# Task 2: Simulate sorption for C_w from 0.1 to 50 mg/L
C_w_range = [round(x * 0.1, 1) for x in range(1, 501)]
sorption_generator = freundlich_isotherm(Kf=2.5, n=0.8, Cw_values=C_w_range)
for C_w, C_s in sorption_generator:
    print(f"Task2: C_w = {C_w:.2f} mg/L → C_s = {C_s:.2f} mg/kg")

# Need to recreate the generator because it's exhausted
sorption_generator = freundlich_isotherm(Kf=2.5, n=0.8, Cw_values=C_w_range)

# Task 3: Filter values where C_s > 10 mg/kg
filtered_sorption = ((C_w, C_s) for C_w, C_s in sorption_generator if C_s > 10)

# Task 4: Process generator on-the-fly
for C_w, C_s in filtered_sorption:
    print(f" Task4: C_w = {C_w:.2f} mg/L → C_s = {C_s:.2f} mg/kg")

