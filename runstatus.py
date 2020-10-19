import sys, os
import time

pidfile = ".runner.pid"
statusfilename = ".runner.status"


#
# open the pidfile and read the process id
# give an error message if file not found or bad pid
try:
    fin = open(pid_file, "r")
    pid = fin.readline()
    os.kill(pid, signal.SIGUSR1) #发送signal
except Exception as e:
    print(f"file {status_file} {e}")
finally:
    fin.close()
# send the USR1 signal to runner.py
# open the status file for reading and check the size
try:
    start =time.clock()
    fin = open(status_file)
# wait until it is non zero size, then read contents and copy to output, then quit.
    while os.path.getsize(status_file) == 0:
        end = time.clock()
        if end - start > 5:
            raise Exception("status timeout")  #超时错误
    for line in fin:
        print(lien)
    fin.close()

    fin = open(status_file)
    f1.truncate(0)
    fin.close()
    
except Exception as e:  # give error messages as necessary
    print(f"file {status_file} {e}")
finally:
    fin.close()
