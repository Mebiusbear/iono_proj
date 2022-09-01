from turtle import st
from src.workflow import Fit_iono
from src.apps.make_plot import make_plot

import os
import numpy as np
import argparse
import time

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='YOLO Detection')
    parser.add_argument("-np","--npixel", type=int, help="the pixel.", default=100)
    parser.add_argument("-s","--steps", type=int, help="the steps.", default=5)
    parser.add_argument("-nw","--n_worker", type=int, help="n_worker.", default=1)
    parser.add_argument("-bs","--block_size", type=int, help="block_size.", default=400)
    parser.add_argument("-po","--plot_only", type=bool, help="plot_only.", default=False)

    args = parser.parse_args()
    iono = Fit_iono(args)

    start = time.time()

    if args.plot_only:
        iono.make_plot()
    else:
        iono.run()

    end = time.time()
    print ("use time(second) : ",end-start)



    

