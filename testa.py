import math
import scipy.stats



def kolmogorov_smirnov(numbers, alpha):

    print("\n___________KS-Test___________\n")


    numbers_ranked = sorted(numbers, reverse=False) 
    n = len(numbers_ranked)

    d_plus = []
    d_minus = []
    i = 1
    for number in numbers_ranked:
        d_plus.append(i/n - number)
        d_minus.append(number-(i-1)/n)
        i += 1

    d = max((max(d_plus),max(d_minus)))

    if alpha == 0.1:
        d_alpha = 1.22385/math.sqrt(n)
    elif alpha == 0.05:
        d_alpha = 1.35810/math.sqrt(n)
    elif alpha == 0.01:
        d_alpha = 1.62762/math.sqrt(n)
    else: ValueError("wrong alpha")

    print("D_alpha: " + str(d_alpha) + "  " + "D: " + str(d))
    if d <= d_alpha:
        print("Keep H0")
    else: print("Reject H0")

def runs_test(numbers,alpha,max_run_length):
    
    print("\n___________Runs-Test___________\n")

    numbers_prev = numbers.copy()
    numbers_prev.insert(0,1)

    runs = []

    i = 0
    for number in numbers:
        if number > numbers_prev[i]:
            runs.append(1)
        if number < numbers_prev[i]:
            runs.append(0)
        i += 1

    runs = runs[1:]

    runs_dict = dict()
    initial_relation = runs[0]
    k = 1
    for relation in runs[1:]:
        if relation == initial_relation:
            k += 1
            continue
        if relation != initial_relation:
            initial_relation = relation
            if k not in runs_dict:
                runs_dict[k] = 0
            runs_dict[k] += 1
            k = 1
    print("Observed:")
    print(runs_dict)

    #expected
    expected_dict = dict()
    i = 1
    N = len(numbers)
    for i in range(1,max_run_length+1):
        expectedRun = (2/math.factorial(i+3)) * (N*(math.pow(i,2)+3*i+1)-(math.pow(i,3)+3*math.pow(i,2)-i-4))
        if i not in expected_dict:
                expected_dict[i] = 0
        expected_dict[i] = expectedRun
        i += 1
    print("Expected:")
    print(expected_dict)

    #
    sum_up = []
    i = 1
    for i in range(1,max_run_length+1):
        sum_up.append(math.pow(expected_dict[i]-runs_dict[i],2)/expected_dict[i])
    
    chi_zero = sum(sum_up)
    df = max_run_length - 1

    chi_table_value =  scipy.stats.chi2.ppf(1-alpha, df=df)

    print("Chi value: " + str(chi_zero) + "  " + "Reference value: " + str(chi_table_value))
    if chi_zero <= chi_table_value:
        print("Keep H0")
    else: print("Reject H0")

    print("\n\n")



        

        

        
        
