#!/usr/bin/env python
from __future__ import division
from __future__ import print_function
from future import standard_library
standard_library.install_aliases()
from builtins import str
from builtins import range
from past.utils import old_div
from subprocess import call
import sys
from threading import Thread
from queue import Queue

queue = Queue()
num = 9
size = 10240    #creates 10MB image
#size = 102400  #creates 100MB image

def createImage(i,q,dest = "/tmp"):
    """creates N 10mb identical image files"""
    global num
    global size
    value = "%sMB " % str(old_div(size,1024))
    while True:
        i = q.get()
        print("Creating %s image #%s in %s inside of thread %s" % (value,i,dest,i))
        cmd = "dd if=/dev/zero of=%s/10mbfile.%s bs=1024 count=%s" % (dest,i,size)
        status = call(cmd, shell=True)
        if status != 0:
            print("Trouble creating image files", err)
            sys.exit(1)
        q.task_done()

def controller():
    global num
    #spawn N worker pool threads
    for i in range(num):
        worker = Thread(target=createImage, args=(i,queue))
        worker.setDaemon(True)
        worker.start()
    #populate queue with N jobs
    for n in range(num):
        queue.put(n)

    print("Main Thread Waiting")
    queue.join()
    print("Done")
if __name__ == "__main__":
    controller()

