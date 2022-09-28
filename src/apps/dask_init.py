from dask.distributed import Client
from src.apps.log_func import init_logging

def dask_init(args,n_worker,scheduler):
    npixel = args.npixel
    steps = args.steps
    pixel_per_screensize_km = args.pscale

    if scheduler == None:
        client = Client(n_workers=n_worker)
    else:
        client = Client(scheduler)
        print ("Client OK!, scheduler: ",scheduler)
    # client.run(init_logging,npixel,steps,pixel_per_screensize_km)

    return client