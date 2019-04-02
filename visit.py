#!/usr/bin/env python3
import h5py
def print_attrs(name, obj):
#    print (name)
    for key, val in obj.attrs.items():
        print ('  "%s/%s": "%s",' % (name,key, val))

array = {}
filename="Bias_tee_testing.hdf5"
filename="FC_LEBT_verification.hdf5"
#filename="FMC-PICO-evaluation.hdf5"
f = h5py.File(filename,'r')
print("{")
f.visititems(print_attrs)
print("}")
