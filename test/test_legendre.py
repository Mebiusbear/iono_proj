from src.apps import legendre
from src.apps import normalized_legendre
from src.apps.spherical_harmonic import spherical_triangle_transform,zip_point
import numpy as np



def concat_dataset(theta,lam_c,normalize_func,steps=5):
    '''
    pnm * [cos(m*lam) for k in range (9) for m in range (1,k+1) if m < 7]
    pnm * [sin(m*lam) for k in range (9) for m in range (1,k+1) if m < 7]
    output:
        array[cos, sin]
    '''
    # from src.apps.normalized_legendre import normalize_pkm
    m = np.array([m for k in range (steps+1) for m in range (1,k+1) if m < 7])
    lam_c_arr = np.ones_like(m) * lam_c * m
    para_cos_arr = np.cos(lam_c_arr)
    para_sin_arr = np.sin(lam_c_arr)
    
    para_pnm_arr = np.array([normalize_pkm(k,m,theta) for k in range (steps+1) for m in range (1,k+1) if m < 7],dtype=np.float64)
    
    factory_1 = para_cos_arr * para_pnm_arr 
    factory_2 = para_sin_arr * para_pnm_arr

    ans = np.concatenate((factory_1,factory_2))
    return ans

def concat_dataset_allpoint(point_zip,normalize_func,steps=5):
    a, b = point_zip[0]
    c = concat_dataset(a,b,steps)
    c_shape = c.shape[0]
    xdata = np.zeros((len(point_zip),c_shape),np.float64)
    for i,(beta_c,lam_c) in enumerate(point_zip):
        xdata[i] = concat_dataset(beta_c,lam_c,normalize_func,steps)
    return xdata


def concat_dask_workflow(point_zip,steps,block_size,n_worker,scheduler,normalize_func):   
    import dask 
    from dask.distributed import Client
    client = Client(n_workers=n_worker)

    new_point_zip = point_zip.reshape(block_size,-1,2)
    task = list()
    for i in range (block_size):
        task.append(dask.delayed(concat_dataset_allpoint)(point_zip=new_point_zip[i],normalize_func=normalize_func,steps=steps))
    data = np.array(dask.compute(*task))
    client.close()
    return data

def main():
    npixel = 2000
    pixel_per_screensize_km = 0.1

    screensize_km  = pixel_per_screensize_km * npixel
    earth_r = 6371.393
    iono_r  = earth_r + 300
    iono_deg = screensize_km * 180 / iono_r / np.pi
    iono_half_deg = iono_deg / 2

    # print ("pixel_per_screensize",pixel_per_screensize_km,"(km)")


    new_lon_dataset = np.linspace(116.4525771-iono_half_deg,116.4525771+iono_half_deg,npixel,dtype=np.float64)
    new_lat_dataset = np.linspace(-26.60055525-iono_half_deg,-26.60055525+iono_half_deg,npixel,dtype=np.float64)
    beta_c_arr, lam_c_arr = spherical_triangle_transform(new_lon_dataset,new_lat_dataset,p_lat=np.radians(10),p_lon=np.radians(10)) 
    # print ("longitude range : ",new_lon_dataset[0],new_lon_dataset[-1])
    # print ("latitude range : ",new_lat_dataset[0],new_lat_dataset[-1])
    point_zip = zip_point(beta_c_arr, lam_c_arr)

    
    concat_dask_workflow(point_zip=point_zip,steps=6,block_size=1000,n_worker=20,scheduler=None,normalize_func=legendre.normalize)

if __name__ == "__main__":
    main()    