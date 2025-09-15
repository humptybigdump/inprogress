import math

def kolmogorovSmirnov(numbers, alpha):
    """
    Kolmogorov-Smirnov test for uniformity. If D <= D_alpha keep H0, otherwise reject.
    """
    
    numbers = sorted(numbers)
    N = len(numbers)
    D_plus = []
    D_minus = []

    i = 0 
    n = 1
    while i < N:
        D_plus.append((n/N)-numbers[i])
        D_minus.append(numbers[i]-((n-1)/N))
        i += 1
        n += 1
    
    max_D_plus = max(D_plus)
    max_D_minus = max(D_minus)

    D = max(max_D_plus, max_D_minus)

    D_alpha = 0
    if alpha == 0.99:
        D_alpha = 1.62762/math.sqrt(N)
    elif alpha == 0.95:
        D_alpha = 1.35810/math.sqrt(N)
    elif alpha == 0.90:
        D_alpha = 1.22385/math.sqrt(N)

    print("D_alpha: " + str(D_alpha) + "  D: " + str(D))
    if D <= D_alpha:
        print("Keep H0")
    else: print ("Reject H0")

def runsTest(numbers, alpha, maxRunLength):

    N = len(numbers)    
    expectedRuns = []
    observedRuns = []
    runs = []
    
    #expected
    i = 0
    for i in range(maxRunLength):
        expectedRun = (2/math.factorial(i+3)) * (N*(math.pow(i,2)+3*i+1)-(math.pow(i,3)+3*math.pow(i,2)-i-4))
        expectedRuns.append(expectedRun)
        i += 1
    
    #observed
    i = 0
    difference = 0
    for i in range(N-1):
        difference = numbers[i+1] - numbers[i]
        if difference > 0:
            runs.append(1)
        else: runs.append(0)
    runs.append(-1)

    """
    i = 0
    for i in range(maxRunLength):
        observedRun = 0
        j = 0
        for j in range(N-1):
            if all(p == runs[j] for p in runs[j-1:j]):
                observedRun += 1
        observedRuns.append(observedRun-1)
    """

    value = 0

    
    idx = 0
    while True:
        j = 0
        while True:
            idx+=1
            j+=1
            if runs[idx] != runs[idx-1]:
                break
        value += 1
        observedRuns.insert(j,value)       
        if idx >= len(runs)-1:
            break

    length = 1
    for i in range(maxRunLength):
        if observedRuns[i-1] > 0:
            length += 1

    print(length)

    onr = 0 
    for i in range(length)-1:
        onr += observedRuns[i]

    print(onr)

    print(observedRuns)
    







    #print(numbers)
    #print(expectedRuns)
    #print(runs)
    #print(observedRuns)


    return None



    



    
