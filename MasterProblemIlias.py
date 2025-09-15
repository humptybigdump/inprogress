import gurobipy as gp           #Import Gurobi
import math

m=4                        #Number of item types
b=[30,50,30,70]            #Demands
I=range(m)

#input patterns, parameter a in the model of the lecture
patterns=[[3,0,0,0],[0,3,0,0],[0,0,2,0],[0,0,0,4]]
P=range(len(patterns))

#Master model
master=gp.Model()

#decision variable x of the master model
xm=master.addVars(len(P),vtype=gp.GRB.CONTINUOUS,name="x")

#objective: minimize number of used stocks
master.setObjective(gp.quicksum(xm[p] for p in P), gp.GRB.MINIMIZE)

#constraint: each demand is fulfilled (knapsack constraint)
master.addConstrs((gp.quicksum(patterns[p][i]*xm[p] for p in P)>=b[i] for i in I), name="c")

master.optimize()

#output objective function value and solution in terminal
master.printAttr(gp.GRB.Attr.ObjVal)
master.printAttr(gp.GRB.Attr.X)

#obtain shadow prices
shaddow=[float('nan') for i in I]
for i in I:
    constr = master.getConstrByName("c["+str(i)+"]")
    shaddow[i]=constr.Pi

#Print shadow prices
print("v=",shaddow)