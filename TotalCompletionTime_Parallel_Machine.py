import gurobipy as gp 
import random
import time

def TCTParallelMachines(p,m,n):
    timer=time.time()
    
    model=gp.Model()

    #decision variables (see lecture)
    x=model.addVars(m,n,n,vtype=gp.GRB.BINARY,name="x")
    I=range(m)
    J=range(n)

    #Objective function
    model.setObjective(gp.quicksum(k*p[j]*x[i,k,j] for i in I for k in J for j in J), gp.GRB.MINIMIZE)  #objective function: minimize total completion time

    #Setting constraints
    model.addConstrs(gp.quicksum(x[i,k,j] for i in I for k in J)==1 for j in J)                         #Each job has exactly one position on one machine
    model.addConstrs(gp.quicksum(x[i,k,j] for j in J)<=1 for i in I for k in J)                         #Each position on each machine can have at most one job


    #Settings for solving the model
    model.setParam(gp.GRB.Param.Threads, 4)
    model.optimize()

    #reading the solution
    solValue=model.getAttr(gp.GRB.Attr.ObjVal)
    xvalues=[[[x[i,k,j].X for j in J] for k in J] for i in I]
    return xvalues, solValue, time.time()-timer



#given parameter values
numberOfJobs=5
numberOfMachines=2
processingTimes=[random.randint(1,200) for i in range(numberOfJobs)]

decisions, objectiveValue, solutionTime=TCTParallelMachines(processingTimes,numberOfMachines,numberOfJobs)    #Using a solver to get the minimal total completion time for the parallel machine environment

#Output of the solutions
print("Solution of the problem:", decisions," with the total completion time,",objectiveValue,". It took",solutionTime,"seconds to solve the model.")
print("We get the following solution:")
for j in range(numberOfJobs):
    for k in range(numberOfJobs):
        for i in range(numberOfMachines):
            if decisions[i][k][j]==1:
                print("Job",j,"is processed on machine", i,"in position", k,".")
print("The total completion time is", objectiveValue,"and it took",solutionTime,"seconds to solve the model.")