from os.path import isfile
import numpy as np
from mesh_utils import rectangular_mesh


# check if file fractional_step.py exists:
if not isfile('fractional_step.py'):
    raise Exception('cannot find file "fractional_step.py"; please place this script in the same folder as  "fractional_step.py".')
else:
    import fractional_step as totest


################
# ACTUAL TESTS #
################


def test_star():

    m = rectangular_mesh(15, 1, 20, 1)

    pn = np.fromfile('tests/input_p.bin').reshape(15,20)

    un = np.fromfile('tests/input_u.bin').reshape(16,22)
    us_correct = np.fromfile('tests/output_u.bin').reshape(16,22)
    us_tested = np.zeros_like(un)

    vn  = np.fromfile('tests/input_v.bin').reshape(17,21)
    vs_correct = np.fromfile('tests/output_v.bin').reshape(17,21)
    vs_tested = np.zeros_like(vn)
    
    dt = 1
    re = 100

    us_tested,vs_tested = totest.get_star(us_tested, vs_tested, un, vn, pn, m, dt, re)
 
    uerr = np.amax(abs(us_correct - us_tested))
    verr = np.amax(abs(vs_correct - vs_tested))

    print()
    print('Testing function for the calculation of u*')
    print('Maximum error on horizontal component:  ', uerr)
    print('Maximum error on vertical component:    ', verr)
    print()



def test_matrix():

    m = rectangular_mesh(15, 1, 20, 1)

    totest.get_poisson_matrix(m)
    print(totest.A_poisson)
    A_poisson=np.fromfile('tests/output_A_poisson.bin')

    maxerr = np.amax(abs(A_poisson - totest.A_poisson.toarray().flatten()))
    
    print()
    print('Testing function for the calculation of coefficient matrix of Poisson solver')
    print('Maximum error on coefficient matrix:  ', maxerr)
    print()



def test_poisson():

    m = rectangular_mesh(15, 1, 20, 1)
    dt = 1

    totest.get_poisson_matrix(m)

    pc_correct = np.fromfile('tests/output_pc.bin').reshape(15,20)
    pc_tested  = np.zeros((15,20))

    us = np.fromfile('tests/input_u.bin').reshape(16,22)
    vs = np.fromfile('tests/input_v.bin').reshape(17,21)

    pc_tested = totest.solve_poisson(m, us, vs, pc_tested, dt)
    
    err = abs(pc_correct-pc_tested); err = err - np.mean(err)

    maxerr = np.amax(err)

    print()
    print('Testing poisson solver')
    print('Maximum error on pressure correction:  ', maxerr)
    print()



#############
# MAIN MENU #
#############

print()
print('What do you want to test?')
print('1 ---> get_star')
print('2 ---> get_poisson_matrix')
print('3 ---> solve_poisson')
print()
choice = input('Enter the number corresponding to your choice:   ')
not_valid = True
while not_valid:
    if choice == '1':
        not_valid = False
        test_star()
    elif choice == '2':
        not_valid = False
        test_matrix()
    elif choice == '3':
        not_valid = False
        test_poisson()
    else:
        print()
        print('INVALID NUMBER; here are your options:')
        print('1 ---> get_star')
        print('2 ---> get_poisson_matrix')
        print('3 ---> solve_poisson')
        print()
        choice = input('Please enter a valid number:   ')