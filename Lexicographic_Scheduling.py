import random

def calculateScheduleTimes(jobSequence):                                        #calculates completion times, lateness and tardiness for the schedule with the given job sequence
    completionTimes=[float('nan') for i in range(n)]
    lateness=[float('nan') for i in range(n)]
    tardiness=[float('nan') for i in range(n)]
    completionTimes[jobSequence[0]]=p[jobSequence[0]]
    for i in range(1,len(jobSequence)):
        completionTimes[jobSequence[i]]=completionTimes[jobSequence[i-1]]+p[jobSequence[i]]
    for i in range(len(jobSequence)):
        lateness[jobSequence[i]]=completionTimes[jobSequence[i]]-d[jobSequence[i]]
        tardiness[jobSequence[i]]=max(0, completionTimes[jobSequence[i]]-d[jobSequence[i]])
    return completionTimes, lateness, tardiness

def totalCompletionTimeWithDeadlines(deadlines):                                #algorithm for determining the total completion time with given deadlines
    tau=sum(p)                                                                  #determine tau
    Jc=list(range(n))                                                           #create set J^c
    jobSequence=[float('nan') for i in range(n)]                                #empty job sequence
    for k in range(n-1, -1, -1):
        consideredDeadlines=[float('nan') for i in range(n)]
        for i in Jc:
            if deadlines[i]>=tau:
                consideredDeadlines[i]=deadlines[i]                             #determine which deadlines have to be considered in Jc (those with deadlines larger or equal tau)
        JobsDeadlineLargerTau=[i for i, l in enumerate(consideredDeadlines) if l>=tau]  #determine job-IDs of jobs which have a deadline larger or equal tau
        kStar=max(JobsDeadlineLargerTau, key=lambda i:p[i])                     #deter ine k*
        jobSequence[k]=kStar                                                    #put k* into position k
        tau=tau-p[kStar]                                                        #determine new tau
        Jc.remove(kStar)
    return jobSequence

def SPT_EDD():
    S=list(range(n))
    S.sort(key=lambda i:(p[i], d[i]))                   #sort jobs in increasing order of their processing times, in case of a tie sort according to their due dates
    return S

def LmaxTCT():
    EDDSequence=list(range(n))
    EDDSequence.sort(key=lambda i:d[i])                 #apply EDD rule
    C, L, T=calculateScheduleTimes(EDDSequence)
    z=max(L)                                            #determine maximum lateness of the EDD job sequence
    dBar=[d[i]+z for i in range(n)]                     #determine deadlines
    S=totalCompletionTimeWithDeadlines(dBar)            #use algorithm for minimizing the total completion time with deadlines
    return S
 

d=[3,4,5,7,7]                                                   #input parameters
p=[2,3,1,2,1]
n=len(p)
sequenceTCTLmax=SPT_EDD()                                       #Use SPT-EDD rule to obtain a schedule / job sequence
C, L, T=calculateScheduleTimes(sequenceTCTLmax)                 #calculate completion times, lateness, and tardiness for SPT-EDD job sequence
Lmax_TCTLmax=max(L)                                             #determine maximum lateness for SPT-EDD job sequence
TCT_TCTLmax=sum(C)                                              #determine total completion time for SPT-EDD job sequence
sequenceLmaxTCT=LmaxTCT()                                       #Use algorithm for lexicographic scheduling with the primary objective minimizing the maximum lateness to obtain a schedule / job sequence
C, L, T=calculateScheduleTimes(sequenceLmaxTCT)                 #calculate completion times, lateness, and tardiness for obtained job sequence
Lmax_LmaxTCT=max(L)                                             #determine maximum lateness for obtained job sequence
TCT_LmaxTCT=sum(C)                                              #determine total completion time for obtained job sequence

#print solution
print("Schedule for Lexicographic Machine Scheduling with the primary objective minimizing the total completion time:", sequenceTCTLmax, "with total completion time:",TCT_TCTLmax, "and maximum lateness", Lmax_TCTLmax,"." )
print("Schedule for Lexicographic Machine Scheduling with the primary objective minimizing the maximum lateness:", sequenceLmaxTCT, "with total completion time:",TCT_LmaxTCT, "and maximum lateness", Lmax_LmaxTCT,"." )