import gurobipy as gp
import math

#Solving the master model (see lecture), the pattern variable is slightly adjusted to a_pi instead of a_ip, as a is a list of patterns
# Furthermore, the Upper and Lower Bounds from the Branch and Price are included
def masterModel(a,LBs,UBs):

    P=range(len(a))

    master=gp.Model()

    xm=master.addVars(len(P),vtype=gp.GRB.CONTINUOUS,name="x")

    master.setObjective(gp.quicksum(xm[p] for p in P), gp.GRB.MINIMIZE)

    master.addConstrs((gp.quicksum(a[p][i]*xm[p] for p in P)>=b[i] for i in I), name="c")

    #if applicable, Upper and Lower Bounds are set based on previous branching
    if len(LBs)>0:
        for i in LBs:
            master.addConstr(xm[i[0]]>=i[1])

    if len(UBs)>0:
        for i in UBs:
            master.addConstr(xm[i[0]]<=i[1])

    master.setParam('OutputFlag', 0)
    master.optimize()

    #obtain shadow prices
    shaddow=[float('nan') for i in I]
    for i in I:
        constr = master.getConstrByName("c["+str(i)+"]")
        shaddow[i]=constr.Pi

    solValue=master.getAttr(gp.GRB.Attr.ObjVal)
    solution=[xm[p].X for p in P]
    return shaddow, solValue, solution

#Solve pricing model (see lecture)
def priceModel(v):
    price=gp.Model()

    ap=price.addVars(m,vtype=gp.GRB.INTEGER,name="a")

    price.setObjective(1-gp.quicksum(v[i]*ap[i] for i in I), gp.GRB.MINIMIZE)

    price.addConstr(gp.quicksum(ap[i]*w[i] for i in I)<=W)

    price.setParam('OutputFlag', 0)
    price.optimize()

    reducedCosts=price.getAttr(gp.GRB.Attr.ObjVal)              #Get reduced costs as value of the objective function
    newPattern=[ap[i].X for i in I]                             #Get new pattern

    return reducedCosts, newPattern

def BranchAndPrice():
    #Step0: Initialization: define patterns and starting patterns and define it best found solution
    #Generate basic patterns (basic patterns from exercise 22)
    PatternList=list(range(m))
    patterns=[[float('nan') for i in I] for j in PatternList]
    for i in I:
        for p in PatternList:
            if (p==i):
                patterns[i][p]=math.floor(W/w[i])
            else:
                patterns[i][p]=0
    bestSolution=[math.ceil(b[i]/patterns[i][i]) for i in I]
    bestSolutionValue=sum(bestSolution)
    openProblems=[[bestSolution, [], []]]

    while len(openProblems)>0:
        redCosts=-1                                                                                                     #set reduced costs to -1 to start while loop
        while redCosts<0:
            #Step 2: Solve relaxation of the problem
            dualVariables, objValue, openProblems[0][0]=masterModel(patterns, openProblems[0][1], openProblems[0][2])

            #check for non integer solution
            nonIntegerValues=[i for i in openProblems[0][0] if not float(i).is_integer()]

            #Step 3: Update best solution if applicable
            if len(nonIntegerValues)==0 and objValue<bestSolutionValue:
                bestSolutionValue=objValue
                bestSolution=openProblems[0][0]

            #Step 4: Column generation
            redCosts, PatternToAdd = priceModel(dualVariables)
            if (redCosts<0):                                                                                        #In case there are negative reduced costs, generate new pattern
                if PatternToAdd not in patterns:
                    patterns.append(PatternToAdd)
                else:
                    redCosts=0

        #Termination by Infeasibility does not have to be checked as there will always be a feasible solution when the starting patterns already give a feasible solution
        #Step 5: Termination by bound
        if math.ceil(objValue)>=bestSolutionValue:
            openProblems.pop(0)
            continue

        #Step6: Termination by solving
        if len(nonIntegerValues)==0:
            openProblems.pop(0)
        #Step 7: Branching
        else:
            branchingVariable = min(enumerate(openProblems[0][0]), key=lambda i: abs((i[1] % 1) - 0.5))[0]
            lowerBounds=openProblems[0][1].copy()
            lowerBounds.append([branchingVariable, math.ceil(openProblems[0][0][branchingVariable])])
            openProblems.append([openProblems[0][0], lowerBounds.copy(), openProblems[0][2].copy()])
            upperBounds=openProblems[0][2].copy()
            upperBounds.append([branchingVariable, math.floor(openProblems[0][0][branchingVariable])])
            openProblems.append([openProblems[0][0], openProblems[0][1].copy(), upperBounds.copy()])
            openProblems.pop(0)

    return bestSolutionValue, bestSolution, patterns

m=4                                 #number of patterns
b=[30,50,30,70]                     #demands
w=[25,25,35,20]                     #widths
W=85                                #Width of one stock
I=range(m)

finalObjValue, finalSol, finalPatterns=BranchAndPrice()                                                                 #Call B&P algorithm

print("Solution:",finalSol,"with Objective function value:", finalObjValue)                                             #Print solution
print("The patterns are:")
for i in range(len(finalSol)):
    if (finalSol[i]!=0):
        print(finalSol[i],"times pattern",finalPatterns[i])
