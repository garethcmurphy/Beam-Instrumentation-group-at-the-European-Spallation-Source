#!/usr/bin/env python3
"""visit beam file"""
import h5py


def print_attrs(name, obj):
    """visit beam file"""
    #    print (name)
    for key, val in obj.attrs.items():
        print('  "%s/%s": "%s",' % (name, key, val))


def main():
    """main"""
    filename = "Bias_tee_testing.hdf5"
    filename = "FC_LEBT_verification.hdf5"
    # filename="FMC-PICO-evaluation.hdf5"
    file = h5py.File(filename, 'r')
    print("{")
    file.visititems(print_attrs)
    print("}")


if __name__ == "__main__":
    main()
