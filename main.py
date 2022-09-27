from turtle import st
from src.workflow import Fit_iono
from src.apps.make_plot import make_plot

import os
import numpy as np
import argparse
import time

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='YOLO Detection')
    parser.add_argument("-np","--npixel", type=int, default=100)
    parser.add_argument("-ps","--pscale", type=float, default=0.1)
    parser.add_argument("-s","--steps", type=int, default=5)
    parser.add_argument("-nw","--n_worker", type=int, default=1)
    parser.add_argument("-bs","--block_size", type=int, default=400)
    parser.add_argument("-po","--plot_only", default=False, action='store_true')
    parser.add_argument("-mr","--mac_run", default=False, action='store_true')
    parser.add_argument("-lr","--linux_run", default=False, action='store_true')
    parser.add_argument("-mmp","--make_mul_plot", default=False, action='store_true')
    parser.add_argument("-sch","--scheduler", type=str)

    args = parser.parse_args()
    print (args)
    iono = Fit_iono(args)

    start = time.time()

    if args.plot_only:
        if args.make_mul_plot:
            iono.makemulplot()
        else:
            iono.makeplot()
    else:
        if args.linux_run:
            iono.linux_run()
        else :
            iono.run()


    end = time.time()
    print ("use time(second) : ",end-start)

