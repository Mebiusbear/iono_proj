# least_square.py
import numpy as np
def least_square(i_variable,d_variable):
    '''
    input:
        i_variable = [X_1, X_2, ..., X_n]
        d_variable = [Y_1, Y_2, ..., Y_n]

    return:
        ans = [b_1, b_2, ..., b_n]
    '''
    factory = np.dot(i_variable.T,i_variable)
    factory = np.array(factory,dtype=np.float64)
    factory_inv = np.linalg.inv(factory)

    return np.dot(np.dot(factory_inv,i_variable.T),d_variable)