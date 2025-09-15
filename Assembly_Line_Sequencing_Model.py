import gurobipy as gp 
import random
import time
import math

def lineSequencing(K,M,I,c,d,l,tau):
    timer=time.time()
    
    model=gp.Model()
    #decision variables (see lecture) plus fictitious sink
    x=model.addVars(M,I,vtype=gp.GRB.BINARY,name="x")
    s=model.addVars(K,I+1,vtype=gp.GRB.CONTINUOUS,lb=0,name="s")
    w=model.addVars(K,I,vtype=gp.GRB.CONTINUOUS,lb=0,name="w")

    #Objective function
    model.setObjective(gp.quicksum(w[k,i] for k in range(K) for i in range(I)), gp.GRB.MINIMIZE)  #objective function: minimize work overload

    #Setting constraints
    #each requisite unit is assigned to one position
    model.addConstrs(gp.quicksum(x[m,i] for m in range(M))==1 for i in range(I))
    model.addConstrs(gp.quicksum(x[m,i] for i in range(I))==d[m] for m in range(M))

    #processing of a unit cannot start before the preceding unit has been completed
    model.addConstrs(s[k,i+1]>=s[k,i]+gp.quicksum(tau[m][k]*x[m,i] for m in range(M)) -w[k,i]-c for i in range(I) for k in range(K))

    #work is restricted to the respective station area
    model.addConstrs(s[k,i]+gp.quicksum(tau[m][k]*x[m,i] for m in range(M)) -w[k,i]<=l[k] for i in range(I) for k in range(K))

    #starting position at each station at the begin and the end of the planning horizon
    model.addConstrs(s[k,0]==0 for k in range(K))
    model.addConstrs(s[k,I]==0 for k in range(K))

    #Settings for solving the model
    model.setParam(gp.GRB.Param.Threads, 4)
    model.optimize()
    #reading the solution
    solValue=model.getAttr(gp.GRB.Attr.ObjVal)
    xvalues=[[x[m,i].X for i in range(I)] for m in range(M)]
    svalues=[[s[k,i].X for i in range(I)] for k in range(K)]
    wvalues=[[w[k,i].X for i in range(I)] for k in range(K)]
    return xvalues, svalues, wvalues, solValue, time.time()-timer


#given parameter values
numberOfModels=7
numberOfStations=10
demands=[random.randint(1,20) for m in range(numberOfModels)]
processingTimes=[[random.randint(1,15) for k in range(numberOfStations)] for m in range(numberOfModels)]
lengthsOfStations=[random.randint(max(processingTimes[m][k] for m in range(numberOfModels)),max(processingTimes[m][k] for m in range(numberOfModels))+4) for k in range(numberOfStations)]
launchInterval=random.randint(min(lengthsOfStations)-3,min(lengthsOfStations))
lengthOfSequence=sum(demands)


#example exercise 20
numberOfModels=3
numberOfStations=4
demands=[2,2,1]
processingTimes=[[10,7,10,6],[8,10,9,8],[9,8,7,10]]
lengthsOfStations=[10,10,10,10]
launchInterval=9
lengthOfSequence=sum(demands)


xDecisions, sDecisions, wDecisions, workOverload, solutionTime=lineSequencing(numberOfStations, numberOfModels, lengthOfSequence,launchInterval,demands,lengthsOfStations,processingTimes)    #Line Sequencing model for minimizing work overload

sequence=[]
for i in range(lengthOfSequence):
    for j in range(numberOfModels):
        if xDecisions[j][i]==1:
            sequence.append(j+1)



#Output of the solutions
print("Minimum work overload for the problem:",workOverload,". It took",solutionTime,"seconds to solve the model.")
print("We get the following model sequence:",sequence,".")