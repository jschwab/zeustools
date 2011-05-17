import glob
import os
import re
import shlex
import shutil
import subprocess
import sys

class ZeusMP:

    def __init__(self, rootdir = "./", makefile = "Makefile", mpiexec = "mpirun"):
        self.zeusdir = rootdir
        self.exedir = "exe90"
        self.srcdir = "src90"
        self.makefile = makefile
        self.mpiexec = mpiexec

    def run(self, nproc = 1):
        """Run ZEUS-MP2 and post-process the output"""

        fstdout = open(os.path.join(self.zeusdir, self.exedir, "zmp.stdout"), 'w')

        try:
            zmp_exe = os.path.join(self.zeusdir, self.exedir,"zeusmp.x")
            zmp = shlex.split("{} -n {} {}".format(self.mpiexec, nproc, zmp_exe))

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

    def clean(self):
        """Run make clean"""

        make_clean = "make -f {} clean".format(self.makefile)
        subprocess.check_call(shlex.split(make_clean), stdout = subprocess.PIPE,
                              cwd = os.path.join(self.zeusdir, self.srcdir))

        return

    def newprob(self, probname):
        """Run make newprob and set DPROBLEM=probname"""

        make_newprob = "make -f {} newprob".format(self.makefile)
        subprocess.check_call(shlex.split(make_newprob), stdout = subprocess.PIPE,
                              cwd = os.path.join(self.zeusdir, self.srcdir))
        
        # read in the makefile
        with open(os.path.join(self.zeusdir, self.srcdir, self.makefile), "r") as mf:
            lines = mf.readlines()

        # write it back out
        with open(os.path.join(self.zeusdir, self.srcdir, self.makefile), "w") as mf:
            for line in lines:
                mf.write(re.sub("DPROBLEM=\w*","DPROBLEM={}".format(probname),line))



    def compile(self, newprob = False):
        """ Recompile ZEUS-MP2"""

        make_all = "make -f {} all".format(self.makefile)
        subprocess.check_call(shlex.split(make_all), stdout = subprocess.PIPE,
                              cwd = os.path.join(self.zeusdir, self.srcdir))

        return


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


if __name__ == "__main__":
    z = ZeusMP("/Users/jschwab/Research/Software/zeusmp2", makefile = "Makefile.laptop", mpiexec = "openmpirun")
    z.newprob("blast")
    z.compile()
