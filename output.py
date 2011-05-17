import glob
import h5py
import numpy as np
import os

class Error(Exception):
    pass

class ComparisonError(Error):

   def __init__(self, var, value1, value2):
       self.var = var
       self.value1 = value1
       self.value2 = value2

class DifferenceError(Error):

   def __init__(self, var, diff, locs):
       self.var = var
       self.diff = diff
       self.locs = locs

   def showall(self):
       diff_fmt = "    Does not match at ({:4d},{:4d},{:4d})  |  diff = {:18.12E}"
       for (k,j,i) in  zip(*self.locs):
           print(diff_fmt.format(i,j,k,self.diff[k,j,i]))

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

def assert_near_equality(a,b):

    t1 = np.allclose(a,b,rtol = 1e-9, atol = 0)
    t2 = np.allclose(b,a,rtol = 1e-9, atol = 0)
    
    if not (t1 and t2):
        diff  =  np.abs(a-b)
        locs = diff.nonzero()
        raise DifferenceError(None, diff, locs)
        
    return

def assert_equality(a,b):

    if not np.array_equal(a,b):
        diff  =  np.abs(a-b)
        locs = diff.nonzero()
        raise DifferenceError(None, diff, locs)
        
    return
                    
def compare_two(output1, output2, unforgiving = True, verbose = True):

    nomatch_msg = "  Files do not match: {:} differs"

    for (file1, file2) in zip(output1.files, output2.files):
        
        print("Comparing {} with {}".format(file1, file2))

        f1 = ZeusMPHDF5(file1) 
        f2 = ZeusMPHDF5(file2) 

        try: # try to compare the files

            # check that time stamps are the same
            t1 = f1.get_dset("t")[0]
            t2 = f2.get_dset("t")[0]
            if t1 != t2:
                raise ComparisonError("t", t1, t2)
        
            # check that the array dimensions are the same
            for axis in ['x1','x2','x3']:
                c1 = f1.get_dset(axis)
                c2 = f2.get_dset(axis)
                if c1.size != c2.size:
                    raise ComparisonError(axis, c1.size, c2.size)

            # check that coordinates are the same
            for axis in ['x1','x2','x3']:
                c1 = f1.get_dset(axis)
                c2 = f2.get_dset(axis)
                try:
                    assert_equality(c1,c2)
                except DifferenceError as e:
                    e.var = axis
                    raise e


            # check that velocities are the same
            for axis in ['v1','v2','v3']:
                c1 = f1.get_dset(axis)
                c2 = f2.get_dset(axis)
                try:
                    assert_near_equality(c1,c2)
                except DifferenceError as e:

                    e.var = axis

                    if unforgiving:
                        raise e
                    else:
                        print(nomatch_msg.format(axis))
                        e.showall()

            # check that physical variables are the same
            for axis in ["e","d"]:
                c1 = f1.get_dset(axis)
                c2 = f2.get_dset(axis)
                try:
                    assert_near_equality(c1,c2)
                except DifferenceError as e:
                    
                    e.var = axis
                        
                    if unforgiving:
                        raise e
                    else:
                        print(nomatch_msg.format(axis))
                        e.showall()
                

        except ComparisonError as CE:
            msg_str = "  Cannot compare files: {:} differs [{:18.12E} != {:18.12E}]"
            print(msg_str.format(CE.var, CE.value1, CE.value2))

        except DifferenceError as DE:
            if DE.var in ['x1','x2','x3']: # if coordinates differ
                msg_str = "  Cannot compare files: {:} differs"
                print(msg_str.format(DE.var))
            else:
                msg_str = "  Files do not match: {:} differs"
                print(msg_str.format(DE.var))
                if verbose: DE.showall()
        finally:
            f1.close()
            f2.close()

    return

class ZeusMPHDF5:

    def __init__(self, filename):
        self.filename = filename
        self.file = h5py.File(filename)
             
    def get_dset(self, name):
        return self.file[datanames[name]][:]

    def close(self):
        self.file.close()


class ZeusMPOutput:

    def __init__(self, datadir = "./"):
        self.datadir = datadir
        self.files = glob.glob(os.path.join(datadir, "hdfaa.*"))
        self.files.sort()



if __name__ == "__main__":
    pass
