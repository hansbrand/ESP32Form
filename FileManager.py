
from tkinter import filedialog
from tkinter import *
import os
import json 
import queue
import time
import sys
import logging
import ScanStrategy as SS


from FileHandler import filestat 
import ESPDevices
import DataContainer
from DataPoint import DataPoint 
#import MeshCreator as MC

isScanning = False
isLoaded = False
logger = None
#import ESP32Form



def getDistanceColor(val,limits = None):

    if val == -30000:
        return ("black")

    if (DataContainer.limits3D != None):
        BLUEVALUE = max(DataContainer.limits3D["maxdistance"],-DataContainer.limits3D["maxdistance"])
        REDLIMIT = BLUEVALUE * 0.4
        GREENLIMIT = BLUEVALUE * 0.1
    else:
        return((0,0,0))

    if val > BLUEVALUE: 
        return((0,0,255))

    if val < GREENLIMIT: 
        return((0,255,0))            


    if val < REDLIMIT:
        refval = (REDLIMIT - float(val))  
        delta = float(REDLIMIT - GREENLIMIT)  
        refquot = refval / delta
        if (refquot > 1):
            refquot = 1
        r = min (int((1 - refquot) * 255.0), 255)
        g = min (int(refquot * 255.0), 255)
        b = 0
    else:
        refval =  (float(val) - REDLIMIT) 
        delta =  (BLUEVALUE - REDLIMIT) 
        refquot = refval / delta
        if (refquot > 1):
            refquot = 1
        r = min (int((1 - refquot) * 255.0), 255)
        g = 0
        b = min (int(refquot * 255.0), 255)
    return (r,g,b)

def analyse(line):
    mi = messageInfo()
    mi.currentMessage=line
    try:
        stt = line;

        #print("received")
        #print(mlist)
        
        fd = None
        if (line[0] !=  "{"):
            newstr = line.split(";")
            if newstr[1][0]  == "T":
                mi.mstatus = newstr[1][0]
                mi.raspi=newstr[1]
                #if "Connected" in newstr[1]:
                #    newstr = newstr[1].split(",")
                #    newstr = newstr[0].split(":")
        else:
            x = json.loads(line)
            #print("messagetype : ", x["messagetype"])
            #print("messagetype : ", x["original"])

            if "null" in x["original"]:
                print(x)

            if "Er" in x["original"]:
                x["tag"] = "E"
                mi.hdegree = x["xdegree"]
                mi.vdegree = x["vdegree"]
                mi.quality= 10000
                mi.messagetype = x["messagetype"]


            if x["tag"] in ("D","M","F","S"):
                try:
                    sttag = x["tag"]
                    mi.mstatus=sttag
                    mi.messagetype = x["messagetype"]
                    mi.device = x["name"] + mi.mstatus
                    stt = x["original"]
                    if (sttag != "S"):
                        stt = stt[2:]
                        nlist = stt.split(",")
                        mpos = nlist[0].replace("m","")
                        #newerstr= mpos[2:]
                        newval = str((int((float(mpos)*1000.0))/1000)*1000)
                        mi.distance = newval
                        mi.hdegree = x["xdegree"]
                        mi.vdegree = x["vdegree"]
                        mi.quality= int(nlist[1])

                except Exception as inst:
                    print (inst)
                    
            if x["tag"] == "E":
                mi.mstatus="E"
                mi.device = x["name"] + mi.mstatus
                mi.messagetype = x["messagetype"]

                mi.error = x["original"]
                mi.hdegree = x["xdegree"]
                mi.vdegree = x["vdegree"]

            if x["tag"] in ("O","C"):
                mi.mstatus = x["tag"]
                mi.messagetype = x["messagetype"]
            mi.jsondata=x
            return mi
    except Exception as inst:
        print(type(inst)) 
        print(inst)
        print("analyse")
        return None


def isloaded():
    global isLoaded
    if isLoaded:
        isLoaded = False
        return True
    return False

