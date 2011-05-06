import os
import subprocess
import sys

class ZeusMP:

    def __init__(self, rootdir = "./"):
        self.zeusdir = rootdir

    def run(self):
        """Run ZEUS-MP2 and post-process the output"""

        fstdout = open(os.path.join(self.zeusdir, "exe90/zmp.stdout"), 'w')

        try:
            subprocess.check_call(os.path.join(self.zeusdir, "exe90/zeusmp.x"),
                                  cwd = os.path.join(self.zeusdir, "exe90"),
                                  stdout = fstdout)
        except (OSError, subprocess.CalledProcessError):
            print("Running Zeus Failed")
            print("Terminating...")
            sys.exit(-1)

        fstdout.close()

        try:
            pp = subprocess.Popen(os.path.join(self.zeusdir, "exe90/zmp_pp.x"),
                                  cwd = os.path.join(self.zeusdir, "exe90"),
                                  stdin=subprocess.PIPE, 
                                  stdout = subprocess.PIPE)
        except:
            pass
        
        nfiles = 1
        pp.communicate(input="auto_h5\n0\n{}\nquit\n".format(nfiles))


        return 

    def compile(self, newprob = False):
        """ Recompile ZEUS-MP2"""
        pass


    def archive_files(archive_dir):

        try:
            os.mkdir(archive_dir)
        except OSError:
            shutil.rmtree(archive_dir)
            os.mkdir(archive_dir)

            hdf_files = glob.glob("hdfaa.*")
            for hdf_file in hdf_files:
                os.rename(hdf_file, os.path.join(archive_dir, hdf_file))
                
                shutil.copy("zmp_inp", os.path.join(archive_dir, "zmp_inp"))
                shutil.copy("zmp_log", os.path.join(archive_dir, "zmp_log"))

                return

# remove any leftover output files

    def cleanup():
                
        pre_files = glob.glob("hdfaa*.*")
        for pre_file in pre_files:
            os.remove(pre_file)
            
        return
