import gurobipy as gp 
import random
import time

def MakespanJobShop(p,machineOrder,m,n):
    timer=time.time()
    
    model=gp.Model()

    M=sum(sum(i) for i in p)            #calculate big M

    #decision variables (see lecture)
    b=model.addVars(m,n,n,vtype=gp.GRB.BINARY,name="b")
    y=model.addVars(m,n,vtype=gp.GRB.CONTINUOUS,lb=0,name="y")
    Cmax=model.addVar(vtype=gp.GRB.CONTINUOUS,lb=0,name="Cmax")
    I=range(m)
    J=range(n)

    #Objective function
    model.setObjective(Cmax, gp.GRB.MINIMIZE)  #objective function: minimize makespan

    #Setting constraints
    for j in J:
        for i in range(m-1):
            model.addConstr(y[machineOrder[j][i+1],j]-y[machineOrder[j][i],j]>=p[machineOrder[j][i]][j])
    model.addConstrs(Cmax-y[i,j]>=p[i][j] for i in I for j in J)
    model.addConstrs(y[i,j]+p[i][j]-M*(1-b[i,j,l])<=y[i,l] for i in I for j in J for l in J if l != j)
    model.addConstrs(y[i,l]+p[i][l]-M*b[i,j,l]<=y[i,j] for i in I for j in J for l in J if l != j)


    #Settings for solving the model
    model.setParam(gp.GRB.Param.Threads, 4)
    model.optimize()

    #reading the solution
    solValue=model.getAttr(gp.GRB.Attr.ObjVal)
    bvalues=[[[[b[i,j,l].X for l in J] for i in I] for j in J] for i in I]
    yvalues=[[y[i,j].X for j in J] for i in I]
    return bvalues, yvalues, solValue, time.time()-timer

def MostWorkRemainingHeuristic(p,machineOrder,m,n):
    timer=time.time()
    numberUnscheduledJobs=sum(len(machineOrder[j]) for j in range(n))           #determine the number of unscheduled jobs
    machineSchedule=[[] for i in range(m)]                                      #create empty schedule for each machine
    machineOrderCopy=[machineOrder[j].copy() for j in range(n)]                 #make a copy of the machine sequences of the jobs 
    while numberUnscheduledJobs>0:
        #Step 1: Define the set of schedulable operations J
        J=[]
        for j in range(n):
            if len(machineOrderCopy[j])==0:
                J.append(float('nan'))
            else:
                J.append(machineOrderCopy[j][0])
        #Step 2: Compute for each job j the sum of its remaining processing times Tj
        T=[]
        for j in range(n):
            if J[j]==float('nan'):
                T.append(0)
            else:
                T.append(sum(p[i][j] for i in machineOrderCopy[j]))
        #Step 3: Schedule the job with the highest remaining processing time
        nextJob=T.index(max(T))
        machineToSchedule=machineOrderCopy[nextJob][0]
        machineSchedule[machineToSchedule].append(nextJob)
        machineOrderCopy[nextJob].pop(0)
        #Step 4: preparation for next iteration
        numberUnscheduledJobs=sum(len(machineOrderCopy[j]) for j in range(n))
    #Determine makespan of the schedule
    numberUncompletedJobs=sum(len(machineSchedule[i]) for i in range(m))
    currentCompletionTimesMachines=[0 for i in range(m)]
    currentCompletionTimesJobs=[0 for i in range(n)]
    while numberUncompletedJobs>0:
        for i in range(m):
            if len(machineSchedule[i])>0:
                firstJob=machineSchedule[i][0]
                if i==machineOrder[firstJob][0]:
                    currentCompletionTimesMachines[i]=max(currentCompletionTimesMachines[i],currentCompletionTimesJobs[firstJob])+p[i][firstJob]
                    currentCompletionTimesJobs[firstJob]=currentCompletionTimesMachines[i]
                    machineOrder[firstJob].remove(i)
                    machineSchedule[i].remove(firstJob)
        numberUncompletedJobs=sum(len(machineSchedule[i]) for i in range(m))
    return max(currentCompletionTimesJobs), time.time()-timer



#given parameter values
numberOfJobs=10
numberOfMachines=5
processingTimes=[[random.randint(1,50) for j in range(numberOfJobs)] for i in range(numberOfMachines)]
machineSequenceOfJobs=[list(range(numberOfMachines)) for j in range(numberOfJobs)]
for j in range(numberOfJobs):
    random.shuffle(machineSequenceOfJobs[j])
#processingTimes=[[5,1],[2,5],[2,7],[4,1]]
#machineSequenceOfJobs=[[0,1,2,3],[0,2,1,3]]

sequenceDecissionModell, startingTimesModell, makespanModell, solutionTimeModell=MakespanJobShop(processingTimes, machineSequenceOfJobs, numberOfMachines,numberOfJobs)    #Using a solver to get the minimal makespan for the job shop machine environment
makespanMostWorkRemaining, solutionTimeMostWorkremaining = MostWorkRemainingHeuristic(processingTimes,machineSequenceOfJobs, numberOfMachines, numberOfJobs)

#Output of the solutions
print("The makespan obtained by solving the modell with a solver is", makespanModell,"and it took",solutionTimeModell,"seconds to solve the model.")
print("The makespan obtained by using the MostWorkRemaining heuristic is", makespanMostWorkRemaining,"and it took",solutionTimeMostWorkremaining,"seconds to compute the solution.")
