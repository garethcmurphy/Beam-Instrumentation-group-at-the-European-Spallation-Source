#!/usr/bin/env python3
import h5py
f = h5py.File('FMC-PICO-evaluation.hdf5', 'r')
print(list(f.keys()))
g=f['/FMC-PICO/FMC-Pico-1m4-C3'].keys()
print(list(g))
a=f['/FMC-PICO/FMC-Pico-1m4-C3/18002_CH4_RNG1_OC'].attrs
for name in a:
    print(name,":", a[name])
f.close()

