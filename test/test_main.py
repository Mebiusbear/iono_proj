import numpy as np
import sys

sys.path.append("./")
a = np.load("./test/data/cpp_100_6.npy")
b = np.load("./test/data/python_100_6.npy")

print (np.allclose(a,b))