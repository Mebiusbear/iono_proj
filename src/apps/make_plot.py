from tokenize import PlainToken
import matplotlib.pyplot as plt
import numpy as np
import os

def make_plot(filename):
    im = np.load(filename)

    plt.imshow(im)
    plt.colorbar()
    plt.show()

def make_mul_plot(ydata,res_data_1,npy_filename):
    
    npy_results_dir = os.path.dirname(os.path.dirname(npy_filename))
    png_results_dir = os.path.join(npy_results_dir,"image_png")
    name = npy_filename.split("/")[-1][:-4] + ".png"
    png_filename = os.path.join(png_results_dir,name)

    plt.figure(figsize=(16,9))

    plt.subplot(131)
    plt.title("origin")
    plt.axis("off")
    plt.imshow(np.array(ydata))

    plt.subplot(132)
    plt.title("280 point")
    plt.axis("off")
    plt.imshow(res_data_1)

    plt.subplot(133)
    plt.title("4000^2 point")
    plt.axis("off")
    res_data_2 = np.load(npy_filename)
    plt.imshow(res_data_2)

    plt.savefig(png_filename)
    plt.show()