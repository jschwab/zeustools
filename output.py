import glob
import h5py
import numpy as np
import os

# define map to the HDF5 datasets
datanames = {"t" : "   time",
             "x1": "i coord",
             "x2": "j coord",
             "x3": "k coord",
             "v1": " i velocity", 
             "v2": " j velocity", 
             "v3": " k velocity", 
             "e":  " gas energy",
             "d":  "gas density",
             "T":  "temperature"}

err_fmt = "{:2s} does not match at ({:4d},{:4d},{:4d})  |  diff = {:18.12E}"

# define a norm function

def array_compare(array1, array2):
    ac = {}
    adiff = abs(array1 - array2)
    ac['max'] = adiff.max()
    ac['avg'] = adiff.mean()
    return ac

def compare_one():
    pass

def on_tile_boundary(i,j,k):
    return (i == 63)

def compare_two(output1, output2):

    for (file1, file2) in zip(output1.files, output2.files):
        
        print("Comparing {} with {}".format(file1, file2))

        f1 = ZeusMPHDF5(file1) 
        f2 = ZeusMPHDF5(file2) 

        # check that time stamps are the same
        t1 = f1.get_dset("t")
        t2 = f2.get_dset("t")
        if np.array_equal(t1,t2):
            print("Time matches")
        else:
            print("Timestamps do not match, {} != {}".format(t1,t2))


        # check that coordinates are the same
        for axis in ['x1','x2','x3']:
            c1 = f1.get_dset(axis)
            c2 = f2.get_dset(axis)
            if np.array_equal(c1,c2):
                print("{} matches".format(axis))
            else:
                print("{} does not match".format(axis))

        # check that velocities are the same
        for axis in ['v1','v2','v3']:
            c1 = f1.get_dset(axis)
            c2 = f2.get_dset(axis)
            if np.array_equal(c1,c2):
                print("{} matches".format(axis))
            else:
                diff  =  np.abs(c1-c2)
                nz = diff.nonzero()
                for (k,j,i) in zip(*nz):
                    if not on_tile_boundary(i,j,k):
                        print(err_fmt.format(axis,i,j,k, diff[k,j,i]))

        # check that physical variables are the same
        for axis in ["e","d"]:
            c1 = f1.get_dset(axis)
            c2 = f2.get_dset(axis)
            if np.array_equal(c1,c2):
                print("{} matches".format(axis))
            else:
                diff  =  np.abs(c1-c2)
                nz = diff.nonzero()
                for (k,j,i) in zip(*nz):
                    print(err_fmt.format(axis,i,j,k, diff[k,j,i]))

    return

class ZeusMPHDF5:

    def __init__(self, filename):
        self.filename = filename
        self.file = h5py.File(filename)
             
    def get_dset(self, name):
        return self.file[datanames[name]][:]


class ZeusMPOutput:

    def __init__(self, datadir = "./"):
        self.datadir = datadir
        self.files = glob.glob(os.path.join(datadir, "hdfaa.*"))



