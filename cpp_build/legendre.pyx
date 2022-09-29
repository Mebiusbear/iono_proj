import math
import numpy as np



# def factorial(int num):
#     cdef int res = 1;
#     for i in range (1,num+1):
#         res *= i
#     return res

def caculate_nkm(k,m):
    if m == 0:
        delta_0m = 1;
    else:
        delta_0m = 0;
    nkm = np.float64();
    nkm = (2-delta_0m) * (2*k+1) * math.factorial(k-m) / math.factorial(k+m);
    return np.sqrt(nkm);

def caculate_pkm(int k,int m, double theta):
    cdef double factory_1;
    cdef double factory_2;
    # print (k,m,theta)
    if m == 0:
        if k == 0:
            return 1;
        if k == 1:
            return np.cos(theta);
        if k > 1:
            factory_1 = caculate_pkm(k-1,m,theta)*np.cos(theta)*(2*k-1);
            factory_2 = caculate_pkm(k-2,m,theta)*(k-1);
            return (factory_1-factory_2) / k;
    elif m >= 1:
        factory_1 = caculate_pkm(k-1,m-1,theta)*(k+m-1);
        factory_2 = caculate_pkm(k,m-1,theta)*np.cos(theta)*(k-m+1);
        return (factory_1-factory_2) / np.sqrt(1-np.power(np.cos(theta),2));

def normalize_pkm(k,m,theta):
    return caculate_nkm(k,m) * caculate_pkm(k,m,theta);
