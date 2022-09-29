# spherical_harmonic.py
import logging
from src.apps.dask_init import dask_init
import dask 
import numpy as np
import time

from src.apps.least_square import least_square



def spherical_triangle_transform(lon_dataset,lat_dataset,p_lat=0,p_lon=0):
    '''
    from GCS to SCS
    '''
    lat = np.deg2rad(lat_dataset)
    beta = np.pi/2 * np.ones_like(lat) - lat
    lam = np.deg2rad(lon_dataset)

    beta_shift,lam_shift = np.meshgrid(lam,beta)
    beta_n = p_lat * np.ones_like(beta_shift)
    lam_n = p_lon * np.ones_like(lam_shift)

    beta_c_arr = np.arccos(
        np.cos(beta_n)*np.cos(beta_shift) + np.sin(beta_n)*np.sin(beta_shift)*np.cos(lam_n-lam_shift)
        )
    lam_c_arr = np.arcsin(
        np.sin(lam_shift-lam_n)*np.sin(beta_shift) / np.sin(beta_c_arr)
        )
    return beta_c_arr, lam_c_arr

def zip_point(beta_c_arr, lam_c_arr):
    '''
    row,col = beta_c_arr.shape
    ydata = list()
    point_list = list()
    for i in range (row):
        for j in range (col):
            point_list.append((beta_c_arr[i][j],lam_c_arr[i][j]))
            ydata.append(tec_dataset[i][j])
    '''
    beta_c_arr_flatten = beta_c_arr.reshape(1,-1)
    lam_c_arr_flatten = lam_c_arr.reshape(1,-1)
    point_zip = np.concatenate((beta_c_arr_flatten,lam_c_arr_flatten)).T
    return point_zip

def concat_dataset(theta,lam_c,steps=5,use_cpp=False):

    '''
    pnm * [cos(m*lam) for k in range (9) for m in range (1,k+1) if m < 7]
    pnm * [sin(m*lam) for k in range (9) for m in range (1,k+1) if m < 7]
    output:
        array[cos, sin]
    '''
    if use_cpp:
        try:
            from src.apps.legendre import normalize_pkm
            # logging.info("Use C++ to jiasu")
        except Exception as e:
            from src.apps.normalized_legendre import normalize_pkm
            # logging.info(e)
            # logging.info("Use python")
    else:
        from src.apps.normalized_legendre import normalize_pkm
        # logging.info("Use python")


    m = np.array([m for k in range (steps+1) for m in range (1,k+1) if m < 7])
    lam_c_arr = np.ones_like(m) * lam_c * m
    para_cos_arr = np.cos(lam_c_arr)
    para_sin_arr = np.sin(lam_c_arr)
    
    para_pnm_arr = np.array([normalize_pkm(k,m,theta) for k in range (steps+1) for m in range (1,k+1) if m < 7],dtype=np.float64)
    
    factory_1 = para_cos_arr * para_pnm_arr 
    factory_2 = para_sin_arr * para_pnm_arr

    ans = np.concatenate((factory_1,factory_2))
    return ans

def concat_dataset_allpoint(point_zip,steps=5,use_cpp=False):

    a, b = point_zip[0]
    c = concat_dataset(a,b,steps)
    c_shape = c.shape[0]
    xdata = np.zeros((len(point_zip),c_shape),np.float64)
    for i,(beta_c,lam_c) in enumerate(point_zip):
        xdata[i] = concat_dataset(beta_c,lam_c,steps,use_cpp)

    return xdata

def concat_dask_workflow(args,point_zip,steps,block_size,n_worker,scheduler,use_cpp=False): 

    client = dask_init(args,n_worker,scheduler)

    new_point_zip = point_zip.reshape(block_size,-1,2)
    task = list()
    for i in range (block_size):
        task.append(dask.delayed(concat_dataset_allpoint)(point_zip=new_point_zip[i],steps=steps,use_cpp=use_cpp))
    data = np.array(dask.compute(*task))
    client.close()
    return data

def fit_spherical_harmonic(point_zip,ydata,steps=5):
    # from src.apps.least_square import least_square

    xdata = concat_dataset_allpoint(point_zip,steps)
    answer = least_square(xdata,ydata)

    return xdata,answer

if __name__ == "__main__":
    import ionox
    import matplotlib.pyplot as plt
    data_dir = "./"
    filename = data_dir+"CODG%03d0.22I"%(1)

    tecarray, _, lonarray, latarray, _ = ionox.read_tec_file(filename)
    tec_dataset = tecarray[18][15:35,50:64] # 第18时序，(2.5-52.5N，70-135E)
    ydata = tec_dataset.reshape(1,-1)[0]
    ydata = np.array(ydata,dtype=np.float64)

    lon_dataset = lonarray[50:64]
    lat_dataset = latarray[15:35]
    beta_c_arr, lam_c_arr = spherical_triangle_transform(lon_dataset,lat_dataset)
    point_zip = zip_point(beta_c_arr, lam_c_arr)

    xdata_1,answer = fit_spherical_harmonic(point_zip,ydata)

    new_lon_dataset = np.linspace(70,135,71)
    new_lat_dataset = np.linspace(52.5,2.5,101)
    beta_c_arr, lam_c_arr = spherical_triangle_transform(new_lon_dataset,new_lat_dataset)
    point_zip = zip_point(beta_c_arr, lam_c_arr)
    xdata_2 = list()
    for beta_c,lam_c in point_zip:
        xdata_2.append(concat_dataset(beta_c,lam_c))
    xdata_2 = np.array(xdata_2,dtype=np.float64)

    plt.figure(figsize=(16,9))

    plt.subplot(131)
    plt.title("origin")
    plt.axis("off")
    plt.imshow(np.array(ydata).reshape(20,14))

    plt.subplot(132)
    plt.title("280 point")
    plt.axis("off")
    res_data_1 = np.dot(xdata_1,answer.T)
    plt.imshow(res_data_1.reshape(20,14))

    plt.subplot(133)
    plt.title("7171point")
    plt.axis("off")
    res_data_2 = np.dot(xdata_2,answer.T)
    plt.imshow(res_data_2.reshape(101,71))

    plt.show()
