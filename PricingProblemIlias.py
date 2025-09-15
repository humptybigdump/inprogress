import gurobipy as gp           #Import Gurobi
import math

m=4                         #Number of item types
w=[25,25,35,20]             #Widths
W=85                        #Width of one stock
I=range(m)

#Input of shadow prices
v= [0.3333333333333333, 0.3333333333333333, 0.5, 0.25]

#Pricing model
price=gp.Model()

#Definition of decision variable a in pricing problem
ap=price.addVars(m,vtype=gp.GRB.INTEGER,name="a")

#objective: minimize reduced costs
price.setObjective(1-gp.quicksum(v[i]*ap[i] for i in I), gp.GRB.MINIMIZE)

#constraint: the pattern may not exceed the width of the stock
price.addConstr(gp.quicksum(ap[i]*w[i] for i in I)<=W)

price.optimize()

#output objective function value and solution in terminal
price.printAttr(gp.GRB.Attr.ObjVal)

#get new pattern
newPattern=[ap[i].X for i in I]

#print new pattern
print(newPattern)