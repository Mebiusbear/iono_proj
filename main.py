from src import (read_tec_file,
                spherical_triangle_transform,
                zip_point,
                fit_spherical_harmonic,
                concat_dataset_allpoint,
                zip_point)
import os
import numpy as np

npixel = 200
steps= 6

data_dir = "./data"
filename = os.path.join(data_dir,"CODG%03d0.22I"%(10))

tecarray, _, lonarray, latarray, _ = read_tec_file(filename)
tec_dataset = tecarray[4][40:55,35:50]
ydata = tec_dataset.reshape(1,-1)[0]
ydata = np.array(ydata,dtype=np.float64)

lon_dataset = lonarray[35:50]
lat_dataset = latarray[40:55]
beta_c_arr, lam_c_arr = spherical_triangle_transform(lon_dataset,lat_dataset,p_lat=np.radians(10),p_lon=np.radians(10))
point_zip = zip_point(beta_c_arr, lam_c_arr)

xdata_1,answer = fit_spherical_harmonic(point_zip,ydata,steps=steps)

new_lon_dataset = np.linspace(-5,65,npixel)
new_lat_dataset = np.linspace(-12.5,-47.5,npixel)
beta_c_arr, lam_c_arr = spherical_triangle_transform(new_lon_dataset,new_lat_dataset,p_lat=np.radians(10),p_lon=np.radians(10))
point_zip = zip_point(beta_c_arr, lam_c_arr)


if __name__ == "__main__":
    import dask
    import time
    from dask.distributed import Client
    client = Client(n_workers=8)
    print (str(client.dashboard_link))
    print ("start_time:\n",time.localtime())
    start_time = time.time()

    block_size = 400
    new_point_zip = point_zip.reshape(block_size,-1,2)
    task = list()
    for i in range (block_size):
        task.append(dask.delayed(concat_dataset_allpoint)(point_zip=new_point_zip[i],steps=steps))
    data = np.array(dask.compute(*task))
    
    ans_shape = answer.shape[0]
    xdata_2 = data.reshape(-1,ans_shape)
    res_data_2 = np.dot(xdata_2,answer.T)
    res_data_2 = res_data_2.reshape(npixel,npixel)

    print ("use_time(s):",time.time()-start_time)