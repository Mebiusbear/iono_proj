import sys
import numpy as np
import os
sys.path.append("./")

from src.apps.ionox import read_tec_file
from src.apps.make_plot import make_mul_plot, make_plot
from src.apps.spherical_harmonic import (spherical_triangle_transform,
                                         zip_point,
                                         fit_spherical_harmonic,
                                         concat_dataset_allpoint,
                                         concat_dask_workflow)


class Fit_iono:
    def __init__(self,args):
        self.npixel = args.npixel
        self.steps = args.steps
        self.block_size = args.block_size
        self.n_worker = args.n_worker
        self.plot_only = args.plot_only
        self.mac_run = args.mac_run
        self.scheduler = args.scheduler
        self.pixel_per_screensize_km = args.pscale

        output_dir = "./results"
        self.image_filename = "pixel_%d_step_%d_scale_%d.npy"%(self.npixel,self.steps,int(self.pixel_per_screensize_km*1000))
        self.image_filename = os.path.join("image_npy",self.image_filename)
        self.output_image_filename = os.path.join(output_dir,self.image_filename)

        self.param_filename = "param_step_%d.npy"%(self.steps)
        self.param_filename = os.path.join("param",self.param_filename)
        self.output_param_filename = os.path.join(output_dir,self.param_filename)

    def part_1(self):
        range_size = 15
        lon_start = 50
        lon_end = lon_start+range_size
        lat_start = 36
        lat_end = lat_start+range_size

        npixel = self.npixel
        steps= self.steps
        
        data_dir = "./data" 
        filename = os.path.join(data_dir,"CODG%03d0.22I"%(10))  

        tecarray, _, lonarray, latarray, _ = read_tec_file(filename)    
        # tec_dataset = tecarray[4][40:55,35:50] # old
        tec_dataset = tecarray[21][lon_start:lon_end,lat_start:lat_end] # new
        ydata = tec_dataset.reshape(1,-1)[0]
        ydata = np.array(ydata,dtype=np.float64)    

        # lon_dataset = lonarray[35:50]   # old
        # lat_dataset = latarray[40:55]   # old
        lon_dataset = lonarray[lon_start:lon_end]   # new
        lat_dataset = latarray[lat_start:lat_end]   # new

        beta_c_arr, lam_c_arr = spherical_triangle_transform(lon_dataset,lat_dataset,p_lat=np.radians(10),p_lon=np.radians(10)) 
        point_zip = zip_point(beta_c_arr, lam_c_arr)    

        xdata_1,answer = fit_spherical_harmonic(point_zip,ydata,steps=steps)
        if self.plot_only:
            answer = np.load(self.output_param_filename)
        res_data_1 = np.dot(xdata_1,answer.T).reshape(15,15)

        return (ydata,res_data_1),answer

    def part_2(self):
        npixel = self.npixel
        steps= self.steps
        pixel_per_screensize_km = self.pixel_per_screensize_km
        screensize_km  = pixel_per_screensize_km * npixel
        
        earth_r = 6371.393
        iono_r  = earth_r + 300
        iono_deg = screensize_km * 180 / iono_r / np.pi
        iono_half_deg = iono_deg / 2

        print ("pixel_per_screensize",pixel_per_screensize_km,"(km)")


        # new_lon_dataset = np.linspace(70,140,npixel) 
        # new_lat_dataset = np.linspace(-2.5,-37.5,npixel)   
        new_lon_dataset = np.linspace(116.4525771-iono_half_deg,116.4525771+iono_half_deg,npixel,dtype=np.float64)
        new_lat_dataset = np.linspace(-26.60055525-iono_half_deg,-26.60055525+iono_half_deg,npixel,dtype=np.float64)
        beta_c_arr, lam_c_arr = spherical_triangle_transform(new_lon_dataset,new_lat_dataset,p_lat=np.radians(10),p_lon=np.radians(10)) 
        print ("longitude range : ",new_lon_dataset[0],new_lon_dataset[-1])
        print ("latitude range : ",new_lat_dataset[0],new_lat_dataset[-1])
        point_zip = zip_point(beta_c_arr, lam_c_arr)

        return point_zip

    def part_3(self,point_zip,answer):

        npixel = self.npixel
        steps= self.steps
        block_size = self.block_size
        n_worker = self.n_worker
        scheduler = self.scheduler

        if n_worker == 1:
            data = concat_dataset_allpoint(point_zip,steps=steps)
        else:
            print ("Part 3, run on dask!")
            data = concat_dask_workflow(point_zip=point_zip,steps=steps,block_size=block_size,n_worker=n_worker,scheduler=scheduler)
        
        ans_shape = answer.shape[0]
        xdata_2 = data.reshape(-1,ans_shape)
        res_data_2 = np.dot(xdata_2,answer.T)
        res_data_2 = res_data_2.reshape(npixel,npixel)

        np.save(self.output_image_filename,res_data_2)

    def makeplot(self):
        make_plot(self.output_image_filename)

    def makemulplot(self):
        (ydata,res_data_1), answer = self.part_1()  
        ydata = ydata.reshape(15,15)
        make_mul_plot(ydata,res_data_1,self.output_image_filename)

    # 输入mac_run则直接跑结果，否则仅输出参数
    def run(self):
        _, answer = self.part_1()
        np.save(self.output_param_filename,answer)
        print ("Save : ",self.output_param_filename)
        
        if self.mac_run:
            point_zip = self.part_2()
            self.part_3(point_zip,answer)

    # 不支持直接求球谐函数的参数
    def linux_run(self):
        answer = np.load(self.output_param_filename)
        point_zip = self.part_2()
        print ("Part 2, finish")
        self.part_3(point_zip,answer)
