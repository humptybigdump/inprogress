import random

def calculateScheduleTimes(jobSequence):                                        #calculates completion times and tardiness for the schedule with the given job sequence
    completionTimes=[float('nan') for i in range(n)]
    tardiness=[float('nan') for i in range(n)]
    completionTimes[jobSequence[0]]=p[jobSequence[0]]
    for i in range(1,len(jobSequence)):
        completionTimes[jobSequence[i]]=completionTimes[jobSequence[i-1]]+p[jobSequence[i]]
    for i in range(len(jobSequence)):
        tardiness[jobSequence[i]]=max(0, completionTimes[jobSequence[i]]-d[jobSequence[i]])
    return tardiness

def mooresAlgorithm():
    S=list(range(n))
    S.sort(key=lambda i:d[i])               #sort jobs in increasing order of their due dates
    J=[]                                    #generate empty J
    T=calculateScheduleTimes(S)             #calculate tardiness
    firstTardyJob=n+1
    while firstTardyJob>=0:                 #as long there is a tardy job in S
        firstTardyJob=-1
        for j in S:                
            if T[j]>0:
                firstTardyJob=j
                firstTardyJobPosition=S.index(firstTardyJob)    #determine first tardy job position
                u=max(S[:firstTardyJobPosition+1],key=lambda i:p[i])    #determine job with the longest processing time not starting after firstTardyJob
                J.append(u)                                         
                S.remove(u)                                     #delete u from S
                T=calculateScheduleTimes(S)                     #calculate tardiness of new job sequence
    S.extend(J)                                                 #termination step
    T=calculateScheduleTimes(S)                                 #calculate tardiness of final job sequence
    u=0
    for i in range(n):                                          #calculate number of tardy jobs
        if T[i]>0:
            u=u+1
    return S, u


        

d=[8,12,4,13,14]                                                  #input parameters
p=[4,7,1,6,3]
n=len(p)
finalSchedule, numberTardyJobs=mooresAlgorithm()                #use Moore's algorithm
print("Obtained job sequence:",finalSchedule, "with a number of tardy jobs:", numberTardyJobs,".")                           #print solution

