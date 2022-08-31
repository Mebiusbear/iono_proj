from tokenize import PlainToken
import matplotlib.pyplot as plt
import numpy as np

def make_plot(filename):
    im = np.load(filename)

    plt.imshow(im)
    plt.colorbar()
    plt.show()
