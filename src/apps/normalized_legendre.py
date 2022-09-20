# normalized_legendre.py
import math
import numpy as np
def caculate_nkm(k,m):
    if m == 0:
        delta_0m = 1
    else:
        delta_0m = 0
    
    nkm = (2-delta_0m) * (2*k+1) * math.factorial(k-m) / math.factorial(k+m)
    return np.sqrt(nkm)

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


# test！
def ath2_nkm(k,m,theta):
    if m == 0:
        if k == 0:
            return 1
        if k == 1:
            return np.sqrt(3) * np.cos(theta)
        if k > 1:
            factor_1 = np.sqrt(4*k**2-1) / k * np.cos(theta) * ath2_nkm(k-1,m,theta)
            factor_2 = (k-1) / k * np.sqrt((2*k+1)/(2*k-3)) * ath2_nkm(k-2,m,theta)
            return factor_1 - factor_2
    else:
        if m == k:
            if m == 1:
                return np.sqrt(3) * np.cos(theta)
            else:
                return np.sqrt((2*k+1)/ (2*k)) * np.sin(theta) * ath2_nkm(k-1,k-1,theta)
        elif m == k-1:
            return np.sqrt(2*k+1) * np.sin(theta) * ath2_nkm(k-1,k-1,theta)
        elif m < k-1:
            factor_1 = np.sqrt((4*k**2-1)/(k**2-m**2)) * np.sin(theta) * ath2_nkm(k-1,m,theta)
            factor_2 = np.sqrt((2*k+1)*((k-1)**2-m**2)/(2*k-3)/(k**2-m**2)) * ath2_nkm(k-2,m,theta)
            return factor_1 - factor_2
        
if __name__ == "__main__":

    print ("k,m=1,1;",np.allclose(ath2_nkm(1,1,0.3),normalize_pkm(1,1,0.3)))
    print ("k,m=2,1;",np.allclose(ath2_nkm(2,1,0.3),normalize_pkm(2,1,0.3)))
    print ("k,m=2,2;",np.allclose(ath2_nkm(2,2,0.3),normalize_pkm(2,2,0.3)))
    print ("k,m=3,1;",np.allclose(ath2_nkm(3,1,0.3),normalize_pkm(3,1,0.3)))
    