def saveHull(hull):
    try:
        dirname = os.path.dirname(__file__)
        datestr = time.strftime("%y_%m_%d")

        ISLINUXOS = sys.platform.startswith('linux') or sys.platform.startswith('cygwin')
        if ISLINUXOS:
            directory =os.path.join(dirname, 'dist/') + datestr
            if  not os.path.isdir(directory):
                os.mkdir(directory)
            filename = directory + "/DIST" + time.strftime("%H_%M_%S")+"_hull.txt"
        else:
            directory =os.path.join(dirname, 'dist\\') + datestr
            if  not os.path.isdir(directory):
                os.mkdir(directory)
            filename = directory + "\\DIST" + time.strftime("%H_%M_%S") +"_hull.txt"
 
        with open(filename, 'wt+') as f:
            for h in hull:
                l = h[0] + " " + h[0] + " " + h[0] + "\n"
                f.write(l)


    except Exception as exc:
        print(exc)


def loadfile(filename):
    global isScanning
    global isLoaded

    try:

        counter = 0
        isScanning = True
        DataContainer.initDataContainer()
        datafd=open(filename,"rt")
        buffer = datafd.readlines()
        datafd.close()
        SS.initSimulation("DETAIL")
        for message in buffer:
            ident = message[0:2]
            if ident in   ESPDevices.deviceList:
                counter = (counter + 1) % 10
                # if (counter == 0):
                #     time.sleep(.01)
                #print("Device found :" + message)
                if (message[:5] == 'C1|M3'):
                    SS.simulateTurn()
                if (ESPDevices.isSensor(message)):
                    #if (('Er' in message) == False):
                        dp = DataPoint(message)
                        DataContainer.addPoint(dp)
                        
        #print(DataContainer.getlimits3D())
        #time.sleep(2)
        isScanning = False
        isLoaded = True
        #hull = DataContainer.createHull()
        #saveHull(hull)

        #print(DataContainer.StatusList)
        return True
    except Exception as pex:
        print("loadfile:",pex)
        return False






def openLoadFile(master):
    ISLINUXOS = sys.platform.startswith('linux') or sys.platform.startswith('cygwin')
    if (ISLINUXOS):
        filename = filedialog.askopenfilename(initialdir = "./dist",title = "Data File",filetypes = (("Data files","*.txt"),("all files","*.*")))
    else:
        filename = filedialog.askopenfilename(initialdir = ".\\dist",title = "Data File",filetypes = (("Data files","*.txt"),("all files","*.*")))

    print("Filename :", filename)
    if (filename == ''):
        return False
    check= loadfile(filename)


    return check



def openMeshFile(master):
    ISLINUXOS = sys.platform.startswith('linux') or sys.platform.startswith('cygwin')
    if (ISLINUXOS):
        filename = filedialog.askopenfilename(initialdir = "./dist",title = "Data File",filetypes = (("Data files","*.xyz"),("all files","*.*")))
    else:
        filename = filedialog.askopenfilename(initialdir = ".\\dist",title = "Data File",filetypes = (("Data files","*.xyz"),("all files","*.*")))

    print("Filename :", filename)
    if (filename == ''):
        return False
    #MC.createmesh(filename)

    return check


def saveCSVlist(slist,ext):
    try:
        dirname = os.path.dirname(__file__)
        datestr = time.strftime("%y_%m_%d")

        ISLINUXOS = sys.platform.startswith('linux') or sys.platform.startswith('cygwin')
        if ISLINUXOS:
            directory =os.path.join(dirname, 'dist/') + datestr
            if  not os.path.isdir(directory):
                os.mkdir(directory)
            filename = directory + "/DIST" + time.strftime("%H_%M_%S")+"_" + ext +".txt"
        else:
            directory =os.path.join(dirname, 'dist\\') + datestr
            if  not os.path.isdir(directory):
                os.mkdir(directory)
            filename = directory + "\\DIST" + time.strftime("%H_%M_%S") +".txt"
 
        with open(filename, 'wt+') as f:
            for l in slist:
                #line = str(int(x[l])) + ";" + str(int(y[l])) + ";" + str(int(z[l])) + "\n"
                #l = l.replace("|",";")
                f.write(l)
        if ISLINUXOS:
            directory =os.path.join(dirname, 'dist/') + datestr
            if  not os.path.isdir(directory):
                os.mkdir(directory)
            filename = directory + "/DIST" + time.strftime("%H_%M_%S")+"_" + ext +".xyz"
            filecolor = directory + "/DIST" + time.strftime("%H_%M_%S")+"_col.xyz"
        else:
            directory =os.path.join(dirname, 'dist\\') + datestr
            if  not os.path.isdir(directory):
                os.mkdir(directory)
            filename = directory + "\\DIST" + time.strftime("%H_%M_%S")+ ".xyz"
            filecolor = directory + "\\DIST" + time.strftime("%H_%M_%S")+"_col.xyz"

 
        with open(filename, 'wt+') as f:
            for l in DataContainer.PointCloud:
                if (l.state == "VALID"):
                    line = str(l.x) + " " + str(l.y) + " " + str(l.z) +  "\n"
                    #l = l.replace("|"," ")
                    f.write(line)

        with open(filecolor, 'wt+') as f:
            for l in DataContainer.PointCloud:
                if (l.state == "VALID"):
                    r,g,b = getDistanceColor(l.meter)
                    line = str(l.x) + " " + str(l.y) + " " + str(l.z) + "\t\t" + str(r) +  " " + str(g) +  " " + str(b) + "\n"
                    #l = l.replace("|",";")
                    f.write(line)


    except Exception as exc:
        print(exc)

