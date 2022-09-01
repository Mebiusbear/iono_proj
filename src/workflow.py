from src.apps.ionox import read_tec_file
from src.apps.make_plot import make_plot
from src.apps.spherical_harmonic import (spherical_triangle_transform,
                                         zip_point,
                                         fit_spherical_harmonic,
                                         concat_dataset_allpoint,
                                         concat_dask_workflow)
import numpy as np
import os
import time

class Fit_iono:
    def __init__(self,args):
        self.npixel = args.npixel
        self.steps = args.steps
        self.block_size = args.block_size
        self.n_worker = args.n_worker
        self.plot_only = args.plot_only

        output_dir = "./results"
        self.filename = "pixel_%d_step_%d.npy"%(self.npixel,self.steps)
        self.output_filename = os.path.join(output_dir,self.filename)

    def part_1(self):

        npixel = self.npixel
        steps= self.steps
        
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

    def part_2(self,point_zip,answer):

        npixel = self.npixel
        steps= self.steps
        block_size = self.block_size
        n_worker = self.n_worker

        if n_worker == 1:
            data = concat_dataset_allpoint(point_zip,steps=steps)
        else:
            data = concat_dask_workflow(point_zip=point_zip,steps=steps,block_size=block_size,n_worker=n_worker)
        
        ans_shape = answer.shape[0]
        xdata_2 = data.reshape(-1,ans_shape)
        res_data_2 = np.dot(xdata_2,answer.T)
        res_data_2 = res_data_2.reshape(npixel,npixel)

        np.save(self.output_filename,res_data_2)

    def makeplot(self):
        make_plot(self.output_filename)
    
    def run(self):
        point_zip,answer,_ = self.part_1()
        self.part_2(point_zip,answer)
