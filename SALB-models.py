import gurobipy as gp 
import random
import time
import math

def SALB1(c,Kmax,t,n,SI,B,L,E,A):
    timer=time.time()
    
    model=gp.Model()
    J=range(n+1)
    #decision variables (see lecture) plus fictitious sink
    x=model.addVars(n+1,Kmax,vtype=gp.GRB.BINARY,name="x")

    #Objective function
    model.setObjective(gp.quicksum(k*x[n,k] for k in SI[n]), gp.GRB.MINIMIZE)  #objective function: minimize number of stations

    #Setting constraints
    model.addConstrs(gp.quicksum(x[j,k] for k in SI[j])==1 for j in J)                                    #Occurance constraints
    model.addConstrs(gp.quicksum(t[j]*x[j,k] for j in B[k])<=c for k in range(Kmax))                         #Cycle time constraints
    for i in A:
        if L[i[0]]>=E[i[1]]:
            model.addConstr(gp.quicksum(k*x[i[0],k] for k in SI[i[0]])<=gp.quicksum(k*x[i[1],k] for k in SI[i[1]]))     #Precedence constraints
    for i in range(n+1):
        for j in range(Kmax):
            if j not in SI[i]:
                model.addConstr(x[i,j]==0)


    #Settings for solving the model
    model.setParam(gp.GRB.Param.Threads, 4)
    model.optimize()
    #reading the solution
    solValue=model.getAttr(gp.GRB.Attr.ObjVal)+1
    xvalues=[[x[j,k].X for k in range(Kmax)] for j in range(n+1)]
    return xvalues, solValue, time.time()-timer

def SALB2(cmax,K,t,n,SI,B,L,E,A):
    timer=time.time()
    
    model=gp.Model()
    J=range(n+1)

    #decision variables (see lecture) plus fictitious sink
    x=model.addVars(n+1,K,vtype=gp.GRB.BINARY,name="x")
    c=model.addVar(vtype=gp.GRB.CONTINUOUS,lb=0,name="c")


    #Objective function
    model.setObjective(c, gp.GRB.MINIMIZE)  #objective function: minimize cycle time

    #Setting constraints
    model.addConstrs(gp.quicksum(x[j,k] for k in SI[j])==1 for j in J)                                    #Occurance constraints
    model.addConstrs(gp.quicksum(t[j]*x[j,k] for j in B[k])<=c for k in range(K))                         #Cycle time constraints
    for i in A:
        if L[i[0]]>=E[i[1]]:
            model.addConstr(gp.quicksum(k*x[i[0],k] for k in SI[i[0]])<=gp.quicksum(k*x[i[1],k] for k in SI[i[1]]))     #Precedence constraints
    for i in range(n+1):
        for j in range(K):
            if j not in SI[i]:
                model.addConstr(x[i,j]==0)


    #Settings for solving the model
    model.setParam(gp.GRB.Param.Threads, 4)
    model.optimize()

    #reading the solution
    solValue=model.getAttr(gp.GRB.Attr.ObjVal)
    xvalues=[[x[j,k].X for k in range(K)] for j in range(n+1)]
    return xvalues, solValue, time.time()-timer

def SALBE(cmin,cmax,Kmin,Kmax,t,n,SI,B,L,E,A):
    timer=time.time()
    
    model=gp.Model()
    J=range(n+1)

    #decision variables (see lecture) plus fictitious sink
    x=model.addVars(n+1,Kmax,vtype=gp.GRB.BINARY,name="x")
    c=model.addVar(vtype=gp.GRB.CONTINUOUS,lb=0,name="c")


    #Objective function
    model.setObjective(c*gp.quicksum((k+1)*x[n,k] for k in SI[n]), gp.GRB.MINIMIZE)  #objective function: minimize line efficiency

    #Setting constraints
    model.addConstrs(gp.quicksum(x[j,k] for k in SI[j])==1 for j in J)                                    #Occurance constraints
    model.addConstrs(gp.quicksum(t[j]*x[j,k] for j in B[k])<=c for k in range(Kmax))                         #Cycle time constraints
    for i in A:
        if L[i[0]]>=E[i[1]]:
            model.addConstr(gp.quicksum(k*x[i[0],k] for k in SI[i[0]])<=gp.quicksum(k*x[i[1],k] for k in SI[i[1]]))     #Precedence constraints
    for i in range(n+1):
        for j in range(Kmax):
            if j not in SI[i]:
                model.addConstr(x[i,j]==0)
    model.addConstr(c>=cmin)
    model.addConstr(c<=cmax)
    model.addConstr(gp.quicksum((k+1)*x[n,k] for k in SI[n])>=Kmin)
    model.addConstr(gp.quicksum((k+1)*x[n,k] for k in SI[n])<=Kmax)


    #Settings for solving the model
    model.setParam(gp.GRB.Param.Threads, 4)
    model.optimize()

    #reading the solution
    solValue=model.getAttr(gp.GRB.Attr.ObjVal)
    xvalues=[[x[j,k].X for k in range(Kmax)] for j in range(n+1)]
    return xvalues, solValue, time.time()-timer