def SaveTurn(slist,width, height,turn):
        dirname = os.path.dirname(__file__)
        datestr = time.strftime("%y_%m_%d")

        ISLINUXOS = sys.platform.startswith('linux') or sys.platform.startswith('cygwin')
        if ISLINUXOS:
            directory =os.path.join(dirname, 'TURN/')
            if  not os.path.isdir(directory):
                os.mkdir(directory)
            dirname = str(width) + "_" + str(height) + "_" + str(turn) 
            directory = directory + dirname + "/"
            if  not os.path.isdir(directory):
                os.mkdir(directory)
            filename= directory + dirname + ".txt" 
        else:
            directory =os.path.join(dirname, 'TURN\\')
            if  not os.path.isdir(directory):
                os.mkdir(directory)
            dirname = str(width) + "_" + str(height) + "_" + str(turn) 
            directory = directory + dirname + "\\"
            if  not os.path.isdir(directory):
                os.mkdir(directory)
            filename= directory + dirname + ".txt" 
 
        with open(filename, 'wt+') as f:
            for l in slist:
                #line = str(int(x[l])) + " " + str(int(y[l])) + " " + str(int(z[l])) + "\n"
                #l = l.replace("|",";")
                f.write(l)


def LoadTurn(width, height,turn):
        dirname = os.path.dirname(__file__)
        datestr = time.strftime("%y_%m_%d")

        ISLINUXOS = sys.platform.startswith('linux') or sys.platform.startswith('cygwin')
        if ISLINUXOS:
            directory =os.path.join(dirname, 'TURN/')
            if  not os.path.isdir(directory):
                os.mkdir(directory)
            filename= directory + str(width) + "_" + str(height) + "_" + str(turn) + ".txt" 
        else:
            directory =os.path.join(dirname, 'TURN\\')
            if  not os.path.isdir(directory):
                os.mkdir(directory)
            filename= directory + str(width) + "_" + str(height) + "_" + str(turn) + ".txt" 
 
        loadfile(filename)


def startlogging():
        global logger

        dirname = os.path.dirname(__file__)
        datestr = time.strftime("%y_%m_%d_%H_%M")

        ISLINUXOS = sys.platform.startswith('linux') or sys.platform.startswith('cygwin')
        if ISLINUXOS:
            directory =os.path.join(dirname, 'logs/')
            if  not os.path.isdir(directory):
                os.mkdir(directory)
            filename= directory + datestr + ".txt" 
        else:
            directory =os.path.join(dirname, 'logs\\')
            if  not os.path.isdir(directory):
                os.mkdir(directory)
            filename= directory + datestr + ".txt" 
        logger = filename
        return
        pass 

def dlog(message):
    global logger
    datestr = time.strftime("%y_%m_%d_%H_%M")

    with open(logger, 'at+') as f:
        f.write("DEBUG : " +  datestr + "   " + message + "\n")
    return

def ilog(message):
    global logger
    datestr = time.strftime("%y_%m_%d_%H_%M")

    with open(logger, 'at+') as f:
        f.write("INFO : " +  datestr + "   " + message + "\n")
    return
