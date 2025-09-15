import gurobipy as gp           #Import Gurobi
import math

#m=4                     #Number of item types
#demands=[30,30,30,120]       #Demands
#widths=[20,22,25,26]  #Widths
#Width=70

m=5                     #Number of item types
demands=[10,15,20,15,5]       #Demands
widths=[17,21,22.5,24,29.5]  #Widths
Width=94

I=range(m)          #Set of item types
a=[0 for i in I]
for i in I:
    a[i]=math.ceil(demands[i]/int(Width/widths[i]))

n=sum(a)            #Upper bound of used large rolls
J=range(n)


model=gp.Model()    #Creation of the model

x=model.addVars(m,n,vtype=gp.GRB.INTEGER,name="x")            #Definition of decision variable x
y=model.addVars(n,vtype=gp.GRB.BINARY,name="y")               #Definition of decision variable y


model.setObjective(gp.quicksum(y[j] for j in J), gp.GRB.MINIMIZE)            #Minimize number of used rolls

model.addConstrs(gp.quicksum(x[i,j] for j in J)>=demands[i] for i in I)            #Constraint 1
model.addConstrs(gp.quicksum(widths[i]*x[i,j] for i in I)<=Width*y[j] for j in J)     #Constraint 2


model.optimize()                                                        #Optimize model


#model.printAttr(gp.GRB.Attr.ObjVal)                                     #Output Objective function value in terminal
model.printAttr(gp.GRB.Attr.X)                                          #Output optimal solution in terminal

patterns=[]
times=[]

for j in J:
    if y[j].X==1:
        pattern=[]
        for i in I:
            pattern.append(x[i,j].X)
        print(pattern)

        # newPattern=[]
        # for i in I:
        #     newPattern.append(x[i,j].X)
        # if len(patterns)==0:
        #     patterns.append(newPattern)
        #     times.append(1)
        # else:
        #     zahler=0
        #     equalSave=0
        #     zahlerSave=0
        #     for p in patterns:
        #         equal=1
        #         for i in I:
        #             if p[i]!=newPattern[i]:
        #                 equal=0
        #             if equal==1:
        #                 equalSave=1
        #                 ZahlerSave=zahler
        #         zahler=zahler+1

        #     if equalSave==1:
        #         times[ZahlerSave]=times[ZahlerSave]+1
        #     else:
        #         patterns.append(newPattern)
        #         times.append(1)
            

print("Objective function value:", model.getAttr(gp.GRB.Attr.ObjVal) )
print("The patterns are:")
for i in range(len(patterns)):
    print(times[i],"times pattern",patterns[i])

print("Solution when pattern allows only one type of item:", n)
print("Lower bound:", sum(demands[i]*widths[i] for i in I)/Width)
print(a)

