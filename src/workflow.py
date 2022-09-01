from src.apps.ionox import read_tec_file
from src.apps.make_plot import make_plot
from src.apps.spherical_harmonic import (spherical_triangle_transform,
                                         zip_point,
                                         fit_spherical_harmonic,
                                         concat_dataset_allpoint)
import numpy as np
import argparse
import os
import time


def main(steps,npixel):

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

    return point_zip,answer,xdata_1

def concat_dask_workflow(point_zip,steps,block_size,n_worker):   
    import dask 
    from dask.distributed import Client 
    client = Client(n_workers=n_worker)    
    print ("dask_board: ",str(client.dashboard_link))  
    new_point_zip = point_zip.reshape(block_size,-1,2)  
    task = list()   
    for i in range (block_size):
        task.append(dask.delayed(concat_dataset_allpoint)(point_zip=new_point_zip[i],steps=steps))
    data = np.array(dask.compute(*task))
    return data


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='YOLO Detection')
    parser.add_argument("-np","--npixel", type=int, help="the pixel.", default=100)
    parser.add_argument("-s","--steps", type=int, help="the steps.", default=5)
    parser.add_argument("-nw","--n_worker", type=int, help="n_worker.", default=8)
    parser.add_argument("-bs","--block_size", type=int, help="block_size.", default=400)
    parser.add_argument("-po","--plot_only", type=bool, help="plot_only.", default=False)

    
    args = parser.parse_args()

    npixel = args.npixel
    steps= args.steps
    block_size = args.block_size
    n_worker = args.n_worker
    plot_only = args.plot_only


    output_dir = "./results"
    filename = "pixel_%d_step_%d.npy"%(npixel,steps)
    output_filename = os.path.join(output_dir,filename)

    if plot_only:
        make_plot(output_filename)

    else:

        # print ("start_time:\n",time.localtime())
        start_time = time.time()
        point_zip,answer,xdata_1 = main(steps,npixel)
        # data = concat_dataset_allpoint(point_zip,steps=steps)
        data = concat_dask_workflow(point_zip=point_zip,steps=steps,block_size=block_size,n_worker=n_worker)
        
        ans_shape = answer.shape[0]
        xdata_2 = data.reshape(-1,ans_shape)
        res_data_2 = np.dot(xdata_2,answer.T)
        res_data_2 = res_data_2.reshape(npixel,npixel)

        print ("use_time(s):",time.time()-start_time)


        np.save(output_filename,res_data_2)