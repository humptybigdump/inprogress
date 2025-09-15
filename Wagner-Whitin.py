import gurobipy as gp 
import random
import time

def wagnerWhitinAlgorithm(A,c,h,N,D):
    timer=time.time()
    F=[0]           #f_k, first value is f_0
    f=[[] for i in range(N)]
    for k in range(N):
        for t in range(k+1):
            f[k].append(F[t]+A+h*sum(D[j]*(j-t) for j in range(t+1,k+1))+c*sum(D[j] for j in range(t,k+1))) #calculation of f_k,t first value is f_1,1, as F starts with f_0, t is not subtracted by one
        F.append(min(f[k]))                         #calculation of f_k
    k=N-1
    x=[0 for i in range(N)]
    while(k>-1):                                    #determine production values via backwards induction
        t=f[k].index(min(f[k]))
        x[t]=sum(D[j] for j in range(t,k+1))
        k=t-1
    return x, F[-1], time.time()-timer                                  #Output of the solution, F[-1] are the optimal costs

def wagnerWhitinModel(A,c,h,N,D):
    timer=time.time()
    M=sum(D)                                        #Calculation of Big M (total demand over all periods)

    model=gp.Model()

    #decision variables (see lecture)
    x=model.addVars(N+1,vtype=gp.GRB.CONTINUOUS,lb=0,name="x")
    I=model.addVars(N+1,vtype=gp.GRB.CONTINUOUS,lb=0,name="I")
    y=model.addVars(N+1,vtype=gp.GRB.BINARY,name="y")

    #Objective function
    model.setObjective(gp.quicksum(A*y[t]+c*x[t]+h*I[t] for t in range(1,N+1)), gp.GRB.MINIMIZE)

    #Setting constraints
    model.addConstrs(I[t]==I[t-1]+x[t]-D[t-1] for t in range(1,N+1))            #inventory balance, as indexing starts with 0, we take D[t-1] as the relevant decision variables range from 1 to N
    model.addConstr(I[0]==0)
    model.addConstr(I[N]==0)
    model.addConstr(x[0]==0)
    model.addConstr(y[0]==0)
    model.addConstrs(x[t]<=M*y[t] for t in range(1,N+1))


    #Settings for solving the model
    model.setParam(gp.GRB.Param.Threads, 4)
    model.optimize()

    #reading the solution
    solValue=model.getAttr(gp.GRB.Attr.ObjVal)
    xvalues=[x[t].X for t in range(1,N+1)]
    return xvalues, solValue, time.time()-timer

def silverMeal(A,c,h,N,D):
    timer=time.time()
    x=[0 for i in range(N)]
    x[0]=D[0]
    tOld=0
    for t in range(1,N):
        H=h*sum(D[j]*(j-tOld) for j in range(tOld+1,t+1))               #Calculating the relevant H
        S=max(H-A,0)
        if S>0:                                                         #Should something be ordered in this period or in tOld
            x[t]=D[t]
            tOld=t
        else:
            x[tOld]=x[tOld]+D[t]
    orderPlacingCosts=0
    unitCosts=0
    holdingCosts=0
    for i in range(N):                                                  #Calculating the costs of the solution
        if x[i]>0:
            orderPlacingCosts=orderPlacingCosts+A
            tOld=i
        unitCosts=unitCosts+x[i]*c
        holdingCosts=holdingCosts+D[i]*h*(i-tOld)
    totalCosts=holdingCosts+unitCosts+orderPlacingCosts
    return x, totalCosts, time.time()-timer


#given parameter values
unitProductionCosts=20
inventoryHoldingCosts=0.4
setUpCosts=54
demands=[20,69,32,130,154,129]
demands=[random.randint(1,200) for i in range(100)]
numberOfPeriods=len(demands)

productionValuesWA, totalCostsWA, timeWA=wagnerWhitinAlgorithm(setUpCosts,unitProductionCosts,inventoryHoldingCosts,numberOfPeriods,demands)    #Using the Wagner Whitin Algorithm to determine a solution
productionValuesWM, totalCostsWM, timeWM=wagnerWhitinModel(setUpCosts,unitProductionCosts,inventoryHoldingCosts,numberOfPeriods,demands)        #Using a solver, i.e., Gurobi, to solve the Wagner Whitin Model to determine a solution
productionValuesSH, totalCostsSH, timeSH=silverMeal(setUpCosts,unitProductionCosts,inventoryHoldingCosts,numberOfPeriods,demands)               #Using the Silver Meal Heuristic to determine a solution

#Output of the solutions
print("Solution of the Wagner Whitin Algorithm:", productionValuesWA,".")
print("Solution of the Wagner Whitin Model:", productionValuesWM,".")
print("Solution of the Silver Meal Heuristic:", productionValuesSH,".")
print("Costs of the solution of the Wagner Whitin Algorithm:",totalCostsWA," (time:", timeWA,"). Costs of the solution of the Wagner Whitin Model:", totalCostsWM," (time:", timeWM,"). Costs of the solution of the Silver Meal Heuristic:", totalCostsSH," (time:", timeSH,").")


