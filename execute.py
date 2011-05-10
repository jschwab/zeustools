import glob
import os
import shlex
import shutil
import subprocess
import sys

class ZeusMP:

    def __init__(self, rootdir = "./"):
        self.zeusdir = rootdir
        self.exedir = "exe90"

    def run(self, nproc = 1):
        """Run ZEUS-MP2 and post-process the output"""

        fstdout = open(os.path.join(self.zeusdir, self.exedir, "zmp.stdout"), 'w')

        try:
            zmp_exe = os.path.join(self.zeusdir, self.exedir,"zeusmp.x")
            zmp = shlex.split("openmpirun -n {} {}".format(nproc, zmp_exe))

            subprocess.check_call(zmp, stdout = fstdout,
                                  cwd = os.path.join(self.zeusdir, self.exedir))

        except (OSError, subprocess.CalledProcessError):
            print("Running Zeus Failed")
            print("Terminating...")
            sys.exit(-1)

        fstdout.close()

        try:
            pp = subprocess.Popen(os.path.join(self.zeusdir, self.exedir, "zmp_pp.x"),
                                  cwd = os.path.join(self.zeusdir, self.exedir),
                                  stdin=subprocess.PIPE, 
                                  stdout = subprocess.PIPE)
        except:
            pass
        
        nfiles = len(glob.glob(os.path.join(self.zeusdir, self.exedir, "hdfaa000000.*"))) - 1
        pp.communicate(input="auto_h5\n0\n{}\nquit\n".format(nfiles))


        return 

    def compile(self, newprob = False):
        """ Recompile ZEUS-MP2"""
        pass


    def archive(self, target_dir):
        
        def archive_file(filename, target_dir):
            return os.rename(os.path.join(self.zeusdir,self.exedir,filename), 
                             os.path.join(target_dir, filename))



        try:
            os.mkdir(target_dir)
        except OSError:
            shutil.rmtree(target_dir)
            os.mkdir(target_dir)

        hdf_files = glob.glob(os.path.join(self.zeusdir, self.exedir, "hdfaa.*"))
        for hdf_file in hdf_files:
            hdf_filename = os.path.split(hdf_file)[1]
            archive_file(hdf_filename, target_dir)
                
        for filename in ["zmp_log", "zmp_inp", "zmp.stdout"]:
            archive_file(filename, target_dir)

        pre_files = glob.glob(os.path.join(self.zeusdir, self.exedir,"hdfaa*.*"))
        for pre_file in pre_files:
            os.remove(pre_file)

        return

