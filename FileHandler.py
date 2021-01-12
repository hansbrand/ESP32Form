

from _thread import *
from threading import Thread
import threading 
import os
import time
import queue

filename = None
logfd = None
filelock = threading.RLock() 
filestat = "UNKOWN"
messages = None
opened = False
saving = False



def openfiles():
    global logfd
    global filename
    global filelock
    global filestat
    global opened
    global messages


    try:
        if opened : return
        filelock.acquire()
        #if (logfd != None):
        #    print("File already open !")
        #else:
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, 'dist\\') + "DIST"+time.strftime("%H_%M_%S")+".txt"
        #logfd=open(filename,"wt+")
        filestat = "OPEN"
        messages = queue.Queue()
        opened = True
        filelock.release()
    except Exception as pex:
        print("openfiles",pex)


def writefile(s):
    global logfd
    global filelock
    global filestat
    global messages
    global opened

    filelock.acquire()
    if (opened ):
        #logfd.write(s)
        messages.put(s)
        filestat = "RECORD"
    filelock.release()


def closeFiles():
    global logfd
    global filelock
    global filestat
    global saving

    filestat = "SAVING"

    filelock.acquire()
    

    if saving: 
        filelock.release()
        filestat = "CLOSED"
        return
    if messages == None:
        filelock.release()
        filestat = "CLOSED"
        return
    if messages.empty() :
        filelock.release()
        filestat = "CLOSED"
        return
    
    saving = True
    print("Files closed")

    sth2 = threading.Thread(target=savefile,daemon=True)
                                    #args=(s,),daemon=True)
    
    sth2.start()
    filelock.release()
    filestat = "CLOSED"


def savefile():
    global logfd
    global filelock
    global filestat
    global messages
    global filename
    global opened
    global saving

    filelock.acquire()
    try:
        if messages.empty() :
            filelock.release()
            return

        total = messages.qsize()
        logfd=open(filename,"wt+")
        #for i in range(0,total):
        counter = 0
        while not messages.empty():
            lstr = messages.get(block =False)
            logfd.write(lstr)
            perc = str(round(((float(counter) / float(total)) * 100.0),2)) + "%"
            #filestat = "Saving : " + perc
            counter += 1
            print(filestat)
        logfd.close()
        opened = False
        saving = False
        filelock.release()
        return
    except Exception as pex:
        print("savefile",pex)
            




