import ctypes

ll = ctypes.cdll.LoadLibrary

lib = ll("./legendre.so")

a = lib.caculate_nkm(3,2)

print (a)