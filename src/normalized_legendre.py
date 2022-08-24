# normalized_legendre.py
import math
import numpy as np
def caculate_nkm(k,m):
    if m == 0:
        delta_0m = 1
    else:
        delta_0m = 0
    
    nkm = (2-delta_0m) * (2*k+1) * math.factorial(k-m) / math.factorial(k+m)
    return nkm

def caculate_pkm(k,m,theta):
    # print (k,m,theta)
    if m == 0:
        if k == 0:
            return 1
        if k == 1:
            return np.cos(theta)
        if k > 1:
            factory_1 = caculate_pkm(k-1,m,theta)*np.cos(theta)*(2*k-1)
            factory_2 = caculate_pkm(k-2,m,theta)*(k-1)
            return (factory_1-factory_2) / k
    elif m >= 1:
        factory_1 = caculate_pkm(k-1,m-1,theta)*(k+m-1)
        factory_2 = caculate_pkm(k,m-1,theta)*np.cos(theta)*(k-m+1)
        return (factory_1-factory_2) / np.sqrt(1-np.power(np.cos(theta),2))

def normalize_pkm(k,m,theta):
    return caculate_nkm(k,m) * caculate_pkm(k,m,theta)

def initial_nkm(steps):
    size = 6
    arr = np.zeros((size,size))
    for i in range(size):
        for j in range (size):
            # arr[i][j] = caculate_nkm(`1`)
            pass
    

    
if __name__ == "__main__":
    initial_nkm(10)

    
    