def rankedPositionalWeight(c,t,n, R,P):
    timer=time.time()
    w=[]
    for j in range(n):
        w.append(t[j]+sum(t[h] for h in R[j]))
    V=list(range(n))
    Q=[[]]
    T=c
    while len(V)!=0:
        potentialTasks=[]
        for j in V:
            if len(P[j])==0 and t[j]<=T:
                potentialTasks.append((j,w[j]))                                                 #determine assignable tasks with their weight
        #if there are otential tasks: determine wk, decrease free processing time of the station and add wk to the station
        if len(potentialTasks)>0:
            maxW=max(potentialTasks, key=lambda k: k[1])[0]
            T=T-t[maxW]
            Q[-1].append(maxW)
            V.remove(maxW)
            for j in V:
                if maxW in P[j]:
                    P[j].remove(maxW)
        #if there are no potential tasks: open new station
        else:
            Q.append([])
            T=c
    numberStations=len(Q)
    return Q, numberStations, time.time()-timer


#given parameter values
numberOfJobs=7
maxCycleTime=72                                                #maximum cycle time: is not relevant for SALB2
maxNumberOfStations=numberOfJobs                               #maximum number of stations: numberOfJobs is default value, but it can be other values depending on the example
processingTimes=[random.randint(1,maxCycleTime) for i in range(numberOfJobs)]
processingTimes.append(0)
tsum=sum(processingTimes)
PrecedenceRelations=[]
immediatePredecessors=[[] for i in range(numberOfJobs)]
immediateSuccessors=[[] for i in range(numberOfJobs)]
allPredecessors=[[] for i in range(numberOfJobs)]
allSuccessors=[[] for i in range(numberOfJobs)]

#generating random predecessor relations
for i in range(1,numberOfJobs):
    a=random.expovariate(lambd=1/(i+1))                     #random variable for deciding if predecessor exists
    if (a>=1):
        nrPredecessors=min(math.floor(a),i)               #determine number of predecessors
        for j in range(nrPredecessors):
            possibleValues=[k for k in range(i) if k not in immediatePredecessors[i]]
            b=random.choice(possibleValues)
            immediatePredecessors[i].append(b)              #save predecessor relations
            PrecedenceRelations.append((b,i))
            immediateSuccessors[b].append(i)

#example exercise 17
numberOfJobs=7
processingTimes=[45,60,30,15,25,10,10]
processingTimes.append(0)
maxCycleTime=72                                                        #cycle time is given here
maxNumberOfStations=4                                                  #number of stations is given in example, default value is usually numberOfJobs except for SALB2
tsum=sum(processingTimes)
PrecedenceRelations=[(1,2),(0,4),(3,4),(2,5),(4,5),(5,6)]
immediatePredecessors=[[],[],[1],[],[0,3],[2,4],[5]]
immediateSuccessors=[[4],[2],[5],[4],[5],[6],[]]
allPredecessors=[[] for i in range(numberOfJobs)]
allSuccessors=[[] for i in range(numberOfJobs)]

#determine sets of immediate and transitive predecessors and successors
for i in range(numberOfJobs):
    for j in immediatePredecessors[i]:
        allPredecessors[i].append(j)
        allSuccessors[j].append(i)
        for k in allPredecessors[j]:
            allPredecessors[i].append(k)
            allSuccessors[k].append(i)
