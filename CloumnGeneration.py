import gurobipy as gp           #Import Gurobi
import math

#Master model
def masterModel(a):

    P=range(len(a))

    master=gp.Model()

    #decision variable x of the master model
    xm=master.addVars(len(P),vtype=gp.GRB.CONTINUOUS,name="x")

    #objective: minimize number of used stocks
    master.setObjective(gp.quicksum(xm[p] for p in P), gp.GRB.MINIMIZE)

    #constraint: each demand is fulfilled (knapsack constraint)
    master.addConstrs((gp.quicksum(a[p][i]*xm[p] for p in P)>=b[i] for i in I), name="c")

    master.optimize()

    #obtain shadow prices
    shaddow=[float('nan') for i in I]
    for i in I:
        constr = master.getConstrByName("c["+str(i)+"]")
        shaddow[i]=constr.Pi

    solValue=master.getAttr(gp.GRB.Attr.ObjVal)                             #Get objective function value of the found solution
    solution=master.getAttr(gp.GRB.Attr.X)                                  #Get optimal solution
    print("Master solution:", solValue, solution,"with shadow prices:", shaddow)
    return shaddow, solValue, solution

#Pricing Model
def priceModel(v):

    price=gp.Model()

    #Definition of decision variable a in pricing problem
    ap=price.addVars(m,vtype=gp.GRB.INTEGER,name="a")

    #objective: minimize reduced costs
    price.setObjective(1-gp.quicksum(v[i]*ap[i] for i in I), gp.GRB.MINIMIZE)

    #constraint: the pattern may not exceed the width of the stock
    price.addConstr(gp.quicksum(ap[i]*w[i] for i in I)<=W)

    price.optimize()

    #get reduced costs as value of the objective function and obtain new pattern
    reducedCosts=price.getAttr(gp.GRB.Attr.ObjVal)              
    newPattern=[ap[i].X for i in I]
    print("Pricing solution:", reducedCosts,newPattern)
    return reducedCosts, newPattern

m=4                         #Number of item types
b=[30,50,30,70]             #Demands
w=[25,25,35,20]             #Widths
W=85                        #Width of one stock
I=range(m)

#Generate basic patterns (basic patterns from exercise 22)
PatternList=range(m)
patterns=[[float('nan') for i in I] for j in PatternList]
for i in I:
    for p in PatternList:
        if (p==i):
            patterns[i][p]=math.floor(W/w[i])
        else:
            patterns[i][p]=0

#set reduced costs to -1 to start while loop
redCosts=-1

#while there are reduced costs
while(redCosts<0):
    #solve master problem to obtain best solution with given patterns
    dualVariables, objValue, sol=masterModel(patterns)
    #solve pricing problem to obtain new pattern
    redCosts, PatternToAdd = priceModel(dualVariables)

    #add new pattern if reduced costs are negative
    if (redCosts<0):
        patterns.append(PatternToAdd)

#print solution
print("Solution:",sol,"with Objective function value:", objValue)
print("The patterns are:")
for i in range(len(patterns)):
    if (sol[i]!=0):
        print(sol[i],"times pattern",patterns[i])