for i in range(numberOfJobs):
    allPredecessors[i]=list(set(allPredecessors[i]))
    allPredecessors[i].sort()
    allSuccessors[i]=list(set(allSuccessors[i]))
    allSuccessors[i].sort()

#determine predecessors (and successors) of sink
allSuccessors.append([])
immediateSuccessors.append([])
allPredecessors.append([i for i in range(numberOfJobs)])
immediatePredecessors.append([])
for i in range(numberOfJobs):
    if len(immediateSuccessors[i])==0:
        immediatePredecessors[numberOfJobs].append(i)
        immediateSuccessors[i].append(numberOfJobs)
        PrecedenceRelations.append((i,numberOfJobs))

#determine earliest and latest stations
earliest=[math.ceil((processingTimes[j]+sum(processingTimes[h] for h in allPredecessors[j]))/maxCycleTime)-1 for j in range(numberOfJobs+1)]
latest=[maxNumberOfStations+1-math.ceil((processingTimes[j]+sum(processingTimes[h] for h in allSuccessors[j]))/maxCycleTime)-1 for j in range(numberOfJobs)]
latest.append(maxNumberOfStations-1)                                                                                                                           #latest station of sink is Kmax
stationInterval=[[i for i in range(earliest[j],latest[j]+1)] for j in range(numberOfJobs+1)]
jobsAssignableToStation=[[] for i in range(maxNumberOfStations)]
for k in range(maxNumberOfStations):
    for j in range(numberOfJobs+1):
        if k in stationInterval[j]:
            jobsAssignableToStation[k].append(j)

if (tsum>maxNumberOfStations*maxCycleTime):
    print("The problem is infeasible")
    exit()

decisionsSALB1, objectiveValueSALB1, solutionTimeSALB1=SALB1(maxCycleTime,maxNumberOfStations,processingTimes,numberOfJobs,stationInterval,jobsAssignableToStation,latest,earliest,PrecedenceRelations)    #SALB1 model for obtaining minimum number of stations
decisionsSALB2, objectiveValueSALB2, solutionTimeSALB2=SALB2(maxCycleTime,maxNumberOfStations,processingTimes,numberOfJobs,stationInterval,jobsAssignableToStation,latest,earliest,PrecedenceRelations)    #SALB2 model for obtaining minimum cycle time
decisionsSALBE, objectiveValueSALBE, solutionTimeSALBE=SALBE(tsum/maxNumberOfStations,maxCycleTime,tsum/maxCycleTime,maxNumberOfStations,processingTimes,numberOfJobs,stationInterval,jobsAssignableToStation,latest,earliest,PrecedenceRelations)    #SALBE model for obtaining maximum efficiency
decisionsRPW, objectiveValueRPW, solutionTimeRPW=rankedPositionalWeight(maxCycleTime, processingTimes,numberOfJobs,allSuccessors,immediatePredecessors)

#Output of the solutions
print("Solution of the problem SALB1 has a minimum number of stations:",objectiveValueSALB1,". It took",solutionTimeSALB1,"seconds to solve the model.")
print("We get the following solution:")
for j in range(numberOfJobs):
    for k in range(maxNumberOfStations):
        if decisionsSALB1[j][k]==1:
                print("Task",j,"is processed on Station", k,".")

print("Solution of the problem solved by the Ranked Positional Weight heuristic has a minimum number of stations:",objectiveValueRPW,". It took",solutionTimeRPW,"seconds to solve the model.")
print("We get the following solution:")
for j in range(numberOfJobs):
    for k in range(objectiveValueRPW):
        if j in decisionsRPW[k]:
            print("Task",j,"is processed on Station", k,".")

print("Solution of the problem SALB2 has a minimum cycle time:",objectiveValueSALB2,". It took",solutionTimeSALB2,"seconds to solve the model.")
print("We get the following solution:")
for j in range(numberOfJobs):
    for k in range(maxNumberOfStations):
        if decisionsSALB2[j][k]==1:
                print("Task",j,"is processed on Station", k,".")

print("Solution of the problem SALBE has a maximum efficiency of:",tsum/objectiveValueSALBE,". It took",solutionTimeSALBE,"seconds to solve the model.")
print("We get the following solution:")
for j in range(numberOfJobs):
    for k in range(maxNumberOfStations):
        if decisionsSALBE[j][k]==1:
                print("Task",j,"is processed on Station", k,".")